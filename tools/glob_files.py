"""glob_files tool — find files matching a glob pattern."""

name = "glob_files"
description = "Find files matching a glob pattern (e.g. '**/*.py', '*.lua')."
schema = {
    "type": "function",
    "function": {
        "name": "glob_files",
        "description": "Find files matching a glob pattern. Returns all matching file paths.",
        "parameters": {
            "type": "object",
            "properties": {
                "pattern": {"type": "string", "description": "Glob pattern (e.g. '**/*.py', '*.lua')"}
            },
            "required": ["pattern"],
        },
    },
}


def action(input: dict) -> dict:
    import subprocess
    pattern = input.get("pattern", "")
    # Use find with the pattern
    cmd = f"find . -path ./.git -prune -o -name '{pattern}' -print 2>/dev/null | head -200"
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
    lines = [l for l in r.stdout.strip().split("\n") if l]
    if not lines:
        return {"success": True, "content": f"No files found matching: {pattern}"}
    return {"success": True, "content": "\n".join(lines)}
