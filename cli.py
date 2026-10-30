import typer
from rich.console import Console
from src.slicer.ast_parser import CodeSlicer
from src.policy.classifier import PolicyGate, RiskTier
from src.sandbox.executor import SandboxExecutor
from src.engine.explainer import EvidenceEngine

app = typer.Typer(help="CodeShield Dev: Security-First, Repository-Local Action Layer")
console = Console()

@app.command()
def execute(command: str, force: bool = typer.Option(False, "--force", "-f", help="Force execution of Tier 3 commands")):
    """
    Evaluates and safely executes a local repository command.
    """
    console.print(f"[bold blue]Evaluating intent for action:[/bold blue] {command}")
    
    # 1. Classify Action
    intent = PolicyGate.classify_action(command)
    
    tier_color = "green" if intent.tier == RiskTier.TIER_1 else "yellow" if intent.tier == RiskTier.TIER_2 else "red"
    console.print(f"Risk Assessment: [bold {tier_color}]{intent.tier.name}[/bold {tier_color}] - {intent.reasoning}")
    
    # 2. Gate Execution
    executor = SandboxExecutor()
    require_approval = not force
    
    success, output = executor.execute(intent, require_human_approval=require_approval)
    
    # 3. Generate Explanation Evidence
    explanation = EvidenceEngine.generate_explanation(
        action=intent.action,
        success=success,
        output=output
    )
    
    console.print(explanation)

@app.command()
def review(file_path: str, line_number: int):
    """
    Performs a method-level review of a specific file and line.
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
def serve(host: str = "127.0.0.m0.1", port: int = 8000):
    """
    Starts the GitHub Webhook CI/CD server.
    """
    import uvicorn
    console.print(f"[bold green]Starting Webhook Server on {host}:{port}...[/bold green]")
    uvicorn.run("src.server.webhook:app", host=host.replace(".m0", ""), port=port, reload=True)

if __name__ == "__main__":
    app()

