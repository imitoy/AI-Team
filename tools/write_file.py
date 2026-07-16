"""write_file tool — write content to a file."""

name = "write_file"
description = 'Write content to a file. Input: {"file_name": "path", "content": "..."}'
schema = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": 'Write content to a file. Input: {"file_name": "path", "content": "..."}',
        "parameters": {
            "type": "object",
            "properties": {
                "file_name": {"type": "string", "description": "The path of the file to write to"},
                "content": {"type": "string", "description": "The content to write to the file"},
            },
            "required": ["file_name", "content"],
        },
    },
}


def action(input: dict) -> dict:
    from communication import ask_proceed

    file_name = input.get("file_name", "")
    content = input.get("content", "")
    print(f"\033[0;36mWriting file:")
    print(content)
    print(f"-> will be written to: {file_name}")
    if not ask_proceed("write_file"):
        return {"success": False, "message": "Tool calling denied by user"}
    try:
        with open(file_name, "w") as f:
            f.write(content)
        return {"success": True, "content": "File written successfully"}
    except Exception as e:
        return {"success": False, "content": f"Failed to write file: {e}"}
