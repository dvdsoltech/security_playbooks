from __future__ import annotations

import os
from typing import Any

from tools.base_tool import SecurityTool, ToolResult


class SplunkMcpTool(SecurityTool):
    """Real MCP execution wrapper for Splunk remote tools."""

    def __init__(self):
        super().__init__(
            name="splunk_mcp",
            base_url=os.getenv("SPLUNK_MCP_ENDPOINT"),
        )
        self.endpoint = self.base_url
        self.token = os.getenv("SPLUNK_MCP_TOKEN")
        self.server_name = os.getenv("SPLUNK_MCP_SERVER_NAME", "splunk-mcp-server")

    def build_command(self) -> list[str]:
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
                            "description": "The Splunk MCP tool to call, e.g. search, lookup, kvstore_read, etc.",
                        },
                        "query": {
                            "type": "string",
                            "description": "Primary query or payload used by the remote MCP tool.",
                        },
                        "arguments": {
                            "type": "object",
                            "description": "Optional arguments for the operation.",
                            "additionalProperties": True,
                        },
                    },
                    "required": ["operation", "query"],
                },
            },
        }

    @staticmethod
    def _normalize_result(result: Any) -> Any:
        if hasattr(result, "model_dump"):
            return result.model_dump()
        if hasattr(result, "dict"):
            return result.dict()
        if isinstance(result, (list, dict, str, int, float, bool)) or result is None:
            return result
        return str(result)

    async def execute(
        self,
        operation: str,
        query: str,
        arguments: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> ToolResult:
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
                from mcp import ClientSession
                from mcp.client.stdio import stdio_client
                from mcp import StdioServerParameters
            except ImportError as exc:  # pragma: no cover
                raise RuntimeError(
                    "The MCP Python library is required. Install `mcp` to enable real Splunk MCP execution."
                ) from exc

            command_args = ["-y", "mcp-remote", self.endpoint]
            if self.token:
                command_args.extend(["--header", f"Authorization: Bearer {self.token}"])

            server_params = StdioServerParameters(
                command="npx",
                args=command_args,
            )

            payload = {"query": query}
            if arguments:
                payload.update(arguments)

            async with stdio_client(server_params) as (read, write):
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    result = await session.call_tool(operation, payload)

                    return ToolResult(
                        success=True,
                        data={
                            "operation": operation,
                            "query": query,
                            "arguments": payload,
                            "result": self._normalize_result(result),
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
