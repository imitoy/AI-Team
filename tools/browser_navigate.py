"""browser_navigate tool — navigate to a URL via agent-browser."""

name = "browser_navigate"
description = "Navigate to a URL in the browser. Returns page snapshot automatically."
schema = {
    "type": "function",
    "function": {
        "name": "browser_navigate",
        "description": "Navigate to a URL in the browser. Returns the page title, URL, and a text snapshot.",
        "parameters": {
            "type": "object",
            "properties": {
                "url": {"type": "string", "description": "The URL to navigate to"}
            },
            "required": ["url"],
        },
    },
}

_BROWSER_SCRIPT = "tools/browser.py"


def action(input: dict) -> dict:
    import json, subprocess
    url = input.get("url", "")
    r = subprocess.run(
        ["python3", _BROWSER_SCRIPT, "navigate", url],
        capture_output=True, text=True, timeout=60,
    )
    try:
        return {"success": True, "content": r.stdout}
    except Exception:
        return {"success": False, "content": r.stderr or "Navigate failed"}
