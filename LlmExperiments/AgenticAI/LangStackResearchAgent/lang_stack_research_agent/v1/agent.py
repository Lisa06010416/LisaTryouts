from __future__ import annotations

from langchain_core.language_models.chat_models import BaseChatModel

from lang_stack_research_agent.v1.nodes import answer_node, classify_node, search_node
from lang_stack_research_agent.v1.state import AgentState


def invoke(question: str, llm: BaseChatModel) -> AgentState:
    state: AgentState = {
        "question": question,
        "search_results": [],
        "searched": False,
    }

    classify = classify_node(llm)
    search = search_node(llm)
    answer = answer_node(llm)

    state.update(classify(state))
    if state.get("needs_search"):
        state.update(search(state))

    state.update(answer(state))
    return state
