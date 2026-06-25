from mini_research_agent.common.config import load_settings
from mini_research_agent.common.llm import create_llm
from mini_research_agent.v2.agent import invoke


def test_v2_direct_question_completes_with_reflection():
    llm = create_llm(load_settings())
    result = invoke("What is 2 + 2?", llm, thread_id="test-direct")

    assert result["searched"] is False
    assert result["critique"]
    assert "4" in result["answer"]


def test_v2_fresh_question_searches_then_reflects():
    llm = create_llm(load_settings())
    result = invoke("Latest AI news today?", llm, thread_id="test-search")

    assert result["searched"] is True
    assert result["critique"]
    assert result["search_results"]
