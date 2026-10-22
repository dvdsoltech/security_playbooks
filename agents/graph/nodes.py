from __future__ import annotations

import json

from typing import Any
from pathlib import Path

from langgraph.graph import END, StateGraph
from langgraph.prebuilt import tools_condition
from langchain_core.messages import AIMessage

from agents.graph.state import AgentState

from tools.tool_registry import register_tools

""" Returns a selected provider class"""
from providers.provider_factory import create_model_provider

""" We're going to centrally manage the assignment evaluation prompt, so grab that. """
PROMPT_ROOT = Path(__file__).resolve().parents[1] / "prompts"


""" We'll let the upstream sources determine initial severity.  """
async def assign_incident(state: AgentState) -> AgentState:
    """The invocation will include the alert details. Here we will have the LLM evaluate the as-is alert content and determine initial applicable playbook."""

    alert_payload = state.raw_alert
    provider = create_model_provider()
    system_prompt = Path(PROMPT_ROOT / "assignment_prompt.md").read_text(encoding="utf-8")
    user_message = json.dumps(alert_payload or {}, default=str, sort_keys=True)

    response = await provider.invoke(
        system_prompt=system_prompt,
        user_message=user_message
    )
    if isinstance(response, str):
        response = AIMessage(content=response)

    state.messages.append(response)
    
    parsed = json.loads(response.content) if isinstance(response.content, str) and response.content.strip().startswith("{") else {}
    
    state.playbook = parsed.get("playbook", "").strip().lower()
    state.rationale = parsed.get("rationale", "").strip()
    state.status = "assignment"
    state.next_step = "Proceed with the appropriate security playbook to the reported security event"
    return state


async def investigate_incident(state: AgentState) -> AgentState:
    """Collect findings from tools and evidence sources, disposition, and log"""
    provider = create_model_provider()
    tool_map = register_tools()

    tools = [
        tool.tool_schema()
        for tool in tool_map.values()
        if hasattr(tool, "tool_schema")
    ]

    alert_payload = state.raw_alert
    system_prompt = Path(PROMPT_ROOT / state.playbook).read_text(encoding="utf-8")
    user_message = json.dumps(alert_payload, default=str, sort_keys=True)
    
    response = await provider.invoke(
        system_prompt=system_prompt,
        user_message=user_message,
        tools=tools,
        tool_choice="auto",
    )
    
    # Store the tool call payload the graph will route on
    # This depends on how your provider returns tool_calls.
    if isinstance(response, str):
        response = AIMessage(content=response)
    state.messages.append(response)
    
    # The provider may return a plain text response or a tool-call result.
    # If it returns tool calls, execute them and feed the result back to the model.
    
    parsed = json.loads(response.content) if isinstance(response.content, str) and response.content.strip().startswith("{") else {}
    state.quality_check = parsed.get("quality_check", "").strip()
    state.recommendations = parsed.get("recommendations", "").strip()
    state.findings = parsed.get("findings", "").strip()
    state.status = "investigating"
    state.next_step = "Correlate evidence across detection systems and validate the root cause"
    
    return state


async def tool_node(state: AgentState) -> AgentState:
    """Execute tool calls emitted by the model."""
    tool_map = register_tools()

    if not state.messages:
        return state

    last_message = state.messages[-1]

    if not getattr(last_message, "tool_calls", None):
        return state

    for call in last_message.tool_calls:
        tool_name = call.get("name")
        args = call.get("args", {}) or {}

        if tool_name not in tool_map:
            state.errors.append(f"Unknown tool requested: {tool_name}")
            continue

        tool = tool_map[tool_name]
        result = await tool.execute(**args)

        if result.success:
            state.evidence.append(
                {
                    "tool": tool_name,
                    "data": result.data,
                    "message": result.message,
                }
            )
        else:
            state.errors.append(f"{tool_name}: {result.message}")

    state.status = "investigating"
    return state

    
""" Conclusion from the perspective of the graph node. """
async def conclude_incident(state: AgentState) -> AgentState:
    """Generate and recommend containment or remediation actions. Communicate with the humans"""
    """Final state for a resolved or blocked event."""
    state.status = "concluded" if not state.errors else "blocked"
    state.next_step = "execute response actions and document audit entries"
    return state


def build_graph() -> StateGraph:
    analysis = StateGraph(AgentState)

    analysis.add_node("assignment", assign_incident)
    analysis.add_node("investigate", investigate_incident)
    analysis.add_node("tools", tool_node)
    analysis.add_node("conclude", conclude_incident)

    analysis.set_entry_point("assignment")

    analysis.add_edge("assignment", "investigate")
    analysis.add_conditional_edge("investigate", tools_condition)
    analysis.add_edge("tools","investigate")
    analysis.add_edge("investigate", "conclude")
    
    analysis.add_edge("conclude", END)

    return analysis
