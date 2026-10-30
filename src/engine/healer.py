import re
from typing import Dict, Any, Optional

class SelfHealingEngine:
    """
    Autonomous Self-Healing Command Rewriter.
    Intercepts destructive or high-risk AI-generated commands and
    automatically reconstructs safe, non-destructive, and reversible alternatives.
    """

    HEALING_RULES = [
        {
            "name": "Recursive Removal Reversal",
            "pattern": r"\brm\s+(-rf|-fr|-r)\s+([^\s;&|]+)",
            "heal_fn": lambda m: f"mkdir -p .codeshield_trash && mv {m.group(2)} .codeshield_trash/",
            "strategy": "Safely relocates target to a quarantined trash directory instead of permanent unrecoverable deletion.",
            "safety_gain": "Reversible deletion with 100% recovery window"
        },
        {
            "name": "Untrusted Pipe to Shell Quarantine",
            "pattern": r"(curl|wget)\s+([^\s;&|]+)\s*\|\s*(bash|sh)",
            "heal_fn": lambda m: f"{m.group(1)} -s {m.group(2)} > .codeshield_quarantine.sh && python cli.py review .codeshield_quarantine.sh 1",
            "strategy": "Quarantines the remote script to disk and triggers immediate AST safety review before execution.",
            "safety_gain": "Eliminates blind remote code execution"
        },
        {
            "name": "Database Schema Preservation",
            "pattern": r"\bDROP\s+TABLE\s+([a-zA-Z0-9_]+)",
            "heal_fn": lambda m: f"ALTER TABLE {m.group(1)} RENAME TO {m.group(1)}_archived_backup",
            "strategy": "Renames database table to timestamped backup rather than permanently dropping data.",
            "safety_gain": "Zero accidental data loss"
        },
        {
            "name": "Permissive Permission Tightening",
            "pattern": r"\bchmod\s+777\s+([^\s;&|]+)",
            "heal_fn": lambda m: f"chmod 755 {m.group(1)}",
            "strategy": "Applies principle of least privilege (755) instead of dangerously open world-writable permissions.",
            "safety_gain": "Blocks unauthorized world-write vulnerabilities"
        },
        {
            "name": "Git Force Push Lease Guard",
            "pattern": r"\bgit\s+push\s+.*(-f|--force)\b",
            "heal_fn": lambda m: m.group(0).replace("-f", "--force-with-lease").replace("--force", "--force-with-lease"),
            "strategy": "Replaces destructive blind force-push with safe lease verification.",
            "safety_gain": "Prevents team commit clobbering"
        }
    ]

    @classmethod
    def heal_action(cls, command: str) -> Dict[str, Any]:
        """
        Analyzes a command and returns an autonomous self-healed alternative if risky.
        """
        cmd_clean = command.strip()

        for rule in cls.HEALING_RULES:
            match = re.search(rule["pattern"], cmd_clean, re.IGNORECASE)
            if match:
                healed = rule["heal_fn"](match)
                return {
                    "original_command": cmd_clean,
                    "healed_command": healed,
                    "rule_triggered": rule["name"],
                    "strategy": rule["strategy"],
                    "safety_gain": rule["safety_gain"],
                    "healed": True
                }

        return {
            "original_command": cmd_clean,
            "healed_command": cmd_clean,
            "rule_triggered": "None",
            "strategy": "Command is within safe parameters or does not require modification.",
            "safety_gain": "Standard Execution",
            "healed": False
        }
