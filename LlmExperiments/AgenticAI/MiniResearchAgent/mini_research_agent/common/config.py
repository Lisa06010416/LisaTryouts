from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    openai_api_key: str | None
    langchain_api_key: str | None
    langchain_project: str
    tavily_api_key: str | None
    model: str


def load_settings() -> Settings:
    load_dotenv()
    settings = Settings(
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        langchain_api_key=os.getenv("LANGCHAIN_API_KEY"),
        langchain_project=os.getenv("LANGCHAIN_PROJECT", "mini-research-agent"),
        tavily_api_key=os.getenv("TAVILY_API_KEY"),
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
    )
    configure_langsmith(settings)
    return settings


def configure_langsmith(settings: Settings) -> None:
    if not settings.langchain_api_key:
        return

    os.environ.setdefault("LANGCHAIN_API_KEY", settings.langchain_api_key)
    os.environ.setdefault("LANGSMITH_TRACING", "true")
    os.environ.setdefault("LANGCHAIN_TRACING_V2", "true")
    os.environ.setdefault("LANGCHAIN_PROJECT", settings.langchain_project)
