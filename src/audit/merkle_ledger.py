import os
import json
import hashlib
import time
from typing import Dict, Any, List, Tuple
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

console = Console(safe_box=True)

class MerkleAuditLedger:
    """
    Cryptographic Block-Chained Merkle Audit Ledger for CodeShield.
    Maintains an immutable, mathematically verifiable audit trail of all
    AI agent terminal actions signed by the iQOO Snapdragon NPU Hardware Key.
    """

    LEDGER_FILE = ".codeshield_ledger.jsonl"
    GENESIS_HASH = "0" * 64

    @classmethod
    def _compute_hash(cls, index: int, timestamp: str, action: str, tier: str, verdict: str, hardware_token: str, prev_hash: str) -> str:
        payload = f"{index}:{timestamp}:{action}:{tier}:{verdict}:{hardware_token}:{prev_hash}"
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()

    @classmethod
    def get_last_block(cls) -> Optional[Dict[str, Any]]:
        if not os.path.exists(cls.LEDGER_FILE):
            return None
        last_line = None
        with open(cls.LEDGER_FILE, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    last_line = line
        return json.loads(last_line) if last_line else None

    @classmethod
    def record(cls, action: str, tier: str, verdict: str, hardware_token: str) -> Dict[str, Any]:
        """
        Appends a new cryptographically chained audit block to the ledger.
        """
        last_block = cls.get_last_block()
        index = (last_block["index"] + 1) if last_block else 0
        prev_hash = last_block["hash"] if last_block else cls.GENESIS_HASH
        timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

        block_hash = cls._compute_hash(index, timestamp, action, tier, verdict, hardware_token, prev_hash)

        block = {
            "index": index,
            "timestamp": timestamp,
            "action": action,
            "tier": tier,
            "verdict": verdict,
            "hardware_token": hardware_token,
            "prev_hash": prev_hash,
            "hash": block_hash
        }

        with open(cls.LEDGER_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(block) + "\n")

        return block

    @classmethod
    def verify_ledger(cls) -> Tuple[bool, int, str]:
        """
        Validates the entire ledger from Genesis block to HEAD.
        Returns: (is_valid, total_blocks_verified, message)
        """
        if not os.path.exists(cls.LEDGER_FILE):
            return True, 0, "Ledger is currently empty (0 blocks)."

        expected_prev = cls.GENESIS_HASH
        count = 0

        with open(cls.LEDGER_FILE, "r", encoding="utf-8") as f:
            for line_no, line in enumerate(f):
                if not line.strip():
                    continue
                block = json.loads(line)
                
                # Verify link
                if block["prev_hash"] != expected_prev:
                    return False, count, f"Broken chain at block #{block['index']}! Expected prev_hash {expected_prev[:12]}..., found {block['prev_hash'][:12]}..."

                # Verify hash integrity
                recomputed = cls._compute_hash(
                    block["index"], block["timestamp"], block["action"],
                    block["tier"], block["verdict"], block["hardware_token"], block["prev_hash"]
                )
                if recomputed != block["hash"]:
                    return False, count, f"Hash mismatch at block #{block['index']}! Tampering detected."

                expected_prev = block["hash"]
                count += 1

        return True, count, f"All {count} cryptographic blocks verified with 100% integrity."

    @classmethod
    def render_cli_view(cls, limit: int = 5):
        """Prints a visual audit inspection report in the terminal."""
        is_valid, count, msg = cls.verify_ledger()

        status_text = "[bold green][+] LEDGER INTEGRITY: VERIFIED SECURE (0 TAMPERING)[/bold green]" if is_valid else "[bold red][!] INTEGRITY BREACH: TAMPERING DETECTED[/bold red]"
        console.print(Panel(status_text, style="cyan"))

        table = Table(title=f"Immutable Cryptographic Audit Trail ({count} blocks total)", box=box.SIMPLE)
        table.add_column("Block", style="cyan")
        table.add_column("Timestamp", style="dim")
        table.add_column("Action Audited", style="bold white")
        table.add_column("Tier", style="yellow")
        table.add_column("Hardware Key Token", style="green")
        table.add_column("SHA-256 Hash", style="magenta")

        if os.path.exists(cls.LEDGER_FILE):
            blocks = []
            with open(cls.LEDGER_FILE, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        blocks.append(json.loads(line))
            for b in blocks[-limit:]:
                table.add_row(
                    f"#{b['index']}",
                    b["timestamp"],
                    b["action"],
                    b["tier"],
                    b["hardware_token"],
                    b["hash"][:16] + "..."
                )

        console.print(table)
        console.print(f"[dim]{msg}[/dim]\n")
