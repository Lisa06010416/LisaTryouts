from __future__ import annotations

from pydantic import BaseModel, Field

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from lang_stack_research_agent.common.tools import web_search
from lang_stack_research_agent.v1.state import AgentState


class ClassifyResult(BaseModel):
    needs_search: bool = Field(description="Whether answering requires current external information.")
    reason: str = Field(description="Short routing rationale.")


def classify_node(llm: BaseChatModel):
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "Classify whether the user question needs fresh external search. "
                "Use search for current, recent, latest, or time-sensitive facts.",
            ),
            ("human", "{question}"),
        ]
    )
    chain = prompt | llm.with_structured_output(ClassifyResult)

    def classify(state: AgentState) -> AgentState:
        result = chain.invoke({"question": state["question"]})
        return {
            "needs_search": result.needs_search,
            "route_reason": result.reason,
        }

    return classify


def search_node(llm: BaseChatModel):
    llm.bind_tools([web_search])

    def search(state: AgentState) -> AgentState:
        result = web_search.invoke({"query": state["question"]})
        return {
            "search_results": [result],
            "searched": True,
        }

    return search


def answer_node(llm: BaseChatModel):
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "Answer concisely. If search results are provided, ground the answer in them. "
                "If no search was needed, answer directly.",
            ),
            ("human", "Question: {question}\nSearch results: {search_results}"),
        ]
    )
    chain = prompt | llm | StrOutputParser()

    def answer(state: AgentState) -> AgentState:
        search_results = state.get("search_results", [])
        return {
            "answer": chain.invoke(
                {
                    "question": state["question"],
                    "search_results": "\n".join(search_results) if search_results else "None",
                }
            ),
            "searched": state.get("searched", False),
        }

    return answer
