# Security Playbooks

This repository contains a LangGraph-based multi-agent security operations framework for orchestrating investigation, triage, and response workflows. The system is designed to align with operational playbooks and evidence collection while supporting a clean integration layer for Splunk, Mixmode, and custom API tools.

## Goals

- Multi-agent orchestration for security workflows
- Markdown-based playbooks and system prompts
- Structured evidence gathering and action history
- Integration with Splunk via API + MCP
- Integration with Mixmode via API search/query endpoints
- Export-ready architecture for Microsoft Foundry

## Repository Layout

- `agents/` – LangGraph agents and orchestration logic
- `tools/` – wrappers for Splunk, Mixmode, and custom API integrations
- `playbooks/` – policy and procedure markdown playbooks
- `configs/` – settings and deployment configuration
- `tests/` – validation tests
- `docs/` – architecture and operational documentation

## Quick Start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Then run the graph locally:

```bash
python -m agents.graph.app
```

## Microsoft Foundry Note

This project is intended for export and deployment to Microsoft Foundry (Azure AI Foundry / Foundry-based deployment patterns), not Palantir.
