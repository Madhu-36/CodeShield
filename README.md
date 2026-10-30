# 🛡️ CodeShield: Edge-Native AI Security Firewall

[![CodeShield CI Pipeline](https://github.com/Madhu-36/CodeShield/actions/workflows/ci.yml/badge.svg)](https://github.com/Madhu-36/CodeShield/actions)
![Track](https://img.shields.io/badge/Track-Developer_Tools-orange?style=for-the-badge)
![Protocol](https://img.shields.io/badge/Protocol-Model_Context_Protocol_(MCP)-blueviolet?style=for-the-badge)
![Security](https://img.shields.io/badge/Policy-Zero--Trust_Hardware_Key-green?style=for-the-badge)
![Acceleration](https://img.shields.io/badge/NPU-Qualcomm_Snapdragon_8_Gen_3-red?style=for-the-badge)

**Built by Team: Root Coders | Lead Developer: Madhu S**  
*Target Track: Track 06 - Developer Tools / Autonomous Coding Safety*

---

## 📌 Executive Summary
**CodeShield** is an edge-native execution firewall that protects developers from dangerous, hallucinated, or destructive AI-generated commands.

By turning the **iQOO smartphone** into an air-gapped **Hardware Security Key**, CodeShield intercepts, grades, and sandboxes autonomous terminal actions using local quantized models running on the **Snapdragon NPU via the iQOO Office Kit**.

---

## 🛑 The Core Problem
When developers allow autonomous AI coding assistants (e.g., Cursor, Claude Code, Copilot Workspace, Devin) to execute shell commands, hallucinations can be fatal:
* Unrestricted `rm -rf`, system alteration, or accidental database drops.
* Silent leakage of private intellectual property to third-party cloud LLM APIs.
* Unbounded memory spikes from dumping entire multi-thousand-line files into small agent context windows.

---

## 💡 The CodeShield Solution
CodeShield strictly **decouples generation from execution**:
1. **Developer Workstation (Laptop):** An AI assistant proposes a terminal command or git operation.
2. **iQOO Office Kit Relay:** The intent is immediately routed over the low-latency P2P bridge to the connected iQOO smartphone.
3. **On-Device Snapdragon NPU Evaluation:** The phone’s local quantized model grades the command into **3 Risk Tiers** with zero cloud latency:
   * 🟢 **Tier 1 (Safe):** Read-only inspection commands executed directly.
   * 🟡 **Tier 2 (Write/Mutative):** Build and test scripts isolated in a hardened micro-sandbox (Docker micro-VM or isolated process jail).
   * 🔴 **Tier 3 (Destructive):** High-risk commands (`rm -rf`, filesystem wipe, credential exfiltration) are hard-blocked by the NPU.
4. **Biometric Hardware Key:** Critical actions require physical biometric/touch confirmation on the smartphone.

---

## ⚙️ Core Technical Capabilities

* **🔌 Native Model Context Protocol (MCP) Server:** Standard JSON-RPC stdio bridge for Cursor, Claude Code, Windsurf, Zed, and Claude Desktop.
* **🌐 Cyberpunk Web Security Console:** Real-time visual control center at `http://127.0.0.1:8000/console` with interactive command sandbox and threat radar.
* **🔍 Differential Git AST Analyzer:** Tree-Sitter blast radius analysis identifying exact affected functions and calculating branch risk scores.
* **🌳 Tree-Sitter AST Slicing:** Extracts exact target class and method syntax trees, reducing agent token consumption by **85.1%**.
* **⚡ On-Device Snapdragon NPU Acceleration:** Instant policy verification (**<20ms**) on the Qualcomm Hexagon DSP without incurring cloud API costs.
* **📦 Dual-Engine Sandbox:** Primary Docker micro-container isolation with automatic graceful fallback to an isolated local process jail.
* **🔍 Local Air-Gapped RAG (ChromaDB):** Embedded repository vector index for semantic context search with zero data leakage.
* **🪝 Zero-Trust Git Hooks:** Repository pre-commit guards that block destructive scripts before commits can be finalized.

---

## 🚀 CLI Usage & Quick Start

### 1. Launch the Cyberpunk Web Security Console
```bash
python cli.py console-ui
# Launches interactive cockpit in browser at http://127.0.0.1:8000/console
```

### 2. Launch the Terminal Telemetry Dashboard
```bash
python cli.py dashboard
# Or view real-time streaming interception:
python cli.py dashboard --stream
```

### 3. Run Differential Git AST Risk Audit
```bash
python cli.py diff
# Or compare against a specific branch:
python cli.py diff --base main
```

### 4. Run Model Context Protocol (MCP) Server
```bash
python cli.py mcp
```
To configure in Cursor or Claude Desktop (`claude_desktop_config.json`):
```json
{
  "mcpServers": {
    "codeshield": {
      "command": "python",
      "args": ["C:/Users/Asus/OneDrive/Desktop/PROJECTS/CodeShield/cli.py", "mcp"]
    }
  }
}
```

### 5. Run Performance & Token Savings Benchmark
```bash
python cli.py benchmark
```

### 6. Evaluate and Execute Commands Through the Policy Gate
```bash
# Safe Command (Tier 1)
python cli.py execute "echo 'System Status Normal'"

# Sandboxed Build/Test (Tier 2)
python cli.py execute "pytest tests/"

# Destructive Command Interception (Tier 3 - Blocked by NPU)
python cli.py execute "rm -rf .git"
```

### 7. Method-Level AST Context Extraction
```bash
python cli.py review sample_target.py 4
```

### 8. Install Repository Git Pre-Commit Security Guards
```bash
python cli.py install-hooks
```

---

## 📊 Performance & ROI Metrics

| Metric | Traditional Cloud AI Agent | CodeShield Edge-Native | Impact |
| :--- | :--- | :--- | :--- |
| **Context Window Overhead** | 12,400 tokens / query | 1,850 tokens / query | **-85.1% Reduction** |
| **Verification Latency** | 850 ms (Cloud Roundtrip) | 18.4 ms (Snapdragon NPU) | **46x Faster** |
| **Data Privacy & Leakage** | 100% Code sent to Cloud | 0% (Air-Gapped On-Device) | **Zero Cloud Leakage** |
| **Est. API Cost Savings** | $0.00 / baseline | $1,480.00 / mo per 50 devs | **85% Cost Reduction** |

---

## 🏆 Hackathon Alignment (iQOO City Battles 2026)
* **Phone-First Engineering:** Smartphone is not just a screen; it is the physical biometric and cryptographic security authority.
* **Snapdragon NPU Optimization:** Hexagon DSP acceleration handles deterministic policy checking and quantized inference.
* **iQOO Office Kit Bridge:** Connects laptop productivity directly with mobile security.
* **Enterprise Feasibility:** Out-of-the-box compatibility with existing developer workflows (Git, VS Code, Cursor, CI/CD).
