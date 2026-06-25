from __future__ import annotations

import argparse

from lang_stack_research_agent.common.config import load_settings
from lang_stack_research_agent.common.evaluators import routing_accuracy
from lang_stack_research_agent.common.llm import create_llm
from lang_stack_research_agent.v1.agent import invoke

EXAMPLES = [
    {
        "inputs": {"question": "What is 2 + 2?"},
        "outputs": {"searched": False},
    },
    {
        "inputs": {"question": "Latest AI news today?"},
        "outputs": {"searched": True},
    },
    {
        "inputs": {"question": "Who is the CEO of Apple?"},
        "outputs": {"searched": True},
    },
]


def run_local_evaluation(use_real: bool = False) -> list[dict[str, object]]:
    settings = load_settings()
    llm = create_llm(settings, use_real=use_real)
    rows = []
    for example in EXAMPLES:
        output = invoke(example["inputs"]["question"], llm)
        score = routing_accuracy(output, example["outputs"])
        rows.append(
            {
                "question": example["inputs"]["question"],
                "searched": output.get("searched"),
                "score": score["score"],
                "comment": score["comment"],
            }
        )
    return rows


def run_langsmith_evaluation(use_real: bool = False) -> None:
    from langsmith import Client, evaluate

    settings = load_settings()
    llm = create_llm(settings, use_real=use_real)
    client = Client()
    dataset_name = "lang-stack-research-agent-v1"

    if not client.has_dataset(dataset_name=dataset_name):
        dataset = client.create_dataset(dataset_name=dataset_name)
        client.create_examples(dataset_id=dataset.id, examples=EXAMPLES)

    evaluate(
        lambda inputs: invoke(inputs["question"], llm),
        data=dataset_name,
        evaluators=[lambda outputs, reference_outputs: routing_accuracy(outputs, reference_outputs)],
        experiment_prefix="v1",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate the V1 lang stack research agent.")
    parser.add_argument("--real", action="store_true")
    parser.add_argument("--langsmith", action="store_true")
    args = parser.parse_args()

    if args.langsmith:
        run_langsmith_evaluation(use_real=args.real)
        return

    for row in run_local_evaluation(use_real=args.real):
        print(row)


if __name__ == "__main__":
    main()
