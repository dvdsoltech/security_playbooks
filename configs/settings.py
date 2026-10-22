from __future__ import annotations

import os


def get_runtime_settings() -> dict[str, str]:
    return {
        # Provider selection
        "MODEL_PROVIDER": os.getenv("MODEL_PROVIDER", "ollama"),
        "MODEL_NAME": os.getenv("MODEL_NAME", ""),
        "MODEL_API_KEY": os.getenv("MODEL_API_KEY", ""),
        "MODEL_API_BASE_URL": os.getenv("MODEL_API_BASE_URL", ""),

        # Ollama
        "OLLAMA_MODEL": os.getenv("OLLAMA_MODEL", "llama3.1"),
        "OLLAMA_BASE_URL": os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),

        # Azure / Foundry-style model config
        "AZURE_OPENAI_DEPLOYMENT": os.getenv("AZURE_OPENAI_DEPLOYMENT", ""),
        "AZURE_OPENAI_ENDPOINT": os.getenv("AZURE_OPENAI_ENDPOINT", ""),
        "AZURE_OPENAI_API_KEY": os.getenv("AZURE_OPENAI_API_KEY", ""),
        "AZURE_OPENAI_API_VERSION": os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-01"),

        # Foundry / generic cloud model config
        "FOUNDRY_MODEL": os.getenv("FOUNDRY_MODEL", ""),
        "FOUNDRY_ENDPOINT": os.getenv("FOUNDRY_ENDPOINT", ""),
        "FOUNDRY_API_KEY": os.getenv("FOUNDRY_API_KEY", ""),
        "FOUNDRY_API_VERSION": os.getenv("FOUNDRY_API_VERSION", "2024-02-01"),

        # VLLM / self-hosted model config
        "VLLM_ENDPOINT": os.getenv("VLLM_ENDPOINT", ""),
        "VLLM_MODEL": os.getenv("VLLM_MODEL", ""),

        # Splunk MCP
        "SPLUNK_MCP_ENDPOINT": os.getenv("SPLUNK_MCP_ENDPOINT", ""),
        "SPLUNK_MCP_TOKEN": os.getenv("SPLUNK_MCP_TOKEN", ""),
        "SPLUNK_MCP_SERVER_NAME": os.getenv("SPLUNK_MCP_SERVER_NAME", "splunk-mcp-server"),

        # Splunk API
        "SPLUNK_API_BASE_URL": os.getenv("SPLUNK_API_BASE_URL", ""),
        "SPLUNK_API_TOKEN": os.getenv("SPLUNK_API_TOKEN", ""),

        # Mixmode
        "MIXMODE_API_URL": os.getenv("MIXMODE_API_URL", "https://api.mixmode.ai"),
        "MIXMODE_API_KEY": os.getenv("MIXMODE_API_KEY", ""),

        # App runtime
        "SECURITY_PLAYBOOKS_ENV": os.getenv("SECURITY_PLAYBOOKS_ENV", "development"),
        "LOG_LEVEL": os.getenv("LOG_LEVEL", "INFO"),
    }
