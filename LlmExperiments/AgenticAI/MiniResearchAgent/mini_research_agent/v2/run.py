from __future__ import annotations

import argparse
import uuid

from langgraph.types import Command

from mini_research_agent.common.config import load_settings
from mini_research_agent.common.llm import create_llm
from mini_research_agent.v2.agent import build_graph


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the V2 mini research agent.")
    parser.add_argument("question", nargs="?", default="Latest AI news today?")
    parser.add_argument("--real", action="store_true", help="Use ChatOpenAI instead of the deterministic mock model.")
    args = parser.parse_args()

    settings = load_settings()
    llm = create_llm(settings, use_real=args.real)
    agent = build_graph(llm)
    config = {"configurable": {"thread_id": f"cli-{uuid.uuid4()}"}}
    result = agent.invoke(
        {
            "question": args.question,
            "search_results": [],
            "searched": False,
            "messages": [],
            "retry_count": 0,
            "interrupted": False,
        },
        config=config,
    )

    if "__interrupt__" in result:
        prompt = result["__interrupt__"][0].value["question"]
        user_reply = input(f"{prompt}\n> ")
        result = agent.invoke(Command(resume=user_reply), config=config)

    print(f"Question: {result['question']}")
    print(f"Needs search: {result.get('needs_search')}")
    print(f"Searched: {result.get('searched')}")
    print(f"Critique: {result.get('critique')}")
    print(f"Answer: {result.get('answer')}")


if __name__ == "__main__":
    main()
