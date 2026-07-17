"""Check the status of a running tool call by its call ID."""

from __future__ import annotations

from tools.tracker import tracker

name = "check_tool_status"

schema = {
    "type": "function",
    "function": {
        "name": "check_tool_status",
        "description": (
            "Check the status of a previously started tool call by its call ID. "
            "Use this to poll for completion of long-running tools. "
            "The response will include the current status (running/done/error), "
            "elapsed time, and the result if completed."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "call_id": {
                    "type": "string",
                    "description": "The call ID returned by a previous tool invocation",
                },
            },
            "required": ["call_id"],
        },
    },
}


def action(input: dict) -> dict:
    """Check tool call status."""
    call_id = input.get("call_id", "")
    if not call_id:
        return {"success": False, "content": "call_id is required"}

    status = tracker.poll(call_id)
    return {"success": True, "content": tracker.get_status(call_id)}
