# Multi-Agent Function Calling Experiment

## Purpose

This experiment demonstrates a simple multi-agent system using ChatGPT API with function calling capabilities. It implements a basic agent that can call functions to perform tasks like calculating sums or fetching mock data.

## Setup

1. Install dependencies using UV:
   ```bash
   uv sync
   ```

2. Set up your OpenAI API key and LangSmith API key in a `.env` file:
   ```
   OPENAI_API_KEY=your_api_key_here
   LANGCHAIN_API_KEY=your_langsmith_api_key_here
   ```

## Usage

### Original OpenAI Version
Run the main script:
```bash
uv run python main.py
```

### LangChain Version
Run the LangChain-based script:
```bash
uv run python langchain_main.py
```

Both scripts will simulate a conversation where the agent uses function calling to perform calculations.

### Monitoring with LangSmith
The LangChain version includes LangSmith tracing for monitoring and debugging:

1. After running `langchain_main.py`, visit [LangSmith Dashboard](https://smith.langchain.com/) to view the execution traces.
2. You can see the agent's decision-making process, tool calls, and responses in detail.
3. Make sure your `LANGCHAIN_API_KEY` is set in the `.env` file.

## Structure

- `main.py`: Main script implementing the multi-agent system with direct OpenAI API function calling.
- `langchain_main.py`: Alternative implementation using LangChain framework for agent orchestration.
- `pyproject.toml`: Project dependencies managed by UV.
- `README.md`: This file.

## Notes

This is a minimal implementation for experimentation purposes. The OpenAI direct version now includes a coordinator/subagent delegation flow, and the LangChain version uses a dedicated worker subagent agent. Both can call predefined functions like `add_numbers` and `get_weather`.