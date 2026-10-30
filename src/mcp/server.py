import sys
import json
import os
from typing import Dict, Any
from src.policy.classifier import PolicyGate
from src.slicer.ast_parser import CodeSlicer
from src.sandbox.executor import SandboxExecutor
from src.bridge.phone_bridge import IQOOPhoneBridge

class CodeShieldMCPServer:
    """
    Standard Model Context Protocol (MCP) Server for CodeShield.
    Enables native integration with modern AI coding environments:
    Cursor, Claude Code, Windsurf, Zed, and Claude Desktop.
    Communicates via JSON-RPC 2.0 over standard I/O (stdio).
    """

    TOOLS = [
        {
            "name": "codeshield_verify_action",
            "description": "Evaluates proposed terminal commands or shell actions using CodeShield's Multi-Tier Policy Gate and on-device Snapdragon NPU validation.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "The exact shell command or script proposed for execution."
                    }
                },
                "required": ["command"]
            }
        },
        {
            "name": "codeshield_slice_context",
            "description": "Performs Tree-Sitter AST context slicing to extract only the target function or method definition, reducing token consumption by over 80%.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Path to the source file to slice."
                    },
                    "line_number": {
                        "type": "integer",
                        "description": "Line number within the method to extract."
                    }
                },
                "required": ["file_path", "line_number"]
            }
        },
        {
            "name": "codeshield_npu_status",
            "description": "Returns the live hardware telemetry of the paired iQOO smartphone and Snapdragon NPU via Office Kit.",
            "inputSchema": {
                "type": "object",
                "properties": {}
            }
        },
        {
            "name": "codeshield_execute_sandboxed",
            "description": "Executes a verified Tier 1 or Tier 2 action strictly inside the isolated CodeShield micro-sandbox.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "Command to execute in sandbox."
                    }
                },
                "required": ["command"]
            }
        }
    ]

    def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        req_id = request.get("id")
        method = request.get("method")
        params = request.get("params", {})

        if method == "initialize":
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {
                        "tools": {}
                    },
                    "serverInfo": {
                        "name": "codeshield-mcp",
                        "version": "2.0.0"
                    }
                }
            }

        elif method == "tools/list":
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "tools": self.TOOLS
                }
            }

        elif method == "tools/call":
            tool_name = params.get("name")
            arguments = params.get("arguments", {})
            return self._call_tool(req_id, tool_name, arguments)

        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "error": {
                "code": -32601,
                "message": f"Method '{method}' not found"
            }
        }

    def _call_tool(self, req_id: Any, name: str, args: Dict[str, Any]) -> Dict[str, Any]:
        if name == "codeshield_verify_action":
            command = args.get("command", "")
            intent = PolicyGate.classify_action(command)
            bridge = IQOOPhoneBridge()
            npu_res = bridge.verify_intent_on_npu(command, intent.tier.name)
            
            content_text = json.dumps({
                "command": command,
                "risk_tier": intent.tier.name,
                "reasoning": intent.reasoning,
                "npu_approved": npu_res["approved_by_npu"],
                "npu_latency_ms": npu_res["npu_latency_ms"],
                "hardware_token": npu_res["hardware_signature"]
            }, indent=2)

            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [{"type": "text", "text": content_text}]
                }
            }

        elif name == "codeshield_slice_context":
            file_path = args.get("file_path", "")
            line_no = args.get("line_number", 1)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    src = f.read()
                slicer = CodeSlicer()
                slice_code = slicer.get_slice_for_line(src, line_no) or "Could not extract slice"
                return {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "content": [{"type": "text", "text": slice_code}]
                    }
                }
            except Exception as e:
                return {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "isError": True,
                    "result": {"content": [{"type": "text", "text": f"Error slicing file: {str(e)}"}]}
                }

        elif name == "codeshield_npu_status":
            bridge = IQOOPhoneBridge()
            dev = bridge.detect_device()
            dev_dict = {
                "device_model": dev.device_model,
                "npu_chipset": dev.npu_chipset,
                "npu_status": dev.npu_status,
                "relay_mode": dev.connection_mode,
                "latency_ms": dev.inference_latency_ms,
                "hardware_key": dev.biometric_hardware_key
            }
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [{"type": "text", "text": json.dumps(dev_dict, indent=2)}]
                }
            }

        elif name == "codeshield_execute_sandboxed":
            command = args.get("command", "")
            intent = PolicyGate.classify_action(command)
            executor = SandboxExecutor()
            success, output = executor.execute(intent, require_human_approval=True)
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [{
                        "type": "text",
                        "text": json.dumps({"success": success, "output": output}, indent=2)
                    }]
                }
            }

        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "error": {"code": -32602, "message": f"Unknown tool name: {name}"}
        }

    def run_stdio(self):
        """Standard stdio loop for MCP clients."""
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue
            try:
                req = json.loads(line)
                resp = self.handle_request(req)
                sys.stdout.write(json.dumps(resp) + "\n")
                sys.stdout.flush()
            except Exception as e:
                err_resp = {
                    "jsonrpc": "2.0",
                    "id": None,
                    "error": {"code": -32700, "message": f"Parse error: {str(e)}"}
                }
                sys.stdout.write(json.dumps(err_resp) + "\n")
                sys.stdout.flush()
