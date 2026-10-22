from __future__ import annotations

import os
from typing import Any

import httpx

from tools.base_tool import SecurityTool, ToolResult


class MixmodeTool(SecurityTool):
    """Wrapper for Mixmode log queries and event searches."""

    def __init__(self):
        super().__init__(
            name="mixmode",
            base_url=os.getenv("MIXMODE_API_URL"),
        )
        self.api_key = os.getenv("MIXMODE_API_KEY")
        self.session = None

    @staticmethod
    def tool_schema() -> dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "mixmode_log_query",
                "description": "Execute a Mixmode PQL query and return log results.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The Mixmode PQL query string. Time ranges are often included directly in the query.",
                        },
                        "timezone": {
                            "type": "string",
                            "description": "Optional timezone for parsing date/time statements.",
                        },
                        "context": {
                            "type": "array",
                            "items": {"type": "integer"},
                            "description": "Optional list of sensor IDs to constrain the query.",
                        },
                    },
                    "required": ["query"],
                },
            },
        }

    async def execute(
        self,
        query: str,
        timezone: str | None = None,
        context: list[int] | None = None,
        **kwargs: Any,
    ) -> ToolResult:
        if not self.api_key:
            return ToolResult(
                success=False,
                data={},
                message="MIXMODE_API_KEY is not configured.",
            )

        if not self.base_url:
            return ToolResult(
                success=False,
                data={},
                message="MIXMODE_API_URL is not configured.",
            )

        params = {"query": query}
        if timezone:
            params["timezone"] = timezone
        if context is not None:
            params["context"] = context

        try:
            if self.session is None:
                self.session = httpx.AsyncClient(
                    headers={"x-mixmode-api-token": self.api_key},
                    timeout=60.0,
                )

            response = await self.session.post(
                self.base_url.rstrip("/") + "/logs/search",
                json=params,
            )
            response.raise_for_status()

            return ToolResult(
                success=True,
                data=response.json(),
                message="Mixmode query executed successfully.",
            )
        except Exception as exc:
            return ToolResult(
                success=False,
                data={"query": query, "timezone": timezone, "context": context},
                message=f"Mixmode query failed: {exc}",
            )
