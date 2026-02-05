import subprocess

def execute_terminal(command: str):
    """
    Executes a shell command on the host system.
    
    CRITICAL: This function forces a user confirmation step before execution.
    """
    print(f"[System]: Agent wants to run: '{command}'. Allow? (y/n): ", end="")
    user_input = input().strip().lower()
    
    if user_input != 'y':
        return "Error: Command denied by user."
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        output_parts = [
            f"EXIT CODE: {result.returncode}",
            f"STDOUT: {result.stdout.strip()}",
            f"STDERR: {result.stderr.strip()}"
        ]
        
        return "\n".join(output_parts)
    except Exception as e:
        return f"Error executing command: {str(e)}"
