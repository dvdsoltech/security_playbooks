from __future__ import annotations

import os

from tools.base_tool import SecurityTool, ToolResult


class MixmodeTool(SecurityTool):
    """Wrapper for Mixmode log queries and event searches."""

    def __init__(self):
        super().__init__(
            name="mixmode",
            base_url=os.getenv("MIXMODE_API_URL"),
        )
        self.api_key = os.getenv("MIXMODE_API_KEY")
        self.tenant_id = os.getenv("MIXMODE_TENANT_ID")

    async def execute(self, *args, **kwargs) -> ToolResult:
        return ToolResult(
            success=True,
            data={
                "mode": "api",
                "api_url": self.base_url,
                "tenant_id": self.tenant_id,
                "note": "Use Mixmode API for log querying and event analysis.",
            },
            message="Mixmode tool initialized.",
        )
