"""grep_search tool — search file contents with regex."""

name = "grep_search"
description = "Search file contents using a regex pattern. Returns matching files with line numbers."
schema = {
    "type": "function",
    "function": {
        "name": "grep_search",
        "description": "Search file contents using a regex pattern. Returns matching files with line numbers.",
        "parameters": {
            "type": "object",
            "properties": {
                "pattern": {"type": "string", "description": "Regex pattern to search for"},
                "file_glob": {"type": "string", "description": "Optional file glob filter (e.g. '*.py')"},
            },
            "required": ["pattern"],
        },
    },
}


def action(input: dict) -> dict:
    import subprocess
    pattern = input.get("pattern", "")
    file_glob = input.get("file_glob", "")
    cmd = f"grep -rn --exclude-dir=.git"
    if file_glob:
        cmd += f" --include='{file_glob}'"
    cmd += f" '{pattern}' . 2>/dev/null | head -100"
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
    if not r.stdout.strip():
        return {"success": True, "content": f"No matches found for: {pattern}"}
    return {"success": True, "content": r.stdout.strip()}
