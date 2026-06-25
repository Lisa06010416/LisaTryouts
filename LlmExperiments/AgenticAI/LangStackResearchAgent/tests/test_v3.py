from lang_stack_research_agent.v3.evaluate import run_local_evaluation


def test_v3_langfuse_style_evaluators_score_expected_cases():
    rows = run_local_evaluation()

    assert len(rows) == 4
    assert all("routing_accuracy" in row["scores"] for row in rows)
    assert all("answer_correctness" in row["scores"] for row in rows)
    assert all("faithfulness_groundedness" in row["scores"] for row in rows)
    assert all("clarification_accuracy" in row["scores"] for row in rows)
    assert all("reflection_quality" in row["scores"] for row in rows)
    assert rows[0]["scores"]["routing_accuracy"] is True
