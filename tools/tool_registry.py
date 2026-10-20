from __future__ import annotations

from tools.mixmode_tool import MixmodeTool
from tools.splunk_tool import SplunkTool


def register_tools() -> dict[str, object]:
    return {
        "splunk": SplunkTool(),
        "mixmode": MixmodeTool(),
    }
