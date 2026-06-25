from __future__ import annotations

from typing import Literal

from langchain_core.language_models.chat_models import BaseChatModel
from langgraph.graph import END, START, StateGraph

from mini_research_agent.v1.nodes import answer_node, classify_node, search_node
from mini_research_agent.v1.state import AgentState


def route_after_classify(state: AgentState) -> Literal["search", "answer"]:
    return "search" if state.get("needs_search") else "answer"


def build_graph(llm: BaseChatModel):
    graph = StateGraph(AgentState)
    graph.add_node("classify", classify_node(llm))
    graph.add_node("search", search_node(llm))
    graph.add_node("answer", answer_node(llm))

    graph.add_edge(START, "classify")
    graph.add_conditional_edges(
        "classify",
        route_after_classify,
        {"search": "search", "answer": "answer"},
    )
    graph.add_edge("search", "answer")
    graph.add_edge("answer", END)

    return graph.compile()


def invoke(question: str, llm: BaseChatModel) -> AgentState:
    agent = build_graph(llm)
    return agent.invoke({"question": question, "search_results": [], "searched": False})
