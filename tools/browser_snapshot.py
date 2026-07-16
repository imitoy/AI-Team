"""browser_snapshot tool — get page accessibility tree."""

name = "browser_snapshot"
description = "Get a text snapshot of the current page with interactive element ref IDs."
schema = {
    "type": "function",
    "function": {
        "name": "browser_snapshot",
        "description": "Get a text snapshot of the current page. Returns interactive elements with ref IDs (@e1, @e2).",
        "parameters": {
            "type": "object",
            "properties": {
                "full": {"type": "boolean", "description": "If true, return complete content. Default: compact."},
            },
            "required": [],
        },
    },
}

_BROWSER_SCRIPT = "tools/browser.py"


def action(input: dict) -> dict:
    import subprocess
    args = ["python3", _BROWSER_SCRIPT, "snapshot"]
    if input.get("full"):
        args.append("--full")
    r = subprocess.run(args, capture_output=True, text=True, timeout=30)
    return {"success": True, "content": r.stdout or r.stderr}
