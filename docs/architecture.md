# Security Playbooks Project

## Architecture overview

This repository is a multi-agent security operations framework driven by LangGraph. The graph is designed to coordinate triage, investigation, and response steps while leveraging external detection tools such as Splunk and Mixmode.

## Notes

- System prompts are intentionally stored as markdown files in a dedicated prompts directory for version controlled playbook definitions.
- The workflow uses a shared state model to track evidence, findings, actions, and recommended next steps.
- Microsoft Foundry export is planned as a deployment target, not a Palantir integration.
