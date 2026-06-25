# Mini Research Agent

## Purpose

This experiment implements a small research agent to exercise the LangChain, LangGraph, and LangSmith stack end to end.

- LangChain: prompt composition, structured output, and tool binding inside agent steps.
- LangGraph: V2 typed state, conditional routing, cycles, checkpointing, and human-in-the-loop interrupts.
- LangSmith: tracing configuration plus evaluation entry points.

V1 is intentionally implemented without LangGraph as a plain Python orchestration baseline. V2 uses LangGraph to show where graph state, cycles, interrupts, and checkpointing start to pay off.

The default execution mode is deterministic mock mode, so the agent can be tested without external API calls. Set `OPENAI_API_KEY` to run with a real OpenAI chat model, and set `LANGCHAIN_API_KEY` to send traces/evaluations to LangSmith.

## Setup

```bash
uv sync
```

Optional `.env` values:

```text
OPENAI_API_KEY=your_openai_api_key
LANGCHAIN_API_KEY=your_langsmith_api_key
LANGCHAIN_PROJECT=mini-research-agent
TAVILY_API_KEY=your_tavily_api_key
```

## Usage

Run V1:

```bash
uv run python -m mini_research_agent.v1.run "Latest AI news today?"
```

Run V2:

```bash
uv run python -m mini_research_agent.v2.run "Latest AI news today?"
```

Run local smoke tests:

```bash
uv run pytest
```

Run local evaluators:

```bash
uv run python -m mini_research_agent.v1.evaluate
uv run python -m mini_research_agent.v2.evaluate
```

To run with real LLM calls:

```bash
uv run python -m mini_research_agent.v1.run --real "Who is the CEO of Apple?"
```

## Structure

- `mini_research_agent/common/`: environment, LLM factory, search tool, and evaluator helpers.
- `mini_research_agent/v1/`: basic classify -> optional search -> answer flow without LangGraph.
- `mini_research_agent/v2/`: multi-turn graph with clarification, reflection, retry cycle, and checkpointing.
- `tests/`: deterministic smoke tests for routing and agent execution.

## Notes

- The search tool uses Tavily when `TAVILY_API_KEY` is present. Otherwise it returns deterministic sample snippets for learning and tests.
- LangSmith tracing is enabled only when `LANGCHAIN_API_KEY` is present.
- LangSmith dataset-based evaluation is intentionally kept behind an explicit `--langsmith` flag because it needs a configured LangSmith workspace.
