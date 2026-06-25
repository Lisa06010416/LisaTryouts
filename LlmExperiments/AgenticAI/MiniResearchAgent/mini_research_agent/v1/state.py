from __future__ import annotations

from typing_extensions import TypedDict


class AgentState(TypedDict, total=False):
    question: str
    search_results: list[str]
    answer: str
    needs_search: bool
    searched: bool
    route_reason: str
