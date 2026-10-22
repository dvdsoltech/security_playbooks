from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal


@dataclass
class AgentState:
    """State container used by the LangGraph workflow."""

    incident_id: str | None = None
    status: Literal["new", "assignment", "investigating", "responding", "concluded", "blocked"] = "new"
    severity: Literal["low", "medium", "high", "critical"] = "medium"
    raw_alert: dict[str, Any] | None = None
    source: str | None = None
    messages: list[BaseMessage] = field(default_factory=list)
    evidence: list[dict[str, Any]] = field(default_factory=list)
    findings: list[str] = field(default_factory=list)
    actions_taken: list[str] = field(default_factory=list)
    recommendations: list[str] = field(default_factory=list)
    quality_check: str | None = None
    playbook: str | None = None
    rationale: str | None = None
    next_step: str | None = None
    tool_calls: list[dict[str, Any]] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "incident_id": self.incident_id,
            "status": self.status,
            "severity": self.severity,
            "raw_alert": self.raw_alert,
            "source": self.source,
            "evidence": self.evidence,
            "quality_check": self.quality_check,
            "findings": self.findings,
            "messages": self.messages,
            "actions_taken": self.actions_taken,
            "recommendations": self.recommendations,
            "playbook": self.playbook,
            "rationale": self.rationale,
            "next_step": self.next_step,
            "tool_calls": self.tool_calls,
            "errors": self.errors,
        }
