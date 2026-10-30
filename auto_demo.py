import time
import sys
import subprocess
import os

def type_text(text, speed=0.08, delay_after=1.0):
    """Simulates human typing in the terminal."""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(speed)
    time.sleep(delay_after)
    print()

def run_step(description, command):
    print(f"\n\033[96m=== {description} ===\033[0m")
    time.sleep(2)
    sys.stdout.write("PS C:\\Users\\Asus\\Desktop\\PROJECTS\\CodeShield> ")
    sys.stdout.flush()
    time.sleep(1)
    
    type_text(command)
    
    # Execute the actual command
    print("\033[90m[Executing via CodeShield Policy Gate...]\033[0m\n")
    time.sleep(1)
    
    # Ensure PYTHONPATH is set so 'src' module can be imported
    env = os.environ.copy()
    env["PYTHONPATH"] = "."
    
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, env=env)
    for line in process.stdout:
        sys.stdout.write(line)
        sys.stdout.flush()
        time.sleep(0.05) # slight delay for cinematic effect
        
    process.wait()
    time.sleep(3)

def main():
    # Clear screen for a clean recording
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print("\n\033[92m[CodeShield Edge-Native Security Firewall - Live Demo initialized]\033[0m\n")
    time.sleep(3)
    
    # Demo 1: Safe Command
    run_step(
        "DEMO 1: Tier 1 (Safe) Command Execution",
        ".\\venv\\Scripts\\python.exe cli.py execute \"echo 'System Status Normal'\""
    )
    
    # Demo 2: Destructive Command
    run_step(
        "DEMO 2: Tier 3 (Destructive) Interception",
        ".\\venv\\Scripts\\python.exe cli.py execute \"rm -rf .git\""
    )
    
    # Demo 3: Context Slicing
    run_step(
        "DEMO 3: Tree-Sitter AST Method Extraction",
        ".\\venv\\Scripts\\python.exe cli.py review sample_target.py 4"
    )
    
    # Demo 4: Tier 2 (Write/Sandbox) Command
    run_step(
        "DEMO 4: Tier 2 (Write) Sandboxed Execution",
        ".\\venv\\Scripts\\python.exe cli.py execute \"pytest tests/\""
    )
    
    # Demo 5: RAG Semantic Indexing
    run_step(
        "DEMO 5: Local RAG Database Indexing",
        ".\\venv\\Scripts\\python.exe cli.py index ."
    )
    
    print("\n\033[92m[End of Demonstration. Handing control back to iQOO Office Kit.]\033[0m\n")

if __name__ == "__main__":
    main()
