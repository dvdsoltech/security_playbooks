from __future__ import annotations

from tools.mixmode_tool import MixmodeTool
from tools.splunk_mcp_tool import SplunkMcpTool
from tools.splunk_api_tool import SplunkApiTool


def register_tools() -> dict[str, object]:
    return {
        "splunk_mcp": SplunkMcpTool(),
        "splunk_api": SplunkApiTool(),
        "mixmode": MixmodeTool()
    }
