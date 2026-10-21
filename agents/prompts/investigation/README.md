# Investigation Playbooks

This directory contains scenario-specific investigation prompts for the security operations workflow. Each playbook is selected by the router based on the alert or incident classification.

## Standard methodology

- All queries should use the Splunk MCP tool unless a different designated tool is explicitly required.
- Do not run or reference a query or tool that is flagged with the note: "Query not available at this time" or "Tool not available at this time".
- Treat missing data points as alert-tuning requests rather than assuming the data exists elsewhere.
- Record all evidence with timestamps, entities, identities, and confidence levels.
- Distinguish clearly between confirmed activity, suspected activity, and unresolved uncertainty.

## Available playbooks

- malware.md
- ransomware.md
- account_compromise.md
- lateral_movement.md
- public_application.md
- data_exfiltration.md
- denial_of_service.md
- malicious_scanning.md
- cloud_compromise.md
- emerging_threat.md
