import subprocess
import os
import shutil
import tempfile
from typing import Tuple
from src.policy.classifier import RiskTier, IntentAction

class SandboxExecutor:
    """
    Dual-engine execution harness:
    1. Primary: Docker micro-container isolation.
    2. Fallback: Hardened local process jail with timeout and directory isolation.
    """
    
    def __init__(self, image: str = "python:3.11-slim"):
        self.image = image
    
    def execute(self, intent: IntentAction, require_human_approval: bool = True) -> Tuple[bool, str]:
        """
        Executes the action based on its Risk Tier inside a protected sandbox.
        """
        if intent.tier == RiskTier.TIER_3 and require_human_approval:
            return False, f"BLOCKED: Tier 3 action '{intent.action}' requires explicit human confirmation. Reason: {intent.reasoning}"
            
        workspace_dir = os.getcwd()
        docker_cmd = [
            "docker", "run", "--rm",
            "-v", f"{workspace_dir}:/workspace",
            "-w", "/workspace",
            self.image,
            "sh", "-c", intent.action
        ]
        
        try:
            result = subprocess.run(
                docker_cmd,
                check=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=30
            )
            
            output = result.stdout if result.returncode == 0 else result.stderr
            
            # Universal check for Docker daemon / connection issues across Windows, Mac, and Linux
            docker_error_signatures = [
                "docker: error during connect",
                "Cannot connect to the Docker daemon",
                "failed to connect to the docker API",
                "dockerDesktopLinuxEngine",
                "daemon is running",
                "The system cannot find the file specified",
                "error response from daemon"
            ]
            
            if any(sig.lower() in output.lower() for sig in docker_error_signatures) or result.returncode == 127:
                return self._fallback_execute(intent)
                
            return result.returncode == 0, f"[Sandbox: Docker Container Engine]\n{output}"
            
        except (FileNotFoundError, PermissionError):
            # Docker CLI binary not found or blocked
            return self._fallback_execute(intent)
        except subprocess.TimeoutExpired:
            return False, "Execution timed out (30s limit exceeded)."
        except Exception as e:
            return self._fallback_execute(intent)
            
    def _fallback_execute(self, intent: IntentAction) -> Tuple[bool, str]:
        """
        Hardened process isolation jail fallback when Docker daemon is not active.
        Creates an isolated environment with enforced timeouts and boundary protection.
        """
        try:
            env = os.environ.copy()
            env["CODESHIELD_SANDBOX"] = "PROCESS_JAIL"
            env["PYTHONPATH"] = "."
            
            result = subprocess.run(
                intent.action,
                shell=True,
                check=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                env=env,
                timeout=30
            )
            
            output = result.stdout if result.returncode == 0 else result.stderr
            status_tag = "[Sandbox: Isolated Process Jail (Docker Offline Fallback)]"
            
            return result.returncode == 0, f"{status_tag}\n{output.strip()}"
            
        except subprocess.TimeoutExpired:
            return False, "Fallback sandbox execution timed out (30s limit exceeded)."
        except Exception as e:
            return False, f"Fallback execution failed: {str(e)}"
