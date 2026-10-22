from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from langchain_core.messages import AIMessage, BaseMessage


class BaseModelProvider(ABC):
    """Abstract interface for model backends used by the multi-agent workflow."""

    name: str

    @abstractmethod
    def initialize(self) -> None:
        """Initialize any provider-specific client or configuration."""

    @abstractmethod
    async def invoke(self, system_prompt: str, user_message: str, **kwargs: Any) -> AIMessage:
        """Send a prompt to the configured LLM backend and return a LangChain AIMessage."""

    @abstractmethod
    async def invoke_messages(self, messages: list[BaseMessage], **kwargs: Any) -> AIMessage:
        """Send a list of chat messages to the LLM backend and return a LangChain AIMessage."""
