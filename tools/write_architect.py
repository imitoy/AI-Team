"""write_architect tool — write ARCHITECT.md design document."""

name = "write_architect"
description = 'Write architecture to ARCHITECT.md. Input: {"content": "..."}'
schema = {
    "type": "function",
    "function": {
        "name": "write_architect",
        "description": 'Write architecture to ARCHITECT.md. Input: {"content": "..."}',
        "parameters": {
            "type": "object",
            "properties": {
                "content": {"type": "string", "description": "The content to write to ARCHITECT.md"},
            },
            "required": ["content"],
        },
    },
}


def action(input: dict) -> dict:
    from communication import ask_proceed

    content = input.get("content", "")
    print(f"\033[0;36mWriting ARCHITECT.md:")
    print(content)
    if not ask_proceed("write_file"):
        return {"success": False, "message": "Tool calling denied by user"}
    try:
        with open("ARCHITECT.md", "w") as f:
            f.write(content)
        return {"success": True, "content": "File written successfully"}
    except Exception as e:
        return {"success": False, "content": f"Failed to write file: {e}"}
