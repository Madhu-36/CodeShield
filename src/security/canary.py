import re
from typing import Dict, Any, List, Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

console = Console(safe_box=True)

class CanaryTrapEngine:
    """
    HoneyToken & Prompt Injection Exfiltration Trap.
    Plants synthetic decoy credentials into the workspace memory space.
    If an autonomous coding agent or poisoned prompt attempts to steal or transmit
    a canary token, CodeShield triggers an immediate Emergency Lockdown.
    """

    CANARY_TOKENS = [
        {
            "id": "CANARY-AWS-01",
            "type": "Cloud Infrastructure Credential",
            "token": "AKIA_CODESHIELD_TRAP_9X8B72",
            "decoy_service": "AWS IAM Production Vault"
        },
        {
            "id": "CANARY-DB-02",
            "type": "Database Connection String",
            "token": "postgres://root:cs_decoy_pass_8891@cluster.db.internal/core",
            "decoy_service": "PostgreSQL Main Customer Table"
        },
        {
            "id": "CANARY-API-03",
            "type": "AI Gateway Secret Key",
            "token": "sk-codeshield-honeytrap-v2-4910294",
            "decoy_service": "Enterprise LLM Gateway"
        }
    ]

    @classmethod
    def inspect_for_canary_leak(cls, command: str) -> Optional[Dict[str, Any]]:
        """
        Inspects command payload for attempted exfiltration of any canary honeytokens.
        """
        for c in cls.CANARY_TOKENS:
            if c["token"] in command or re.search(re.escape(c["token"][:12]), command):
                return {
                    "alert": "EMERGENCY_LOCKDOWN_TRIGGERED",
                    "canary_id": c["id"],
                    "canary_type": c["type"],
                    "targeted_service": c["decoy_service"],
                    "reason": "Autonomous agent or prompt injection attempted to exfiltrate canary credential!",
                    "action_taken": "Execution killed. Network isolation enforced. Alert dispatched to iQOO phone."
                }
        return None

    @classmethod
    def render_cli_status(cls):
        console.print(Panel("[*] CODESHIELD CANARY HONEYTOKEN DEFENSE MATRIX", style="bold cyan"))
        
        table = Table(title="Active Synthetic Honeytokens Monitored by NPU", box=box.SIMPLE)
        table.add_column("Canary ID", style="bold cyan")
        table.add_column("Decoy Target", style="white")
        table.add_column("Trap Signature", style="dim green")
        table.add_column("Interception Status", style="bold green")

        for c in cls.CANARY_TOKENS:
            masked = c["token"][:12] + "..." + c["token"][-4:]
            table.add_row(c["id"], c["decoy_service"], masked, "[ACTIVE - ARMED]")

        console.print(table)
        console.print("[dim green][+] 3 Honeytokens armed. Zero-tolerance prompt injection defense active.[/dim green]\n")
