"""list_files tool — list all files recursively."""

name = "list_files"
description = "List all files in the current directory recursively"
schema = {
    "type": "function",
    "function": {
        "name": "list_files",
        "description": "List all files in the current directory recursively",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
        },
    },
}


def action(input: dict) -> dict:
    import subprocess
    try:
        result = subprocess.run(["ls", "-R"], capture_output=True, text=True, timeout=10)
        return {"success": True, "content": result.stdout}
    except Exception as e:
        return {"success": False, "content": f"Failed to list files: {e}"}
