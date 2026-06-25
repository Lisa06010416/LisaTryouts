from __future__ import annotations

import argparse
import re
import uuid
from typing import Any

from langfuse import Evaluation, get_client
from langgraph.types import Command

from lang_stack_research_agent.common.config import load_settings
from lang_stack_research_agent.common.llm import create_llm
from lang_stack_research_agent.v2.agent import build_graph

EXAMPLES = [
    {
        "input": {"question": "What is 2 + 2?"},
        "expected_output": {
            "searched": False,
            "interrupted": False,
            "reference_answer": "2 + 2 = 4.",
            "acceptable_substrings": ["4"],
            "requires_grounding": False,
        },
        "metadata": {"case": "direct-answer"},
    },
    {
        "input": {"question": "Latest AI news today?"},
        "expected_output": {
            "searched": True,
            "interrupted": False,
            "reference_answer": "AI providers are focusing on agent reliability, evaluation, and observability.",
            "acceptable_substrings": ["agent reliability", "evaluation", "observability"],
            "requires_grounding": True,
        },
        "metadata": {"case": "fresh-search"},
    },
    {
        "input": {"question": "Who is the CEO of Apple?"},
        "expected_output": {
            "searched": True,
            "interrupted": False,
            "reference_answer": "Apple's CEO is Tim Cook.",
            "acceptable_substrings": ["tim cook"],
            "requires_grounding": True,
        },
        "metadata": {"case": "fresh-company-fact"},
    },
    {
        "input": {
            "question": "Help me with it",
            "clarification_reply": "Please answer: What is 2 + 2?",
        },
        "expected_output": {
            "searched": False,
            "interrupted": True,
            "reference_answer": "2 + 2 = 4.",
            "acceptable_substrings": ["4"],
            "requires_grounding": False,
        },
        "metadata": {"case": "clarification"},
    },
]


def run_agent_case(*, item: dict[str, Any], use_real: bool = False) -> dict[str, Any]:
    settings = load_settings()
    llm = create_llm(settings, use_real=use_real)
    agent = build_graph(llm)
    config = {"configurable": {"thread_id": f"v3-eval-{uuid.uuid4()}"}}
    input_data = item["input"]

    result = agent.invoke(
        {
            "question": input_data["question"],
            "search_results": [],
            "searched": False,
            "messages": [],
            "retry_count": 0,
            "interrupted": False,
        },
        config=config,
    )

    if "__interrupt__" in result and input_data.get("clarification_reply"):
        result = agent.invoke(Command(resume=input_data["clarification_reply"]), config=config)

    return dict(result)


def routing_accuracy_evaluator(*, output: dict[str, Any], expected_output: dict[str, Any], **kwargs: Any) -> Evaluation:
    expected = expected_output["searched"]
    actual = output.get("searched", False)
    return Evaluation(
        name="routing_accuracy",
        value=actual == expected,
        data_type="BOOLEAN",
        comment=f"expected searched={expected}, got searched={actual}",
    )


def answer_correctness_evaluator(*, output: dict[str, Any], expected_output: dict[str, Any], **kwargs: Any) -> Evaluation:
    answer = normalize_text(output.get("answer", ""))
    acceptable = [normalize_text(text) for text in expected_output.get("acceptable_substrings", [])]
    matched = [text for text in acceptable if text and text in answer]
    return Evaluation(
        name="answer_correctness",
        value=1.0 if matched else 0.0,
        data_type="NUMERIC",
        comment="Matched expected answer signal." if matched else "No expected answer signal found.",
    )


def faithfulness_evaluator(*, output: dict[str, Any], expected_output: dict[str, Any], **kwargs: Any) -> Evaluation:
    if not expected_output.get("requires_grounding", False):
        return Evaluation(
            name="faithfulness_groundedness",
            value=1.0,
            data_type="NUMERIC",
            comment="No external grounding required for this case.",
        )

    answer_terms = content_terms(output.get("answer", ""))
    evidence_terms = content_terms(" ".join(output.get("search_results", [])))
    overlap = answer_terms & evidence_terms
    score = min(1.0, len(overlap) / 3)
    return Evaluation(
        name="faithfulness_groundedness",
        value=score,
        data_type="NUMERIC",
        comment=f"overlap_terms={sorted(overlap)}",
    )


def clarification_accuracy_evaluator(*, output: dict[str, Any], expected_output: dict[str, Any], **kwargs: Any) -> Evaluation:
    expected = expected_output["interrupted"]
    actual = output.get("interrupted", False)
    return Evaluation(
        name="clarification_accuracy",
        value=actual == expected,
        data_type="BOOLEAN",
        comment=f"expected interrupted={expected}, got interrupted={actual}",
    )


def reflection_quality_evaluator(*, output: dict[str, Any], **kwargs: Any) -> Evaluation:
    critique = output.get("critique", "")
    has_signal = len(critique.strip()) >= 12
    return Evaluation(
        name="reflection_quality",
        value=has_signal,
        data_type="BOOLEAN",
        comment="Critique contains useful signal." if has_signal else "Critique is too thin.",
    )


def run_local_evaluation(use_real: bool = False) -> list[dict[str, Any]]:
    rows = []
    evaluators = [
        routing_accuracy_evaluator,
        answer_correctness_evaluator,
        faithfulness_evaluator,
        clarification_accuracy_evaluator,
        reflection_quality_evaluator,
    ]
    for example in EXAMPLES:
        output = run_agent_case(item=example, use_real=use_real)
        evaluations = [
            evaluator(
                input=example["input"],
                output=output,
                expected_output=example["expected_output"],
                metadata=example.get("metadata", {}),
            )
            for evaluator in evaluators
        ]
        rows.append(
            {
                "case": example["metadata"]["case"],
                "answer": output.get("answer"),
                "scores": {evaluation.name: evaluation.value for evaluation in evaluations},
            }
        )
    return rows


def run_langfuse_experiment(use_real: bool = False) -> Any:
    langfuse = get_client()

    def task(*, item: dict[str, Any], **kwargs: Any) -> dict[str, Any]:
        return run_agent_case(item=item, use_real=use_real)

    return langfuse.run_experiment(
        name="LangStack Research Agent V3",
        run_name="v3-langfuse-evaluation",
        description="Evaluate routing, correctness, groundedness, clarification, and reflection.",
        data=EXAMPLES,
        task=task,
        evaluators=[
            routing_accuracy_evaluator,
            answer_correctness_evaluator,
            faithfulness_evaluator,
            clarification_accuracy_evaluator,
            reflection_quality_evaluator,
        ],
        max_concurrency=1,
        metadata={"agent_version": "v3", "mode": "real" if use_real else "mock"},
    )


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower()).strip()


def content_terms(text: str) -> set[str]:
    stopwords = {
        "the",
        "and",
        "or",
        "is",
        "are",
        "a",
        "an",
        "of",
        "to",
        "in",
        "on",
        "with",
        "that",
        "this",
        "according",
        "provided",
    }
    return {
        word
        for word in re.findall(r"[a-zA-Z][a-zA-Z\-]{3,}", text.lower())
        if word not in stopwords
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Run V3 Langfuse-style evaluations.")
    parser.add_argument("--real", action="store_true")
    parser.add_argument("--langfuse", action="store_true", help="Send experiment traces and scores to Langfuse.")
    args = parser.parse_args()

    if args.langfuse:
        result = run_langfuse_experiment(use_real=args.real)
        print(result.format())
        return

    for row in run_local_evaluation(use_real=args.real):
        print(row)


if __name__ == "__main__":
    main()
