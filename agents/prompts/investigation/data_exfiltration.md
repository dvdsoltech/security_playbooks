# Restraints
- All queries use the Splunk MCP tool
- Do not run tools or queries that has the following note at the end: "Query not available at this time" OR "Tool not available at this time"  

# Data Exfiltration Alert - Initial Incident Determination
## Check Alert Details
### Ensure relevant information is recorded and fill in gaps
Record the following information from the alert. If a data point is missing, note it as an alert-tuning request rather than assuming it is unavailable elsewhere. Run the Splunk DNS resolution queries if needed.
- Source IP
  - Query: IP Resolution: `` `sp_dns_index` `sp_dns_query({src_ip})` ``
- Source Hostname
  - Query: Hostname Resolution: `` `sp_dns_index` `sp_dns_query({src_dns})` ``
- Source Port and Protocol
  - Qualifier: If more then 10 high ports and only high ports, just insert "multiple_high_ports"
- Destination IP
  - Destination IP Resolution Query `` `sp_dns_index` `sp_dns_query({dest_ip})` ``
- Destination Hostname
  - Query: Hostname Resolution: `` `sp_dns_index` `sp_dns_query({dest_dns})` ``
- Destination Ports and Protocol
  - Qualifier: If more then 10 high ports and only high ports, just insert "multiple_high_ports"
- Identity
- Time Range
- Bytes in/out
- Alert Source
- Any reported file names, paths, object names, content types, or data-classification labels
- Whether the alert describes a completed transfer, an attempted transfer, or suspected unconfirmed transfer

## Corroberate Suspicious Activity
### Consider if the entities are expected
- Are the involved entities listed in VRS inventories?
  - Check a Splunk Asset Inventory
    - Asset Inventory: `\`sp_inventory_assets({entity_ip},{entity_dns})\``
      - Qualifier: regex wildcard ".*" for whichever entity value is missing
- If so, find the operating system and infer the likeliest system function of the entity as gathered by the inventories
- If not included in the alert, infer the priority of the entity in context of its assumed function and operating system within the environment
- Get associated owner, contact, administator if included
- If entity is not included in any official inventory, note the absence.

### Associate identities with the entities
- Infer an account from the hostname if the system has a workstation operating system. VRS tends to assign hostnames that have a matching pattern with the assigned user's account name.
- Review Windows Event Logs for the most recent identities accessing the entity within a +/- 1 hour window of the alert.
  - Windows Event Logs: `index=wineventlog EventCode=4624 <entity_hostname> Account_Name!="*$"  Source_Network_Address!="10.21.4.25" earliest=<alert_earliest_time_epoch_minus_1_hour> latest=<alert_latest_time_epoch_plus_1_hour>  | stats values(Account_Name) as accounts  by ComputerName Source_Network_Address`
- Do a best-effort deduplication from the above two steps.
- Validate the identities by checking the following identity stores
  - LDAP: `| inputlookup vrs_identities_ldap | where match(identity,"<identity>") OR match(identity,"<identity2>") | table identity user_domain userAccountControl displayName category`
  - Okta `index=okta <identity> OR <identity2> earliest=-1h | table _time * ` (**Query not available at this time**)
  - Entra `| inputlookup vrs_identities_entra | where match(identity,"<identity>") OR match(identity,"<identity2>") | table identity user_domain  displayName email first laset title *`
  - Windows Local Accounts `index=windows sourcetype=WinLocalUsers` (**Query not available at this time**)
  - Distinguish the account that initiated a process from a user who was merely logged on. If attribution is uncertain, say so.

### Consider if network traffic is normal
- Determine whether the system routinely handles sensitive data or makes outbound transfers.
- History of this specific traffic as seen in the logs
  - Palo Alto `index=paloalto <entity_ip> <entity2_ip>  earliest=-7d  latest=now  | stats count dc(src_port) as src_port by src_ip dest_ip dest_port action `
  - MixMode: `API getLogs or getIndicator` request
- History of this specific connection as stored in alert history
  - MixMode: `index=mixmode <entity_ip> <entity2_ip>  earliest=-30d | stats count values(mitreTacticId) as mitreTacticId values(mitreTacticName) as mitreTacticName  by alertName `
- History of this specific connection referenced in knowledge stores (**Tool not available at this time**)
- Absent alert disclosure, does this traffic look normal based on the judgment of the analyst (Thinking of industry standard best practices and well known security controls)
- Assign a verdict of likely or not-likely normal traffic. 

### Examine the transfer
- Determine whether the activity is ongoing. Preserve relevant logs and identifiers needed for follow-up. (Also contributes to scope evaluation)

### Assess the destination and normal activity associated with that destination
- Identify the destination’s owner and purpose, if not included in the alert. 
  - Whois for IP ownership
- Determine whether it is an approved business partner, sanctioned SaaS service, corporate cloud tenant, or unknown external endpoint.
- Consider whether it is a common business partner, sanctioned SaaS service, corporate cloud tenant, or unknown external endpoint.
- Check whether the destination is newly observed for the source, identity, or environment: `<query>`



### Attribute activity to processes and data
- Identify the process attributable to the connections `index=windows sourcetype=ProcessConnections  <entity_ip> OR <entity2_ip> | table OwningProcess ProcessName State  LocalAddress LocalPort RemoteAddress RemotePort `
- Further validate process execution within Windows Event Logs if process identified in the previous step: `index=wineventlog EventCode=4688 OR EventCode=4689 <process_name> <entity_hostname> OR <entity2_hostname> | table _time signature action Account_Name Account_Domain ComputerName Creator_Process_Name New_Process_ID New_Process_Name process`
- See if you can reconcile the two sources above to support process attribution and report as a single correlated summary.
- Look for relevant preparation or access activity from an identified host logs: file reads, archive creation, compression, staging, or use of transfer tools: `index=wineventlog`
- Correlate network, process, file, and identity timestamps. Report **observed file transfer** only when evidence links the files to the transfer; otherwise describe them as potentially related activity.

### Check authorization and/or business context (RAG case)
- Is there an approved system workflow, scheduled job, ticket, or change record explaining the transfer?
  - Change Records:  (**Tool not available at this time**)
  - Application Diagrams:   (**Tool not available at this time**)
  - Application Security Reviews: ` (**Tool not available at this time**)

### Get a Sense of Scope
- Search several days before and after the alert for related transfers involving the same source, identity, process, destination, or data set: `<query>` (**Query not available at this time**)
- Look for other sources sending data to the same destination or receiving account: `<query>` (**Query not available at this time**)
- Correlate preceding suspicious activity, such as unusual authentication, privilege changes, bulk data access, or disabling of security controls: `<query>` (**Query not available at this time**)
- Correlate other notable events across the same process, identity, and entities `index=notable <process_name> OR <identity> OR <identity2> OR <entity_hostname> OR <entity2_hostname> OR <entity_ip> OR entity2_ip | table _time search_name risk_* threat_*``

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
