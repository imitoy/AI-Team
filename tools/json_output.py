"""json_output tool — set response format to JSON."""

name = "json_output"
description = "Output the result in JSON format"
schema = None  # This is a handle tool, not a function tool


def action(input: dict) -> dict:
    # In the Lua version this modified the communication object.
    # In Python, this would need access to the API object.
    # For now, return a placeholder.
    return {"success": True, "content": "JSON output mode requested"}
