from fastapi import FastAPI, Request
from pydantic import BaseModel
from src.slicer.ast_parser import CodeSlicer
from src.engine.explainer import EvidenceEngine

app = FastAPI(title="CodeShield Webhook Server", description="CI/CD GitHub PR Integration")
slicer = CodeSlicer()

class PRPayload(BaseModel):
    action: str
    pull_request: dict
    repository: dict

@app.post("/webhook")
async def handle_github_webhook(request: Request):
    """
    Endpoint to receive GitHub Webhook payloads on Pull Request.
    """
    payload = await request.json()
    action = payload.get("action")
    
    if action not in ["opened", "synchronize"]:
        return {"status": "ignored", "reason": f"Action {action} not processed"}
        
    # In a real scenario, we would fetch the diff from GitHub API using the PR number.
    # For this prototype, we'll simulate fetching a file and slicing it.
    
    # Simulate a file being changed
    sample_file = "sample_target.py"
    try:
        with open(sample_file, "r", encoding="utf-8") as f:
            source = f.read()
    except FileNotFoundError:
        return {"status": "error", "message": f"{sample_file} not found locally to simulate diff."}
        
    # Simulate the diff was on line 4
    slice_content = slicer.get_slice_for_line(source, 4)
    
    if slice_content:
        # Generate an explanation / review comment based on the slice
        # In a real implementation, this is where we would pass the slice to the local RAG 
        # and an LLM to generate a review.
        review_comment = EvidenceEngine.generate_explanation(
            action="Automated AST Review",
            success=True,
            output="[INFO] Extracted method-level slice for review. Ready for LLM processing.",
            ast_context=slice_content
        )
        return {"status": "success", "review_comment": review_comment}
        
    return {"status": "error", "message": "Could not determine AST slice."}
