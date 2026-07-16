"""browser_type tool — type text into an input field."""

name = "browser_type"
description = "Type text into an input field by ref ID. Clears field first."
schema = {
    "type": "function",
    "function": {
        "name": "browser_type",
        "description": "Type text into an input field identified by its ref ID (e.g. @e3). Clears the field first.",
        "parameters": {
            "type": "object",
            "properties": {
                "ref": {"type": "string", "description": "Element reference (e.g. @e3)"},
                "text": {"type": "string", "description": "The text to type"},
            },
            "required": ["ref", "text"],
        },
    },
}

_BROWSER_SCRIPT = "tools/browser.py"


def action(input: dict) -> dict:
    import subprocess
    ref = input.get("ref", "")
    text = input.get("text", "")
    r = subprocess.run(["python3", _BROWSER_SCRIPT, "type", ref, text], capture_output=True, text=True, timeout=30)
    return {"success": True, "content": r.stdout or r.stderr}
