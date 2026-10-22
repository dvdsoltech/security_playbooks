from __future__ import annotations

import os
from typing import Any

import httpx

from tools.base_tool import SecurityTool, ToolResult


class SplunkApiTool(SecurityTool):
    """Strictly POST-only wrapper for Splunk kvstore writes using a bearer token."""

    def __init__(self):
        super().__init__(
            name="splunk_api",
            base_url=os.getenv("SPLUNK_API_BASE_URL"),
        )
        self.token = os.getenv("SPLUNK_API_TOKEN")
        self.session = None

    @staticmethod
    def tool_schema() -> dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "splunk_kvstore_post",
                "description": "Write a JSON payload to a Splunk kvstore collection using an HTTP POST. This tool is restricted to POST operations only.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "collection": {
                            "type": "string",
                            "description": "The Splunk kvstore collection name to write to.",
                        },
                        "payload": {
                            "type": "object",
                            "description": "The JSON object payload to be inserted or updated in the collection.",
                            "additionalProperties": True,
                        },
                    },
                    "required": ["collection", "payload"],
                },
            },
        }

    async def execute(
        self,
        collection: str,
        payload: dict[str, Any],
        **kwargs: Any,
    ) -> ToolResult:
        """POST a JSON payload to a Splunk kvstore collection."""
        if not collection:
            return ToolResult(success=False, data={}, message="collection is required.")

        if not isinstance(payload, dict):
            return ToolResult(success=False, data={}, message="payload must be a JSON object.")

        if not self.base_url:
            return ToolResult(
                success=False,
                data={},
                message="SPLUNK_API_BASE_URL is not configured.",
            )

        if not self.token:
            return ToolResult(
                success=False,
                data={},
                message="SPLUNK_API_TOKEN is not configured.",
            )

        endpoint = f"{self.base_url.rstrip('/')}/{collection}"

        try:
            if self.session is None:
                self.session = httpx.AsyncClient(
                    headers={"Authorization": f"Bearer {self.token}"},
                    timeout=30.0,
                )

            response = await self.session.post(
                endpoint,
                json=payload,
            )
            response.raise_for_status()

            return ToolResult(
                success=True,
                data={
                    "collection": collection,
                    "payload": payload,
                    "status_code": response.status_code,
                    "response": response.json() if response.content else {},
                },
                message="POST successful.",
            )
        except Exception as exc:  # pragma: no cover
            return ToolResult(
                success=False,
                data={"collection": collection, "payload": payload},
                message=f"Splunk kvstore POST failed: {exc}",
            )
