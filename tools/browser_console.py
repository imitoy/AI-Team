"""browser_console tool — get browser console output and JS errors."""

name = "browser_console"
description = "Get browser console messages and JavaScript errors from the current page."
schema = {
    "type": "function",
    "function": {
        "name": "browser_console",
        "description": "Get browser console output and JavaScript errors. Detect silent errors and failed API calls.",
        "parameters": {
            "type": "object",
            "properties": {
                "clear": {"type": "boolean", "description": "If true, clear message buffers after reading"}
            },
            "required": [],
        },
    },
}

_BROWSER_SCRIPT = "tools/browser.py"


def action(input: dict) -> dict:
    import subprocess
    args = ["python3", _BROWSER_SCRIPT, "console"]
    if input.get("clear"):
        args.append("--clear")
    r = subprocess.run(args, capture_output=True, text=True, timeout=30)
    return {"success": True, "content": r.stdout or r.stderr}
