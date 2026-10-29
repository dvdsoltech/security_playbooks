# Restraints
- All queries use the Splunk MCP tool
- Do not run tools or queries that has the following note at the end: "Query not available at this time" OR "Tool not available at this time"  

# Data Exfiltration Alert - Initial Incident Determination
## Check Alert Details
### Ensure relevant information is recorded and fill in gaps
Record the following information from the alert: source ip, source hostname, source port/protocol, destination ip, destination hostname, destination port/protocol, identity, time range, bytes in, bytes out, alert source, transfer content, and transfer status. If a data point is missing, note it as an alert-tuning request rather than assuming it is unavailable elsewhere. Run the Splunk DNS resolution queries if needed.
- Source IP
  - Query: IP Resolution: `` `sp_dns_index` `sp_dns_query({{SRC_IP}})` ``
- Source Hostname
  - Query: Hostname Resolution: `` `sp_dns_index` `sp_dns_query({{SRC_DNS}})` ``
- Source Port and Protocol
  - Qualifier: If more then 10 high ports and only high ports, just insert "multiple_high_ports"
- Destination IP
  - Destination IP Resolution Query `` `sp_dns_index` `sp_dns_query({{DEST_IP}})` ``
- Destination Hostname
  - Query: Hostname Resolution: `` `sp_dns_index` `sp_dns_query({{DEST_DNS}})` ``
- Destination Ports and Protocol
  - Qualifier: If more then 10 high ports and only high ports, just insert "multiple_high_ports"
- Identity:
- Time Range:
- Bytes in/out:
- Alert Source:
- Transfer Content: Any reported file names, paths, object names, content types, or data-classification labels
- Transfer Status: Whether the alert describes a completed transfer, an attempted transfer, or suspected unconfirmed transfer

## Corroberate Suspicious Activity
### Consider if the entities are expected
- Are the involved entities listed in the asset inventories?
  - Check a Splunk Asset Inventory
    - Asset Inventory: `` \`sp_inventory_assets({{ENTITY_IP}},{{ENTITY_DNS}})\` ``
      - Qualifier: regex wildcard ".*" for whichever entity value is missing
- Is the source entity from a remote device?: `` \`sp_remote_managed_entity({{SRC_IP}})\` ``
- If so, find the operating system and infer the likeliest system function of the entity as gathered by the inventories
- If not included in the alert, infer the priority of the entity in context of its assumed function and operating system within the environment
- Get associated owner, contact, administator if included
- If entity is not included in any official inventory, note the absence.

### Associate identities with the entities
- Infer an account from the hostname if the system has a workstation operating system. VRS tends to assign hostnames that have a matching pattern with the assigned user's account name.
- Review Windows Event Logs for the most recent identities accessing the entity within a +/- 1 hour window of the alert.
  - Windows Event Logs: `` \`sp_windows_4624({{ENTITY_DNS}},{{EARLIEST_EPOCH_TIME}},{{LATEST_EPOCH_TIME}})\` ``
- Do a best-effort deduplication from the above two steps.
- Validate the identities by checking the following identity stores
  - Identity Inventory: `` \`sp_inventory_identities({{IDENTITY}})\` ``
  - Windows Local Accounts `` `\sp_windows_local_accounts{{IDENTITY}}\` `` 
  - Linux Local Accounts (**Query not available at this time**)
  - Distinguish the account that initiated a process from a user who was merely logged on. If attribution is uncertain, say so.

### Examine the transfer
- Determine whether the activity is ongoing. Preserve relevant logs and identifiers needed for follow-up. (Also contributes to scope evaluation)
  - Time the suspected transfer was initiated: 
  - Check remote traffic since that time: `` \`sp_endpoint_connections({{SRC_IP}},{{DEST_IP}})\` ``
  - Check internal traffic since that time: `` \`sp_network_connections({{SRC_IP}},{{DEST_IP}})\` ``

### Assess the destination and normal activity associated with that destination
- Identify the destination’s owner and purpose, if not included in the alert. 
  - Whois for IP ownership
- Determine whether it is an approved business partner, sanctioned SaaS service, corporate cloud tenant, or unknown external endpoint.
- Consider whether it is a common business partner, sanctioned SaaS service, corporate cloud tenant, or unknown external endpoint.


### Attribute activity to processes and data
- Identify the process attributable to the connections `` \`sp_windows_process_connections({{SRC_DNS}}) \` ``
- Further validate process execution within Windows Event Logs if process identified in the previous step: `` \`sp_windows_process_4688_4689({{PROCESS_NAME}},{{SRC_DNS}})\` ``
- See if you can reconcile the two sources above to support process attribution and report as a single correlated summary.
- Look for relevant preparation or access activity from an identified host logs: file reads, archive creation, compression, staging, or use of transfer tools: `index=wineventlog`
- Correlate network, process, file, and identity timestamps. Report **observed file transfer** only when evidence links the files to the transfer; otherwise describe them as potentially related activity.

### Check authorization and/or business context (RAG case)
- Is there an approved system workflow, scheduled job, ticket, or change record explaining the transfer?
  - Change Records:  (**Tool not available at this time**)
  - Application Diagrams:   (**Tool not available at this time**)
  - Application Security Reviews: ` (**Tool not available at this time**)


# Verdict

## Score Findings
- Was data transfered?
- Was the source expected?
- Was the destination expected?
- Is the traffic ongoing?
- What services were associated with the traffice?
- Was the traffic associated with an approved change or application pattern?
- Is it an incident?

## Alert Quality Evaluation
- Is **data exfiltration** the best classification? If not, would *authorized data transfer*, *misconfigured integration*, or *policy violation* be more accurate?
- Does the alert info establish a completed transfer, or only a possible channel or unusual volume?
- What information would be required to know for 100% certain this is unsanctioned data exfiltration activity?
- Is that information present? - yes or no.

## Report

- **Disposition:**
  - Benign: expected or routine activity
  - True Positive: Benign but risky
  - Uncertain: not enough information
  - Attack: threat observed
- **Severity:** low, medium, high, or critical
- **Transfer status:** confirmed, attempted, or unconfirmed
  - If available, what was transferred
- **Recommended action:** 
  - Escalate: 
  - Contain source entity and identity:
    - If transfer is ongoing or sensitive data loss is strongly indicated, escalate and highlight recommendation for containment procedures. (Consider the evidence-preservation and impact of blocking a destination, account, or process given the entity, identity, and file data gathered from the analysis)
  - Monitor: 
  - Suppress: only when the specific workflow has been validated and the suppression conditions are narrow enough to retain visibility into deviations.
- **Evidence:** Concise, timestamped findings from the summary, with log references and explicit uncertainty.
