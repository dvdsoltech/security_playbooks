from __future__ import annotations

import json
import os
from typing import Any

from langchain_core.messages import AIMessage, BaseMessage

from providers.base_provider import BaseModelProvider


class VLLMProvider(BaseModelProvider):
    name = "vllm"

    def __init__(self, model: str | None = None, base_url: str | None = None, api_key: str | None = None):
        self.model = model or os.getenv("VLLM_MODEL", "meta-llama/Meta-Llama-3.1-8B-Instruct")
        self.base_url = base_url or os.getenv("VLLM_BASE_URL", "http://localhost:8000/v1")
        self.api_key = api_key or os.getenv("VLLM_API_KEY", "EMPTY")
        self.client = None

    def initialize(self) -> None:
        try:
            from openai import OpenAI
        except ImportError as exc:  # pragma: no cover
            raise RuntimeError("openai package is required for vLLM support.") from exc

        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url,
        )
        
    def _to_ai_message(self, message: Any) -> AIMessage:
        tool_calls = []
        if getattr(message, "tool_calls", None):
            for call in message.tool_calls:
                args = call.function.arguments
                if isinstance(args, str):
                    try:
                        args = json.loads(args)
                    except Exception:
                        args = {}
                tool_calls.append({
                    "name": call.function.name,
                    "args": args,
                    "id": call.id,
                })

        return AIMessage(
            content=message.content or "",
            tool_calls=tool_calls,
        )
    
    async def invoke(self, system_prompt: str, user_message: str, **kwargs: Any) -> AIMessage:
        if self.client is None:
            self.initialize()

        response = self.client.chat.completions.create(
            model=self.model,
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
            model=self.model,
            messages=[{"role": m.type, "content": m.content} for m in messages],
            **kwargs,
        )
        return self._to_ai_message(response.choices[0].message)
