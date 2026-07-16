"""browser_back tool — go back in browser history."""

name = "browser_back"
description = "Navigate back to the previous page in browser history."
schema = {
    "type": "function",
    "function": {
        "name": "browser_back",
        "description": "Navigate back to the previous page in browser history.",
        "parameters": {"type": "object", "properties": {}, "required": []},
    },
}

_BROWSER_SCRIPT = "tools/browser.py"


def action(input: dict) -> dict:
    import subprocess
    r = subprocess.run(["python3", _BROWSER_SCRIPT, "back"], capture_output=True, text=True, timeout=30)
    return {"success": True, "content": r.stdout or r.stderr}
