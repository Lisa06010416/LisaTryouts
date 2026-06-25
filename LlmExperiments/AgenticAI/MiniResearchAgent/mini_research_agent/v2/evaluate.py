from __future__ import annotations

import argparse

from mini_research_agent.common.config import load_settings
from mini_research_agent.common.evaluators import (
    clarification_accuracy,
    reflection_quality,
    routing_accuracy,
)
from mini_research_agent.common.llm import create_llm
from mini_research_agent.v2.agent import invoke

EXAMPLES = [
    {
        "inputs": {"question": "What is 2 + 2?"},
        "outputs": {"searched": False, "interrupted": False},
    },
    {
        "inputs": {"question": "Latest AI news today?"},
        "outputs": {"searched": True, "interrupted": False},
    },
]


def run_local_evaluation(use_real: bool = False) -> list[dict[str, object]]:
    settings = load_settings()
    llm = create_llm(settings, use_real=use_real)
    rows = []
    for index, example in enumerate(EXAMPLES):
        output = invoke(example["inputs"]["question"], llm, thread_id=f"eval-{index}")
        route_score = routing_accuracy(output, example["outputs"])
        clarify_score = clarification_accuracy(output, example["outputs"])
        reflection_score = reflection_quality(output, example["outputs"])
        rows.append(
            {
                "question": example["inputs"]["question"],
                "searched": output.get("searched"),
                "routing_score": route_score["score"],
                "clarification_score": clarify_score["score"],
                "reflection_score": reflection_score["score"],
            }
        )
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate the V2 mini research agent.")
    parser.add_argument("--real", action="store_true")
    args = parser.parse_args()

    for row in run_local_evaluation(use_real=args.real):
        print(row)


if __name__ == "__main__":
    main()
