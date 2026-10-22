from __future__ import annotations

import os
from typing import Any

from langchain_core.messages import AIMessage, BaseMessage

from providers.base_provider import BaseModelProvider


class FoundryProvider(BaseModelProvider):
    """Microsoft Foundry / Azure AI inference provider for deployed environments."""

    name = "foundry"

    def __init__(self, deployment: str | None = None, endpoint: str | None = None, api_key: str | None = None):
        self.deployment = deployment or os.getenv("AZURE_OPENAI_DEPLOYMENT", "")
        self.endpoint = endpoint or os.getenv("AZURE_OPENAI_ENDPOINT", "")
        self.api_key = api_key or os.getenv("AZURE_OPENAI_API_KEY", "")
        self.client = None

    def initialize(self) -> None:
        try:
            from openai import AzureOpenAI
        except ImportError as exc:  # pragma: no cover
            raise RuntimeError("openai package is required for Foundry support.") from exc

        if not self.endpoint or not self.api_key:
            raise RuntimeError("AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_API_KEY must be set for Foundry mode.")

        self.client = AzureOpenAI(
            api_key=self.api_key,
            api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-01"),
            azure_endpoint=self.endpoint,
        )

    def _to_ai_message(self, message: Any) -> AIMessage:
        tool_calls = []
        if getattr(message, "tool_calls", None):
            for call in message.tool_calls:
                tool_calls.append(
                    {
                        "name": call.function.name,
                        "args": call.function.arguments if isinstance(call.function.arguments, dict) else json.loads(call.function.arguments),
                        "id": call.id,
                    }
                )

        return AIMessage(
            content=message.content or "",
            tool_calls=tool_calls,
        )
    
    async def invoke(self, system_prompt: str, user_message: str, **kwargs: Any) -> AIMessage:
        if self.client is None:
            self.initialize()

        response = self.client.chat.completions.create(
            model=self.deployment,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
            **kwargs,
        )
        return self._to_ai_message(response.choices[0].message)

    async def invoke_messages(self, messages: list[BaseMessage], **kwargs: Any) -> AIMessage:
        if self.client is None:
            self.initialize()

        response = self.client.chat.completions.create(
            model=self.deployment,
            messages=[{"role": m.type, "content": m.content} for m in messages],
            **kwargs,
        )
        return self._to_ai_message(response.choices[0].message)
