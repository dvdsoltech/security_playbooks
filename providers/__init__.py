from __future__ import annotations

import os

from providers.foundry_provider import FoundryProvider
from providers.ollama_provider import OllamaProvider


def get_model_provider() -> object:
    provider_name = os.getenv("MODEL_PROVIDER", "ollama").lower()

    if provider_name == "foundry":
        return FoundryProvider()
    if provider_name == "ollama":
        return OllamaProvider()

    raise ValueError(f"Unsupported MODEL_PROVIDER: {provider_name}")


def get_provider_name() -> str:
    return os.getenv("MODEL_PROVIDER", "ollama").lower()
