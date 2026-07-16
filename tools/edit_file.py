"""edit_file tool — find-and-replace within a file."""

name = "edit_file"
description = 'Edit a file by replacing text. Input: {"file_name": "path", "replace": "old", "content": "new"}'
schema = {
    "type": "function",
    "function": {
        "name": "edit_file",
        "description": 'Edit a file by replacing text. Input: {"file_name": "path", "replace": "old text", "content": "new text"}',
        "parameters": {
            "type": "object",
            "properties": {
                "file_name": {"type": "string", "description": "The path of the file to edit"},
                "replace": {"type": "string", "description": "The content to find and replace"},
                "content": {"type": "string", "description": "The new content to replace with"},
            },
            "required": ["file_name", "replace", "content"],
        },
    },
}


def action(input: dict) -> dict:
    from communication import ask_proceed

    file_name = input.get("file_name", "")
    replace = input.get("replace", "")
    content = input.get("content", "")
    print(f"\033[0;36mEditing file:")
    print(replace)
    print("-> will be replaced as ->")
    print(content)
    print(f"-> in: {file_name}")
    if not ask_proceed("edit_file"):
        return {"success": False, "content": "Tool calling denied by user"}
    try:
        with open(file_name, "r") as f:
            existing = f.read()
        if replace in existing:
            existing = existing.replace(replace, content, 1)
            with open(file_name, "w") as f:
                f.write(existing)
            return {"success": True, "content": "File edited successfully"}
        return {"success": False, "content": "Replace content not found"}
    except Exception as e:
        return {"success": False, "content": f"Failed to edit file: {e}"}
