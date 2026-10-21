from __future__ import annotations

import os
from typing import Any

from providers.base_provider import BaseModelProvider


class OllamaProvider(BaseModelProvider):
    """Local inference provider for Ollama-based experimentation and local development."""

    name = "ollama"

    def __init__(self, model: str | None = None, base_url: str | None = None):
        self.model = model or os.getenv("OLLAMA_MODEL", "llama3.1")
        self.base_url = base_url or os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        self.client = None

    def initialize(self) -> None:
        try:
            import httpx
        except ImportError as exc:  # pragma: no cover
            raise RuntimeError("httpx is required for Ollama support.") from exc
        self.client = httpx.Client(base_url=self.base_url, timeout=120.0)

    async def invoke(self, system_prompt: str, user_message: str, **kwargs: Any) -> str:
        if self.client is None:
            self.initialize()

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
            **kwargs,
        }
        response = self.client.post("/api/chat", json=payload)
        response.raise_for_status()
        data = response.json()
        return data.get("message", {}).get("content", "")

    async def invoke_messages(self, messages: list[dict[str, str]], **kwargs: Any) -> str:
        if self.client is None:
            self.initialize()

        payload = {
            "model": self.model,
            "messages": messages,
            **kwargs,
        }
        response = self.client.post("/api/chat", json=payload)
        response.raise_for_status()
        data = response.json()
        return data.get("message", {}).get("content", "")
