from __future__ import annotations

import os
from typing import Any

from tools.base_tool import SecurityTool, ToolResult


class MixmodeTool(SecurityTool):
    """Wrapper for Mixmode log queries and event searches."""

    def __init__(self):
        super().__init__(
            name="mixmode",
            base_url=os.getenv("MIXMODE_API_URL"),
        )
        self.api_key = os.getenv("MIXMODE_API_KEY")

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
                            "description": "The Mixmode PQL query string. Time ranges are commonly included directly in the query.",
                        },
                        "timezone": {
                            "type": "string",
                            "description": "Optional timezone for parsing date/time statements in the Mixmode query language.",
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

    async def execute(self, *args, **kwargs) -> ToolResult:
        return ToolResult(
            success=True,
            data={
                "mode": "api",
                "api_url": self.base_url,
                "api_key_present": bool(self.api_key),
                "note": (
                    "Use the Mixmode API to run a PQL query. "
                    "The API key is sent as the x-mixmode-api-token header."
                ),
            },
            message="Mixmode tool initialized.",
        )
