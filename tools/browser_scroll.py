"""browser_scroll tool — scroll the page up or down."""

name = "browser_scroll"
description = "Scroll the page up or down."
schema = {
    "type": "function",
    "function": {
        "name": "browser_scroll",
        "description": "Scroll the page. Use 'down' to reveal more content, 'up' to scroll back.",
        "parameters": {
            "type": "object",
            "properties": {
                "direction": {"type": "string", "enum": ["up", "down"], "description": "Direction to scroll"}
            },
            "required": ["direction"],
        },
    },
}

_BROWSER_SCRIPT = "tools/browser.py"


def action(input: dict) -> dict:
    import subprocess
    direction = input.get("direction", "down")
    r = subprocess.run(["python3", _BROWSER_SCRIPT, "scroll", direction], capture_output=True, text=True, timeout=30)
    return {"success": True, "content": r.stdout or r.stderr}
