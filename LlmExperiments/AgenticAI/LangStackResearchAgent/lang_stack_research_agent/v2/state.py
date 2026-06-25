from __future__ import annotations

from langchain_core.messages import BaseMessage
from typing_extensions import TypedDict


class AgentState(TypedDict, total=False):
    question: str
    search_results: list[str]
    answer: str
    needs_search: bool
    searched: bool
    messages: list[BaseMessage]
    is_ambiguous: bool
    critique: str
    reflection_ok: bool
    retry_count: int
    interrupted: bool
    route_reason: str
