"""kill_process tool — kill a detached process by ID (stub)."""

name = "kill_process"
description = 'Kill a detached process. Input: {"id": "pid"}'
schema = {
    "type": "function",
    "function": {
        "name": "kill_process",
        "description": 'Kill a detached process. Input: {"id": "pid"}',
        "parameters": {
            "type": "object",
            "properties": {
                "id": {"type": "string", "description": "The process ID to kill"},
            },
            "required": ["id"],
        },
    },
}


def action(input: dict) -> dict:
    from communication import ask_proceed
    if not ask_proceed("kill_process"):
        return {"success": False, "content": "Command execution denied by user"}
    # Stub — in the Lua version this was incomplete too
    return {"success": True, "content": "Process killed (stub)"}
