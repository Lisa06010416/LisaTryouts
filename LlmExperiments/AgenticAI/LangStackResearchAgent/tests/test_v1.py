from lang_stack_research_agent.common.config import load_settings
from lang_stack_research_agent.common.llm import create_llm
from lang_stack_research_agent.v1.agent import invoke


def test_v1_routes_direct_question_without_search():
    llm = create_llm(load_settings())
    result = invoke("What is 2 + 2?", llm)

    assert result["searched"] is False
    assert "4" in result["answer"]


def test_v1_routes_fresh_question_to_search():
    llm = create_llm(load_settings())
    result = invoke("Latest AI news today?", llm)

    assert result["searched"] is True
    assert result["search_results"]
