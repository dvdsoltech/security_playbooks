from __future__ import annotations

import os

MODEL_PROVIDER = os.getenv("MODEL_PROVIDER", "ollama").lower()

if MODEL_PROVIDER == "ollama":
    from providers.ollama_provider import OllamaProvider
    PROVIDER_CLASS = OllamaProvider
elif MODEL_PROVIDER == "foundry":
    from providers.foundry_provider import FoundryProvider
    PROVIDER_CLASS = FoundryProvider
else:
    raise ValueError(f"Unsupported MODEL_PROVIDER: {MODEL_PROVIDER}")


def create_model_provider() -> object:
    return PROVIDER_CLASS()
