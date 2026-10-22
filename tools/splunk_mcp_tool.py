import os

from langchain_core.tools import BaseTool
from langchain_mcp_adapters.client import MultiServerMCPClient


def create_splunk_mcp_client() -> MultiServerMCPClient:
    url = os.environ.get("SPLUNK_MCP_URL")
    token = os.environ.get("SPLUNK_MCP_TOKEN")

    if not url or not url.strip():
        raise RuntimeError("SPLUNK_MCP_URL must be set")
    if not token or not token.strip():
        raise RuntimeError("SPLUNK_MCP_TOKEN must be set")

    return MultiServerMCPClient(
        {
            "splunk": {
                "transport": "streamable_http",
                "url": url,
                "headers": {"Authorization": f"Bearer {token}"},
            }
        }
    )


async def get_splunk_tools() -> list[BaseTool]:
    client = create_splunk_mcp_client()
    return await client.get_tools(server_name="splunk")


def main():
    print("Hello from soc-lite!")


if __name__ == "__main__":
    main()
