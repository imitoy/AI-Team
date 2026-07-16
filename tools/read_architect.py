"""read_architect tool — read ARCHITECT.md."""

name = "read_architect"
description = "Read ARCHITECT.md design document"
schema = {
    "type": "function",
    "function": {
        "name": "read_architect",
        "description": "Read ARCHITECT.md design document",
        "parameters": {"type": "object", "properties": {}, "required": []},
    },
}


def action(input: dict) -> dict:
    try:
        with open("ARCHITECT.md", "r") as f:
            content = f.read()
        return {"success": True, "content": content}
    except FileNotFoundError:
        return {"success": True, "content": "File is empty."}
    except Exception as e:
        return {"success": False, "content": f"Failed to read: {e}"}
