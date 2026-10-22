from __future__ import annotations

import os
from typing import Any

from tools.base_tool import SecurityTool, ToolResult


class SplunkMcpTool(SecurityTool):
    """Wrapper for the Splunk remote MCP server.

    This class creates the exact config/command pattern that Splunk expects
    for mcp-remote, while still fitting the repo's tool interface.
    """

    def __init__(self):
        self.name = "splunk_mcp"
        self.endpoint = os.getenv("SPLUNK_MCP_ENDPOINT")
        self.token = os.getenv("SPLUNK_MCP_TOKEN")
        self.server_name = os.getenv("SPLUNK_MCP_SERVER_NAME", "splunk-mcp-server")
        self.base_url = self.endpoint

        if not self.endpoint:
            raise ValueError("SPLUNK_MCP_ENDPOINT is required for Splunk MCP access.")

    def as_mcp_config(self) -> dict[str, Any]:
        """Return the same JSON shape Splunk provided for an MCP client."""
        args = ["-y", "mcp-remote", self.endpoint]

        if self.token:
            args.extend(["--header", f"Authorization: Bearer {self.token}"])

        return {
            "mcpServers": {
                self.server_name: {
                    "command": "npx",
                    "args": args,
                }
            }
        }

    def build_command(self) -> list[str]:
        """Build the CLI command used by mcp-remote."""
        command = ["npx", "-y", "mcp-remote", self.endpoint]
        if self.token:
            command.extend(["--header", f"Authorization: Bearer {self.token}"])
        return command

    async def execute(self, *args, **kwargs) -> ToolResult:
        """Return the resolved MCP config and command for the client."""
        config = self.as_mcp_config()
        return ToolResult(
            success=True,
            data={
                "server_name": self.server_name,
                "endpoint": self.endpoint,
                "command": self.build_command(),
                "mcp_config": config,
                "note": (
                    "This tool prepares and validates the Splunk MCP bridge. "
                    "A separate MCP client library is still needed to actually execute tools."
                ),
            },
            message="Splunk MCP bridge configuration ready.",
        )
        
@staticmethod
def tool_schema() -> dict[str, Any]:
    return {
        "type": "function",
        "function": {
            "name": "splunk_mcp_query",
            "description": "Query Splunk through the remote MCP endpoint.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The Splunk search or investigation query to run.",
                    },
                    "earliest": {
                        "type": "string",
                        "description": "The earliest time range, e.g. -1h or -24h.",
                    },
                    "latest": {
                        "type": "string",
                        "description": "The latest time range, e.g. now.",
                    },
                },
                "required": ["query"],
            },
        },
    }
