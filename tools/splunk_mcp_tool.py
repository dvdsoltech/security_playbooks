from __future__ import annotations

import os
from typing import Any

from tools.base_tool import SecurityTool, ToolResult


class SplunkMcpTool(SecurityTool):
    """Wrapper for the Splunk remote MCP server."""

    def __init__(self):
        super().__init__(name="splunk_mcp", base_url=os.getenv("SPLUNK_MCP_ENDPOINT"))
        self.endpoint = self.base_url
        self.token = os.getenv("SPLUNK_MCP_TOKEN")
        self.server_name = os.getenv("SPLUNK_MCP_SERVER_NAME", "splunk-mcp-server")

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

    @staticmethod
    def tool_schema() -> dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "splunk_mcp_execute",
                "description": "Execute a Splunk MCP operation such as a search, lookup, investigation, or data retrieval.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "operation": {
                            "type": "string",
                            "description": "The Splunk MCP tool name to call, for example: search, lookup, kvstore_read, or another supported operation.",
                        },
                        "query": {
                            "type": "string",
                            "description": "The primary query or command payload accepted by the remote MCP tool.",
                        },
                        "arguments": {
                            "type": "object",
                            "description": "Optional additional arguments to pass to the MCP tool.",
                            "additionalProperties": True,
                        },
                    },
                    "required": ["operation", "query"],
                },
            },
        }

    async def execute(
        self,
        operation: str,
        query: str,
        arguments: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> ToolResult:
        """Initialize the MCP client, create a session, call the remote tool, and return the payload."""
        if not operation:
            return ToolResult(success=False, data={}, message="operation is required.")

        if not query:
            return ToolResult(success=False, data={}, message="query is required.")

        if not self.endpoint:
            return ToolResult(
                success=False,
                data={},
                message="SPLUNK_MCP_ENDPOINT is not configured.",
            )

        try:
            try:
                from mcp import StdioServerParameters
                from mcp.client.session import ClientSession
                from mcp.client.stdio import stdio_client
            except ImportError as exc:  # pragma: no cover
                raise RuntimeError(
                    "The MCP Python client library is required for Splunk MCP execution. "
                    "Install the `mcp` package."
                ) from exc

            args = ["-y", "mcp-remote", self.endpoint]

            if self.token:
                args.extend(["--header", f"Authorization: Bearer {self.token}"])

            server_params = StdioServerParameters(
                command="npx",
                args=args,
            )

            payload = {"query": query}
            if arguments:
                payload.update(arguments)

            async with stdio_client(server_params) as (read, write):
                async with ClientSession(read, write) as session:
                    await session.initialize()

                    result = await session.call_tool(operation, payload)

                    payload_result = None
                    if hasattr(result, "model_dump"):
                        payload_result = result.model_dump()
                    elif hasattr(result, "dict"):
                        payload_result = result.dict()
                    else:
                        payload_result = result

                    return ToolResult(
                        success=True,
                        data={
                            "operation": operation,
                            "query": query,
                            "arguments": payload,
                            "result": payload_result,
                            "endpoint": self.endpoint,
                        },
                        message="Splunk MCP tool executed successfully.",
                    )

        except Exception as exc:  # pragma: no cover
            return ToolResult(
                success=False,
                data={
                    "operation": operation,
                    "query": query,
                    "arguments": arguments or {},
                },
                message=f"Splunk MCP tool execution failed: {exc}",
            )
