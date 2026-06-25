from __future__ import annotations

import argparse

from mini_research_agent.common.config import load_settings
from mini_research_agent.common.llm import create_llm
from mini_research_agent.v1.agent import invoke


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the V1 mini research agent.")
    parser.add_argument("question", nargs="?", default="Latest AI news today?")
    parser.add_argument("--real", action="store_true", help="Use ChatOpenAI instead of the deterministic mock model.")
    args = parser.parse_args()

    settings = load_settings()
    llm = create_llm(settings, use_real=args.real)
    result = invoke(args.question, llm)

    print(f"Question: {result['question']}")
    print(f"Needs search: {result.get('needs_search')}")
    print(f"Searched: {result.get('searched')}")
    print(f"Answer: {result.get('answer')}")


if __name__ == "__main__":
    main()
