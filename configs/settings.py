from __future__ import annotations

import os


def get_runtime_settings() -> dict[str, str]:
    return {
        "MODEL_PROVIDER": os.getenv("MODEL_PROVIDER", "ollama"),
        "OLLAMA_MODEL": os.getenv("OLLAMA_MODEL", "llama3.1"),
        "OLLAMA_BASE_URL": os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
        "AZURE_OPENAI_DEPLOYMENT": os.getenv("AZURE_OPENAI_DEPLOYMENT", ""),
        "AZURE_OPENAI_ENDPOINT": os.getenv("AZURE_OPENAI_ENDPOINT", ""),
        "AZURE_OPENAI_API_KEY": os.getenv("AZURE_OPENAI_API_KEY", ""),
    }
