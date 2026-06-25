from __future__ import annotations

from pydantic import BaseModel, Field

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.types import interrupt

from mini_research_agent.common.tools import web_search
from mini_research_agent.v2.state import AgentState


class ClassifyResult(BaseModel):
    needs_search: bool = Field(description="Whether answering requires current external information.")
    is_ambiguous: bool = Field(description="Whether the question needs user clarification.")
    reason: str = Field(description="Short routing rationale.")


class ReflectionResult(BaseModel):
    ok: bool = Field(description="Whether the answer is good enough to finish.")
    critique: str = Field(description="Specific critique or reason to accept the answer.")


def classify_node(llm: BaseChatModel):
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "Classify the latest user question. Mark ambiguous only when the question lacks a concrete subject. "
                "Use search for current, recent, latest, or time-sensitive facts.",
            ),
            MessagesPlaceholder("messages"),
            ("human", "{question}"),
        ]
    )
    chain = prompt | llm.with_structured_output(ClassifyResult)

    def classify(state: AgentState) -> AgentState:
        result = chain.invoke(
            {
                "question": state["question"],
                "messages": state.get("messages", []),
            }
        )
        return {
            "needs_search": result.needs_search,
            "is_ambiguous": result.is_ambiguous,
            "route_reason": result.reason,
        }

    return classify


def clarify_node(llm: BaseChatModel):
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "Ask one concise clarification question."),
            MessagesPlaceholder("messages"),
            ("human", "{question}"),
        ]
    )
    chain = prompt | llm | StrOutputParser()

    def clarify(state: AgentState) -> AgentState:
        clarification_question = chain.invoke(
            {
                "question": state["question"],
                "messages": state.get("messages", []),
            }
        )
        user_reply = interrupt({"question": clarification_question})
        new_question = f"{state['question']}\nClarification: {user_reply}"
        return {
            "question": new_question,
            "is_ambiguous": False,
            "interrupted": True,
            "messages": state.get("messages", [])
            + [AIMessage(content=clarification_question), HumanMessage(content=str(user_reply))],
        }

    return clarify


def search_node(llm: BaseChatModel):
    llm.bind_tools([web_search])

    def search(state: AgentState) -> AgentState:
        query = state["question"]
        if state.get("critique") and state.get("retry_count", 0) > 0:
            query = f"{query}\nFind evidence that addresses this critique: {state['critique']}"
        result = web_search.invoke({"query": query})
        return {
            "search_results": state.get("search_results", []) + [result],
            "searched": True,
        }

    return search


def synthesize_node(llm: BaseChatModel):
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "Answer with a concise, grounded response. Use conversation history and search results when present.",
            ),
            MessagesPlaceholder("messages"),
            ("human", "Question: {question}\nSearch results: {search_results}"),
        ]
    )
    chain = prompt | llm | StrOutputParser()

    def synthesize(state: AgentState) -> AgentState:
        answer = chain.invoke(
            {
                "question": state["question"],
                "messages": state.get("messages", []),
                "search_results": "\n".join(state.get("search_results", [])) or "None",
            }
        )
        return {
            "answer": answer,
            "searched": state.get("searched", False),
            "messages": state.get("messages", []) + [HumanMessage(content=state["question"]), AIMessage(content=answer)],
        }

    return synthesize


def reflect_node(llm: BaseChatModel):
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "Judge whether the answer is complete, grounded, and directly answers the question. "
                "Return ok=false only when another search could materially improve it.",
            ),
            (
                "human",
                "Question: {question}\nAnswer: {answer}\nSearch results: {search_results}\nRetry count: {retry_count}",
            ),
        ]
    )
    chain = prompt | llm.with_structured_output(ReflectionResult)

    def reflect(state: AgentState) -> AgentState:
        result = chain.invoke(
            {
                "question": state["question"],
                "answer": state.get("answer", ""),
                "search_results": "\n".join(state.get("search_results", [])) or "None",
                "retry_count": state.get("retry_count", 0),
            }
        )
        retry_count = state.get("retry_count", 0)
        if not result.ok:
            retry_count += 1
        return {
            "reflection_ok": result.ok,
            "critique": result.critique,
            "retry_count": retry_count,
        }

    return reflect
