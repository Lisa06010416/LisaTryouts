from __future__ import annotations

import re
from typing import Any, TypeVar

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage, BaseMessage
from langchain_core.outputs import ChatGeneration, ChatResult
from langchain_core.runnables import RunnableLambda
from pydantic import BaseModel

from mini_research_agent.common.config import Settings

StructuredModel = TypeVar("StructuredModel", bound=BaseModel)


class MockChatModel(BaseChatModel):
    """Small deterministic model for local graph tests and API-free demos."""

    @property
    def _llm_type(self) -> str:
        return "mock-chat-model"

    def _generate(
        self,
        messages: list[BaseMessage],
        stop: list[str] | None = None,
        run_manager: Any | None = None,
        **kwargs: Any,
    ) -> ChatResult:
        prompt = "\n".join(message.content for message in messages)
        return ChatResult(generations=[ChatGeneration(message=AIMessage(content=self._answer(prompt)))])

    def _answer(self, prompt: str) -> str:
        lower_prompt = prompt.lower()
        if "latest ai news" in lower_prompt:
            return "Current AI news changes quickly, so I would search before answering."
        if "ceo of apple" in lower_prompt:
            return "Apple's CEO is Tim Cook. This fact should still be checked when freshness matters."
        if "2 + 2" in lower_prompt or "2+2" in lower_prompt:
            return "2 + 2 = 4."
        if "critique" in lower_prompt or "judge" in lower_prompt:
            return "The answer is grounded enough for this demo."
        return "This is a concise mock answer based on the available context."

    def with_structured_output(
        self,
        schema: type[StructuredModel],
        **kwargs: Any,
    ) -> Any:
        def invoke(input_value: Any) -> StructuredModel:
            text = _latest_human_text(input_value).lower()
            needs_search = any(
                phrase in text
                for phrase in ("latest", "today", "current", "news", "ceo", "recent", "2026")
            )
            is_ambiguous = any(
                re.search(pattern, text)
                for pattern in (r"\bit\b", r"\bthis\b", r"\bthat thing\b", r"\bhelp me with it\b")
            )

            payload: dict[str, Any] = {}
            for name in schema.model_fields:
                if name == "needs_search":
                    payload[name] = needs_search
                elif name == "is_ambiguous":
                    payload[name] = is_ambiguous
                elif name == "reason":
                    payload[name] = "Fresh or time-sensitive questions need search." if needs_search else "The question can be answered directly."
                elif name == "ok":
                    payload[name] = True
                elif name == "critique":
                    payload[name] = "The answer is sufficiently grounded for this demo."
                else:
                    payload[name] = None
            return schema(**payload)

        return RunnableLambda(invoke)

    def bind_tools(self, tools: Any, **kwargs: Any) -> "MockChatModel":
        return self


def create_llm(settings: Settings, use_real: bool = False) -> BaseChatModel:
    if use_real:
        if not settings.openai_api_key:
            raise RuntimeError("OPENAI_API_KEY is required when --real is used.")

        from langchain_openai import ChatOpenAI

        return ChatOpenAI(model=settings.model, temperature=0)

    return MockChatModel()


def _latest_human_text(input_value: Any) -> str:
    messages = getattr(input_value, "messages", None)
    if messages:
        for message in reversed(messages):
            if getattr(message, "type", None) == "human":
                return str(message.content)
        return str(messages[-1].content)
    return str(input_value)
