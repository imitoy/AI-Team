"""read_file tool — read content from a file."""

name = "read_file"
description = 'Read content from a file. Input: {"file_name": "path"}'
schema = {
    "type": "function",
    "function": {
        "name": "read_file",
        "description": 'Read content from a file. Input: {"file_name": "path"}',
        "parameters": {
            "type": "object",
            "properties": {
                "file_name": {"type": "string", "description": "The path of the file to read from"},
            },
            "required": ["file_name"],
        },
    },
}


def action(input: dict) -> dict:
    file_name = input.get("file_name", "")
    try:
        with open(file_name, "r") as f:
            content = f.read()
        if not content:
            return {"success": False, "content": "File is empty"}
        return {"success": True, "content": content}
    except FileNotFoundError:
        return {"success": False, "content": "File not found"}
    except Exception as e:
        return {"success": False, "content": f"Failed to read file: {e}"}
