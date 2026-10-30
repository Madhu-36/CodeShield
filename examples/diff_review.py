import os
from src.slicer.ast_parser import CodeSlicer
from src.engine.explainer import EvidenceEngine

def main():
    """
    Demonstrates a simulated CI/webhook flow where a PR introduces a change.
    Instead of passing the entire file to the model, we use AST slicing.
    """
    print("=== CodeShield Dev: End-to-End Diff Review Example ===")
    
    # 1. Simulate a target file
    sample_file = "sample_target.py"
    sample_code = """
class AuthenticationManager:
    def login(self, username, password):
        # TODO: Implement secure hashing
        if username == "admin" and password == "admin":
            return True
        return False
        
    def logout(self):
        print("Logged out")
        
def utils_helper():
    pass
"""
    with open(sample_file, "w") as f:
        f.write(sample_code)
        
    print(f"1. Simulated a PR diff modifying line 4 in '{sample_file}'.")
    
    # 2. Extract Method Slice
    slicer = CodeSlicer()
    slice_content = slicer.get_slice_for_line(sample_code, 4)
    
    print("\n2. Method-Level AST Extraction:")
    print("Instead of sending 2000 lines of file context, we isolate:")
    print("-" * 40)
    print(slice_content)
    print("-" * 40)
    
    # 3. Simulate an LLM generating a local verification command (e.g., bandit security scan)
    action = f"bandit -r {sample_file}"
    print(f"\n3. Assistant proposes security action: `{action}`")
    
    # 4. Generate Grounded Explanation
    print("\n4. Explanation Engine Output:")
    explanation = EvidenceEngine.generate_explanation(
        action=action,
        success=True,
        output="[INFO] Bandit analysis complete. Found 1 issue: Hardcoded password.",
        ast_context=slice_content
    )
    print(explanation)
    
    # Cleanup
    os.remove(sample_file)

if __name__ == "__main__":
    main()

