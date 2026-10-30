import sys
import webbrowser
import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box
from src.slicer.ast_parser import CodeSlicer
from src.slicer.diff_analyzer import GitDiffASTAnalyzer
from src.policy.classifier import PolicyGate, RiskTier
from src.sandbox.executor import SandboxExecutor
from src.engine.explainer import EvidenceEngine
from src.engine.healer import SelfHealingEngine
from src.audit.merkle_ledger import MerkleAuditLedger
from src.security.canary import CanaryTrapEngine
from src.bridge.phone_bridge import IQOOPhoneBridge
from src.bridge.voice_auth import VoiceBiometricBridge
from src.ui.dashboard import CodeShieldDashboard
from src.benchmark.runner import BenchmarkRunner
from src.hooks.manager import HookManager
from src.mcp.server import CodeShieldMCPServer

# Safe terminal encoding on Windows
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

app = typer.Typer(help="CodeShield Dev: Security-First, Repository-Local Action Layer")
console = Console(safe_box=True)

@app.command()
def execute(command: str, force: bool = typer.Option(False, "--force", "-f", help="Force execution of Tier 3 commands")):
    """
    Evaluates and safely executes a local repository command with audit ledger & canary checks.
    """
    # 0. Canary Honeytoken Inspection
    canary_leak = CanaryTrapEngine.inspect_for_canary_leak(command)
    if canary_leak:
        console.print(Panel(f"[bold red][!] {canary_leak['alert']}[/bold red]\n{canary_leak['reason']}\n{canary_leak['action_taken']}", style="red"))
        MerkleAuditLedger.record(command, "CANARY_BREACH", "LOCKED_DOWN", "EMERGENCY-NPU-ISOLATION")
        return

    console.print(f"[bold blue]Evaluating intent for action:[/bold blue] {command}")
    
    # 1. Classify Action
    intent = PolicyGate.classify_action(command)
    
    tier_color = "green" if intent.tier == RiskTier.TIER_1 else "yellow" if intent.tier == RiskTier.TIER_2 else "red"
    console.print(f"Risk Assessment: [bold {tier_color}]{intent.tier.name}[/bold {tier_color}] - {intent.reasoning}")
    
    # 2. Gate Execution
    executor = SandboxExecutor()
    require_approval = not force
    
    success, output = executor.execute(intent, require_human_approval=require_approval)
    
    # 3. Record in Cryptographic Merkle Audit Ledger
    bridge = IQOOPhoneBridge()
    npu_res = bridge.verify_intent_on_npu(command, intent.tier.name)
    MerkleAuditLedger.record(
        action=command,
        tier=intent.tier.name,
        verdict="SUCCESS" if success else "BLOCKED",
        hardware_token=npu_res["hardware_signature"]
    )
    
    # 4. Generate Explanation Evidence
    explanation = EvidenceEngine.generate_explanation(
        action=intent.action,
        success=success,
        output=output
    )
    
    console.print(explanation)

@app.command()
def heal(command: str = typer.Argument(..., help="Dangerous command to auto-heal into a safe alternative")):
    """
    Autonomous Self-Healing: Rewrites destructive commands into safe, non-destructive equivalents.
    """
    res = SelfHealingEngine.heal_action(command)
    
    if res["healed"]:
        console.print(Panel("[bold green][+] COMMAND HEALED AUTOMATICALLY BY CODESHIELD NPU[/bold green]", style="green"))
    else:
        console.print(Panel("[bold cyan][*] COMMAND DOES NOT REQUIRE HEALING[/bold cyan]", style="cyan"))
        
    table = Table(box=box.SIMPLE)
    table.add_column("Parameter", style="bold white")
    table.add_column("Details", style="cyan")
    
    table.add_row("Original Proposed", res["original_command"])
    table.add_row("Healed Alternative", f"[bold green]{res['healed_command']}[/bold green]")
    table.add_row("Strategy Applied", res["strategy"])
    table.add_row("Safety Benefit", f"[bold yellow]{res['safety_gain']}[/bold yellow]")
    console.print(table)

@app.command()
def audit(limit: int = typer.Option(5, "--limit", "-l", help="Number of recent ledger blocks to display")):
    """
    Inspects the cryptographic Merkle-Tree audit ledger signed by the iQOO Hardware Key.
    """
    MerkleAuditLedger.render_cli_view(limit)

@app.command()
def audit_verify():
    """
    Mathematically verifies the complete cryptographic hash chain of the audit ledger.
    """
    valid, count, msg = MerkleAuditLedger.verify_ledger()
    if valid:
        console.print(f"[bold green][+] Audit Ledger Integrity Verified: {msg}[/bold green]")
    else:
        console.print(f"[bold red][!] Audit Breach Detected: {msg}[/bold red]")

@app.command()
def canary():
    """
    Displays the active Canary Honeytokens and prompt injection defense status.
    """
    CanaryTrapEngine.render_cli_status()

@app.command()
def voice_auth(
    passphrase: str = typer.Argument(..., help="Voice passphrase spoken into iQOO phone (e.g. 'Authorize Push')"),
    action: str = typer.Option("Tier 3 Privileged Action", "--action", "-a", help="Action being authorized")
):
    """
    Simulates voice-biometric acoustic verification on the iQOO phone via Snapdragon NPU.
    """
    VoiceBiometricBridge.render_cli_view(passphrase, action)

@app.command()
def review(file_path: str, line_number: int):
    """
    Performs a method-level review of a specific file and line using Tree-Sitter AST slicing.
    """
    console.print(f"[bold blue]Extracting method slice for {file_path}:{line_number}[/bold blue]")
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            source = f.read()
    except FileNotFoundError:
        console.print(f"[bold red]File not found:[/bold red] {file_path}")
        return
        
    slicer = CodeSlicer()
    slice_content = slicer.get_slice_for_line(source, line_number)
    
    if slice_content:
        console.print(f"\n[bold green]Extracted AST Context:[/bold green]\n```python\n{slice_content}\n```")
    else:
        console.print("[yellow]Could not determine method slice for given line.[/yellow]")

@app.command()
def diff(base: str = typer.Option("HEAD~1", "--base", "-b", help="Git reference to compare against (e.g. main, HEAD~1)")):
    """
    Performs differential AST risk analysis across modified branch files.
    """
    GitDiffASTAnalyzer.render_cli_report(base)

@app.command()
def dashboard(stream: bool = typer.Option(False, "--stream", "-s", help="Run animated live intercept feed")):
    """
    Displays the interactive CodeShield terminal telemetry dashboard and phone status.
    """
    if stream:
        CodeShieldDashboard.run_live_stream()
    else:
        CodeShieldDashboard.render_static_overview()

@app.command()
def benchmark():
    """
    Runs empirical performance, token savings, and NPU latency benchmarks.
    """
    BenchmarkRunner.run_all()

@app.command()
def bridge():
    """
    Inspects and tests connection to the iQOO smartphone via Office Kit / ADB.
    """
    bridge_inst = IQOOPhoneBridge()
    dev = bridge_inst.detect_device()
    console.print(f"[bold green][+] Paired Device:[/bold green] {dev.device_model}")
    console.print(f"[bold cyan]    AI Chipset:[/bold cyan] {dev.npu_chipset}")
    console.print(f"[bold cyan]    NPU Status:[/bold cyan] {dev.npu_status}")
    console.print(f"[bold cyan]    Relay Mode:[/bold cyan] {dev.connection_mode}")
    console.print(f"[bold cyan]    On-Device Latency:[/bold cyan] {dev.inference_latency_ms} ms")
    console.print(f"[bold cyan]    Biometric Key:[/bold cyan] {dev.biometric_hardware_key}")

@app.command()
def mcp():
    """
    Starts the native Model Context Protocol (MCP) server over stdio for Cursor, Claude Code, and Windsurf.
    """
    server = CodeShieldMCPServer()
    server.run_stdio()

@app.command()
def install_hooks(repo: str = typer.Option(".", "--repo", "-r", help="Path to git repository")):
    """
    Installs CodeShield Zero-Trust Pre-Commit Git Hooks.
    """
    ok, msg = HookManager.install_git_hooks(repo)
    if ok:
        console.print(f"[bold green][+] {msg}[/bold green]")
    else:
        console.print(f"[bold red][-] {msg}[/bold red]")

@app.command()
def index(directory: str = "."):
    """
    Indexes the specified directory into the local RAG database.
    """
    from src.retrieval.rag_index import LocalRepositoryRAG
    console.print(f"[bold blue]Indexing directory:[/bold blue] {directory}")
    rag = LocalRepositoryRAG()
    count = rag.index_directory(directory)
    console.print(f"[bold green]Successfully indexed {count} method/class slices into ChromaDB.[/bold green]")

@app.command()
def console_ui(host: str = "127.0.0.1", port: int = 8000, open_browser: bool = typer.Option(True, "--open/--no-open", help="Open browser automatically")):
    """
    Launches the Cyberpunk Web Security Console in the browser.
    """
    import uvicorn
    url = f"http://{host}:{port}/console"
    console.print(f"[bold cyan][+] Launching CodeShield Web Security Console at:[/bold cyan] {url}")
    if open_browser:
        webbrowser.open(url)
    uvicorn.run("src.server.webhook:app", host=host, port=port, reload=False)

@app.command()
def serve(host: str = "127.0.0.1", port: int = 8000):
    """
    Starts the CodeShield Gateway Webhook & Web Console Server.
    """
    import uvicorn
    console.print(f"[bold green][+] Starting CodeShield Webhook Server on {host}:{port}...[/bold green]")
    console.print(f"[bold cyan][+] Web Security Console available at: http://{host}:{port}/console[/bold cyan]")
    uvicorn.run("src.server.webhook:app", host=host, port=port, reload=True)

if __name__ == "__main__":
    app()
