from __future__ import annotations

import os

from langchain_core.tools import tool


@tool
def web_search(query: str) -> str:
    """Search the web for current information."""
    api_key = os.getenv("TAVILY_API_KEY")
    if api_key:
        from tavily import TavilyClient

        client = TavilyClient(api_key=api_key)
        response = client.search(query=query, max_results=3)
        snippets = [
            f"{item.get('title', 'Untitled')}: {item.get('content', '')}"
            for item in response.get("results", [])
        ]
        return "\n".join(snippets)

    return mock_search(query)


def mock_search(query: str) -> str:
    normalized = query.lower()
    if "ai" in normalized and ("latest" in normalized or "news" in normalized):
        return (
            "Mock AI News: Frontier model providers are focusing on agent reliability, "
            "evaluation, and observability."
        )
    if "ceo of apple" in normalized or "apple" in normalized:
        return "Mock Company Fact: Apple CEO is Tim Cook."
    return f"Mock Search Result: No live API configured. Query was: {query}"
