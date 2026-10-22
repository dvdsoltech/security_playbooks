from __future__ import annotations

import os
from typing import Any

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

    async def invoke(self, system_prompt: str, user_message: str, **kwargs: Any) -> str:
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
        return response.choices[0].message.content

    async def invoke_messages(self, messages: list[dict[str, str]], **kwargs: Any) -> str:
        if self.client is None:
            self.initialize()

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            **kwargs,
        )
        return response.choices[0].message.content
