from __future__ import annotations

from typing import Any
from pathlib import Path

from langgraph.graph import END, StateGraph
from langgraph.prebuilt import tools_condition

from agents.graph.state import AgentState

""" Returns a selected provider class"""
from providers.provider_factory import create_model_provider

""" We're going to centrally manage the assignment evaluation prompt, so grab that. """
PROMPT_ROOT = Path(__file__).resolve().parents[1] / "prompts"
ASSIGNMENT_PROMPT_PATH = PROMPT_ROOT / "assignment_prompt.md"

""" We'll let the upstream sources determine initial severity.  """
def assign_incident(state: AgentState) -> AgentState:
    """The invocation will include the alert details. Here we will have the LLM evaluate the as-is alert content and determine initial applicable playbook."""

    alert_payload = state.to_dict()
    provider = create_model_provider()
    system_prompt = Path(ASSIGNMENT_PROMPT_PATH).read_text(encoding="utf-8")
    input = json.dumps(alert_payload, default=str, sort_keys=True)

    decision = await provider.invoke(
        system_prompt=system_prompt,
        input=input
    )
    parsed = json.loads(decision)
    playbook = parsed.get("playbook", "").strip().lower()
    rationale = parsed.get("rationale", "").strip()
    
    state.playbook = playbook
    state.rationale = rationale
    state.status = "assignment"
    state.next_step = "Proceed with the appropriate security playbook to the reported security event"
    return state

def investigate_incident(state: AgentState) -> AgentState:
    """Collect findings from tools and evidence sources, disposition, and log"""
    state.status = "investigating"
    state.next_step = "Correlate evidence across detection systems and validate the root cause"
    return state

""" Conclusion from the perspective of the agent. """
def conclude_incident(state: AgentState) -> AgentState:
    """Generate and recommend containment or remediation actions. Communicate with the humans"""
    """Final state for a resolved or blocked event."""
    state.status = "concluded" if not state.errors else "blocked"
    state.next_step = "execute response actions and document audit entries"
    return state


def build_graph() -> StateGraph:
    analysis = StateGraph(AgentState)

    analysis.add_node("assignment", assign_incident)
    analysis.add_node("investigate", investigate_incident)
    analysis.add_node("conclude", conclude_incident)

    analysis.set_entry_point("assignment")

    analysis.add_edge("assignment", "investigate")
    analysis.add_conditional_edge("investigate", tools_condition)
    analysis.add_edge("tools","investigate")
    analysis.add_edge("investigate", "conclude")
    
    analysis.add_edge("conclude", END)

    return analysis
