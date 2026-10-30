import time
import sys
import subprocess
import os

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def type_text(text, speed=0.06, delay_after=0.8):
    """Simulates realistic human typing in the terminal."""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(speed)
    time.sleep(delay_after)
    print()

def run_step(description, command):
    print(f"\n\033[96m=== {description} ===\033[0m")
    time.sleep(1.5)
    sys.stdout.write("PS C:\\Users\\Asus\\Desktop\\PROJECTS\\CodeShield> ")
    sys.stdout.flush()
    time.sleep(0.8)
    
    type_text(command)
    
    print("\033[90m[Executing via CodeShield Edge-Native Policy Gate...]\033[0m\n")
    time.sleep(0.5)
    
    env = os.environ.copy()
    env["PYTHONPATH"] = "."
    
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, env=env)
    for line in process.stdout:
        sys.stdout.write(line)
        sys.stdout.flush()
        time.sleep(0.02)
        
    process.wait()
    time.sleep(2)

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print("\n\033[92m[CodeShield Edge-Native Security Firewall - Live Walkthrough Initialized]\033[0m\n")
    time.sleep(2)
    
    # Step 1: Telemetry Dashboard & iQOO Phone Bridge
    run_step(
        "DEMO 1: iQOO Office Kit Telemetry & Snapdragon NPU Status",
        ".\\venv\\Scripts\\python.exe cli.py dashboard"
    )
    
    # Step 2: Tier 1 Safe Execution
    run_step(
        "DEMO 2: Tier 1 (Safe) Read-Only Command Evaluation",
        ".\\venv\\Scripts\\python.exe cli.py execute \"echo 'System Status Normal'\""
    )
    
    # Step 3: Tier 3 Destructive Interception
    run_step(
        "DEMO 3: Tier 3 (Destructive) Real-Time Interception & NPU Blocking",
        ".\\venv\\Scripts\\python.exe cli.py execute \"rm -rf .git\""
    )
    
    # Step 4: Tree-sitter AST Slicing
    run_step(
        "DEMO 4: Tree-Sitter AST Context Slicing (Context Optimization)",
        ".\\venv\\Scripts\\python.exe cli.py review sample_target.py 4"
    )
    
    # Step 5: Benchmark Suite
    run_step(
        "DEMO 5: Quantitative ROI, Token Savings & NPU Speed Benchmark",
        ".\\venv\\Scripts\\python.exe cli.py benchmark"
    )
    
    # Step 6: Git Hook Security Guard
    run_step(
        "DEMO 6: Zero-Trust Pre-Commit Git Security Guard Installation",
        ".\\venv\\Scripts\\python.exe cli.py install-hooks"
    )
    
    print("\n\033[92m[Demonstration Complete. CodeShield fully operational on Snapdragon NPU & iQOO Office Kit.]\033[0m\n")

if __name__ == "__main__":
    main()
