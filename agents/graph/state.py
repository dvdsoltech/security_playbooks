from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal


@dataclass
class AgentState:
    """State container used by the LangGraph workflow."""

    incident_id: str | None = None
    status: Literal["new", "assignment", "investigating", "responding", "concluded", "blocked"] = "new"
    severity: Literal["low", "medium", "high", "critical"] = "medium"
    source: str | None = None
    title: str | None = None
    summary: str | None = None
    entity: str | None = None
    evidence: list[dict[str, Any]] = field(default_factory=list)
    findings: list[str] = field(default_factory=list)
    actions_taken: list[str] = field(default_factory=list)
    recommendations: list[str] = field(default_factory=list)
    playbook: str | None = None
    rationale: str | None = None
    next_step: str | None = None
    errors: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "incident_id": self.incident_id,
            "status": self.status,
            "severity": self.severity,
            "source": self.source,
            "title": self.title,
            "summary": self.summary,
            "entity": self.entity,
            "evidence": self.evidence,
            "findings": self.findings,
            "actions_taken": self.actions_taken,
            "recommendations": self.recommendations,
            "playbook": self.playbook,
            "rationale": self.rationale,
            "next_step": self.next_step,
            "errors": self.errors,
        }
