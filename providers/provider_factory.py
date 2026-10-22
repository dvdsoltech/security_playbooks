from __future__ import annotations

import os

MODEL_PROVIDER = os.getenv("MODEL_PROVIDER")
if MODEL_PROVIDER is None:
    raise RuntimeError(
        "MODEL_PROVIDER must be set to one of: ollama, foundry, vllm."
    )

MODEL_PROVIDER = MODEL_PROVIDER.lower()

if MODEL_PROVIDER == "ollama":
    from providers.ollama_provider import OllamaProvider
    PROVIDER_CLASS = OllamaProvider
elif MODEL_PROVIDER == "foundry":
    from providers.foundry_provider import FoundryProvider
    PROVIDER_CLASS = FoundryProvider
elif MODEL_PROVIDER == "vllm":
    from providers.vllm_provider import VLLMProvider
    PROVIDER_CLASS = VLLMProvider
else:
    raise ValueError(f"Unsupported MODEL_PROVIDER: {MODEL_PROVIDER}")


def create_model_provider() -> object:
    return PROVIDER_CLASS()
