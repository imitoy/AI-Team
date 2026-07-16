"""run_command tool — execute a shell command."""

name = "run_command"
description = 'Run a shell command. Input: {"command": "ls -l", "detach": false}'
schema = {
    "type": "function",
    "function": {
        "name": "run_command",
        "description": 'Run a shell command. Input: {"command": "ls -l", "detach": false}',
        "parameters": {
            "type": "object",
            "properties": {
                "command": {"type": "string", "description": "The shell command to run"},
                "detach": {"type": "boolean", "description": "Whether to detach the process for long-running commands"},
            },
            "required": ["command"],
        },
    },
}


def action(input: dict) -> dict:
    from communication import ask_proceed

    command = input.get("command", "")
    detach = input.get("detach", False)
    print(f"\033[0;36mRunning command: {command}")
    if not ask_proceed("run_command"):
        return {"success": False, "content": "Command execution denied by user"}
    import subprocess
    try:
        if detach:
            subprocess.Popen(command, shell=True, start_new_session=True)
            return {"success": True, "content": "Command started in background"}
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=120)
        output = result.stdout + result.stderr
        return {"success": True, "content": output if output else "(no output)"}
    except subprocess.TimeoutExpired:
        return {"success": False, "content": "Command timed out"}
    except Exception as e:
        return {"success": False, "content": f"Failed to run command: {e}"}
