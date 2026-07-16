"""browser_press tool — press a keyboard key."""

name = "browser_press"
description = "Press a keyboard key (Enter, Tab, Escape, etc.)."
schema = {
    "type": "function",
    "function": {
        "name": "browser_press",
        "description": "Press a keyboard key. Useful for submitting forms (Enter), navigating (Tab), etc.",
        "parameters": {
            "type": "object",
            "properties": {
                "key": {"type": "string", "description": "Key to press (Enter, Tab, Escape, ArrowDown, etc.)"}
            },
            "required": ["key"],
        },
    },
}

_BROWSER_SCRIPT = "tools/browser.py"


def action(input: dict) -> dict:
    import subprocess
    key = input.get("key", "")
    r = subprocess.run(["python3", _BROWSER_SCRIPT, "press", key], capture_output=True, text=True, timeout=30)
    return {"success": True, "content": r.stdout or r.stderr}
