"""browser_click tool — click an element by ref ID."""

name = "browser_click"
description = "Click on an element by its ref ID (e.g. @e5)."
schema = {
    "type": "function",
    "function": {
        "name": "browser_click",
        "description": "Click an element identified by its ref ID from the snapshot (e.g. @e5).",
        "parameters": {
            "type": "object",
            "properties": {
                "ref": {"type": "string", "description": "Element reference (e.g. @e5)"}
            },
            "required": ["ref"],
        },
    },
}

_BROWSER_SCRIPT = "tools/browser.py"


def action(input: dict) -> dict:
    import subprocess
    ref = input.get("ref", "")
    r = subprocess.run(["python3", _BROWSER_SCRIPT, "click", ref], capture_output=True, text=True, timeout=30)
    return {"success": True, "content": r.stdout or r.stderr}
