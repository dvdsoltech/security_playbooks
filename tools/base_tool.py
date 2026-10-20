from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ToolResult:
    success: bool
    data: dict | list | None = None
    message: str | None = None
    metadata: dict | None = None


class SecurityTool:
    """Base tool wrapper for external security integrations."""

    def __init__(self, name: str, base_url: str | None = None):
        self.name = name
        self.base_url = base_url

    async def execute(self, *args, **kwargs) -> ToolResult:
        raise NotImplementedError("Subclasses must implement execute().")
