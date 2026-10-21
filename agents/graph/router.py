from __future__ import annotations

from pathlib import Path

PROMPT_ROOT = Path(__file__).resolve().parents[1] / "prompts" / "investigation"

PLAYBOOK_KEYWORDS = {
    "ransomware": ["ransomware", "encryption", "ransom note"],
    "malware": ["malware", "payload", "virus", "trojan", "malicious file"],
    "account_compromise": ["account compromise", "credential abuse", "mfa", "token theft", "user compromise"],
    "lateral_movement": ["lateral movement", "pivot", "remote execution", "rdp", "smb", "wmi"],
    "public_application": ["public application", "web app", "external app", "web attack", "application abuse"],
    "data_exfiltration": ["data exfiltration", "exfil", "transfer out", "sensitive data", "large upload"],
    "denial_of_service": ["denial of service", "ddos", "service outage", "traffic spike"],
    "malicious_scanning": ["scanning", "reconnaissance", "enumeration", "port scan", "probe"],
    "cloud_compromise": ["cloud compromise", "cloudtrail", "iam", "azure", "aws", "gcp", "token abuse"],
    "emerging_threat": ["emerging threat", "novel activity", "new campaign", "unknown attack", "zero-day"],
}


def load_prompt(path: str | Path) -> str:
    return Path(path).read_text(encoding="utf-8")


def select_investigation_playbook(incident_summary: str) -> str:
    """Select the most relevant investigation playbook based on alert terminology."""
    normalized = incident_summary.lower()

    for playbook_name, keywords in PLAYBOOK_KEYWORDS.items():
        if any(keyword in normalized for keyword in keywords):
            return str(PROMPT_ROOT / f"{playbook_name}.md")

    return str(PROMPT_ROOT / "emerging_threat.md")


def route_incident(incident_summary: str) -> dict[str, str]:
    playbook_path = select_investigation_playbook(incident_summary)
    return {
        "playbook_path": playbook_path,
        "prompt": load_prompt(playbook_path),
        "selected_playbook": Path(playbook_path).stem,
    }
