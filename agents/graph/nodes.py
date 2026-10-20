from __future__ import annotations

from typing import Any

from langgraph.graph import END, StateGraph

from agents.graph.state import AgentState


def orchestrate_incident(state: AgentState) -> AgentState:
    """Entry node that sets the initial workflow state."""
    state.status = "triage"
    state.next_step = "triage the reported incident and collect initial evidence"
    return state


def triage_incident(state: AgentState) -> AgentState:
    """Gather initial incident context and determine severity."""
    state.status = "triage"
    if state.severity in {"high", "critical"}:
        state.next_step = "route to investigation and response workflow"
    else:
        state.next_step = "perform standard investigation and business impact review"
    return state


def investigate_incident(state: AgentState) -> AgentState:
    """Collect derived findings from tools and evidence sources."""
    state.status = "investigating"
    state.next_step = "correlate evidence across detection systems and validate the root cause"
    return state


def respond_to_incident(state: AgentState) -> AgentState:
    """Generate and recommend containment or remediation actions."""
    state.status = "responding"
    state.next_step = "execute response actions and document audit entries"
    return state


def finalize_incident(state: AgentState) -> AgentState:
    """Final state for a resolved or blocked event."""
    state.status = "resolved" if not state.errors else "blocked"
    state.next_step = "complete closure summary and preserve evidence artifacts"
    return state


def build_graph() -> StateGraph:
    workflow = StateGraph(AgentState)

    workflow.add_node("orchestrate", orchestrate_incident)
    workflow.add_node("triage", triage_incident)
    workflow.add_node("investigate", investigate_incident)
    workflow.add_node("respond", respond_to_incident)
    workflow.add_node("finalize", finalize_incident)

    workflow.set_entry_point("orchestrate")
    workflow.add_edge("orchestrate", "triage")
    workflow.add_edge("triage", "investigate")
    workflow.add_edge("investigate", "respond")
    workflow.add_edge("respond", "finalize")
    workflow.add_edge("finalize", END)

    return workflow
