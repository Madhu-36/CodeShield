import os
import stat
from typing import Tuple

PRE_COMMIT_SCRIPT = """#!/bin/sh
# CodeShield Edge-Native Security Pre-Commit Guard
# Intercepts staged git changes before commit to prevent policy violations.

echo "[CodeShield] Running Zero-Trust Pre-Commit Policy Gate..."

# Check staged files for dangerous keywords or unverified commands
STAGED_DIFF=$(git diff --cached --name-only)

if [ -z "$STAGED_DIFF" ]; then
    exit 0
fi

echo "[CodeShield] Inspecting staged changes with ASTra / CodeShield Policy Gate..."

# Quick scan for destructive signatures
if git diff --cached | grep -E "(rm -rf|mkfs|drop database|shutdown -h)" > /dev/null; then
    echo "\\033[0;31m[BLOCKED BY CODESHIELD] High-risk destructive signature detected in staged diff!\\033[0m"
    echo "Action requires explicit Tier 3 authorization from iQOO Hardware Key."
    exit 1
fi

echo "\\033[0;32m[CodeShield] Policy verification PASSED. Commit authorized.\\033[0m"
exit 0
"""

class HookManager:
    """
    Installs and manages repository-level security hooks for CodeShield.
    """
    
    @classmethod
    def install_git_hooks(cls, repo_dir: str = ".") -> Tuple[bool, str]:
        git_dir = os.path.join(repo_dir, ".git")
        if not os.path.exists(git_dir):
            return False, f"Directory '{repo_dir}' is not a git repository (.git folder not found)."
            
        hooks_dir = os.path.join(git_dir, "hooks")
        os.makedirs(hooks_dir, exist_ok=True)
        
        pre_commit_path = os.path.join(hooks_dir, "pre-commit")
        try:
            with open(pre_commit_path, "w", encoding="utf-8", newline="\n") as f:
                f.write(PRE_COMMIT_SCRIPT)
                
            # Make executable on Unix/Mac/WSL
            st = os.stat(pre_commit_path)
            os.chmod(pre_commit_path, st.st_mode | stat.S_IEXEC)
            
            return True, f"Successfully installed CodeShield Pre-Commit Guard at {pre_commit_path}"
        except Exception as e:
            return False, f"Failed to install git hook: {str(e)}"
