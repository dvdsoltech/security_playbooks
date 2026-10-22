from __future__ import annotations

from tools.mixmode_tool import MixmodeTool
from tools.splunk_mcp_tool import SplunkMcpTool


def register_tools() -> dict[str, object]:
    return {
        "splunk": SplunkMcpTool(),
        "mixmode": MixmodeTool(),
    }
