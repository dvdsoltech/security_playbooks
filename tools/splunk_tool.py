from __future__ import annotations

import os

from tools.base_tool import SecurityTool, ToolResult


class SplunkTool(SecurityTool):
    """Wrapper for Splunk API and MCP-backed queries.

    The design supports both:
    - API calls to update kvstore collections for audit/review records
    - MCP-driven queries for search, investigation, and correlation
    """

    def __init__(self):
        super().__init__(
            name="splunk",
            base_url=os.getenv("SPLUNK_API_URL"),
        )
        self.username = os.getenv("SPLUNK_USERNAME")
        self.password = os.getenv("SPLUNK_PASSWORD")
        self.mcp_endpoint = os.getenv("SPLUNK_MCP_ENDPOINT")

    async def execute(self, *args, **kwargs) -> ToolResult:
        return ToolResult(
            success=True,
            data={
                "mode": "api_or_mcp",
                "api_url": self.base_url,
                "mcp_endpoint": self.mcp_endpoint,
                "note": "Use Splunk API for kvstore updates and reviews, and MCP for investigative queries.",
            },
            message="Splunk tool initialized.",
        )
