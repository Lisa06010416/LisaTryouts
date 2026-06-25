from __future__ import annotations

from typing import Literal

from langchain_core.language_models.chat_models import BaseChatModel
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph

from mini_research_agent.v2.nodes import (
    clarify_node,
    classify_node,
    reflect_node,
    search_node,
    synthesize_node,
)
from mini_research_agent.v2.state import AgentState


def route_after_classify(state: AgentState) -> Literal["clarify", "search", "synthesize"]:
    if state.get("is_ambiguous"):
        return "clarify"
    if state.get("needs_search"):
        return "search"
    return "synthesize"


def route_after_reflect(state: AgentState) -> Literal["search", "end"]:
    if not state.get("reflection_ok", True) and state.get("retry_count", 0) < 2:
        return "search"
    return "end"


def build_graph(llm: BaseChatModel):
    graph = StateGraph(AgentState)
    graph.add_node("classify", classify_node(llm))
    graph.add_node("clarify", clarify_node(llm))
    graph.add_node("search", search_node(llm))
    graph.add_node("synthesize", synthesize_node(llm))
    graph.add_node("reflect", reflect_node(llm))

    graph.add_edge(START, "classify")
    graph.add_conditional_edges(
        "classify",
        route_after_classify,
        {"clarify": "clarify", "search": "search", "synthesize": "synthesize"},
    )
    graph.add_edge("clarify", "classify")
    graph.add_edge("search", "synthesize")
    graph.add_edge("synthesize", "reflect")
    graph.add_conditional_edges("reflect", route_after_reflect, {"search": "search", "end": END})

    return graph.compile(checkpointer=MemorySaver())


def invoke(question: str, llm: BaseChatModel, thread_id: str = "demo-thread") -> AgentState:
    agent = build_graph(llm)
    config = {"configurable": {"thread_id": thread_id}}
    return agent.invoke(
        {
            "question": question,
            "search_results": [],
            "searched": False,
            "messages": [],
            "retry_count": 0,
            "interrupted": False,
        },
        config=config,
    )
