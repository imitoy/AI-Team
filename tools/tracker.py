"""Async tool call tracker — manages background tool execution with status polling.

Usage:
    from tools.tracker import tracker
    call_id = tracker.start("run_command", {"command": "sleep 10; echo done"})
    status = tracker.poll(call_id)  # {'status': 'running', 'elapsed': 5.2}
    result = tracker.wait(call_id)  # blocks until done

Each call has: id, tool_name, arguments, status (pending|running|done|error),
start_time, end_time, result, error.

Default timeout: 300 seconds — after this, poll() returns status='running' with
elapsed time so the LLM can decide to wait or continue.
"""

from __future__ import annotations

import json
import threading
import time
import uuid
from typing import Any


DEFAULT_TIMEOUT = 300  # seconds before poll returns "still running"


class ToolCallTracker:
    """Singleton tracker for async tool calls."""

    def __init__(self):
        self._calls: dict[str, dict] = {}
        self._lock = threading.Lock()

    def start(self, tool_name: str, arguments: dict, action_fn, timeout: int = DEFAULT_TIMEOUT) -> str:
        """Start a tool call in a background thread. Returns call_id."""
        call_id = str(uuid.uuid4())[:12]
        now = time.time()

        entry = {
            "id": call_id,
            "tool_name": tool_name,
            "arguments": arguments,
            "status": "pending",
            "start_time": now,
            "end_time": None,
            "elapsed": 0.0,
            "result": None,
            "error": None,
            "timeout": timeout,
        }

        with self._lock:
            self._calls[call_id] = entry

        thread = threading.Thread(
            target=self._run, args=(call_id, tool_name, arguments, action_fn),
            daemon=True)
        thread.start()
        return call_id

    def poll(self, call_id: str) -> dict:
        """Get the current status of a tool call.

        Returns dict with: id, tool_name, status, elapsed, result, error.
        Status is one of: pending, running, done, error, not_found.
        """
        with self._lock:
            entry = self._calls.get(call_id)
        if not entry:
            return {"id": call_id, "status": "not_found", "error": f"Call {call_id} not found"}

        now = time.time()
        elapsed = now - entry["start_time"]

        if entry["status"] == "done":
            return {
                "id": call_id,
                "tool_name": entry["tool_name"],
                "status": "done",
                "elapsed": round(elapsed, 2),
                "result": entry["result"],
            }
        elif entry["status"] == "error":
            return {
                "id": call_id,
                "tool_name": entry["tool_name"],
                "status": "error",
                "elapsed": round(elapsed, 2),
                "error": entry["error"],
            }
        else:
            # pending or running
            if elapsed < entry["timeout"]:
                return {
                    "id": call_id,
                    "tool_name": entry["tool_name"],
                    "status": "running",
                    "elapsed": round(elapsed, 2),
                    "message": f"Tool '{entry['tool_name']}' is still running ({elapsed:.1f}s elapsed). Call check_tool_status again with call_id='{call_id}' to poll for completion.",
                }
            else:
                # Timeout — still running but past threshold
                return {
                    "id": call_id,
                    "tool_name": entry["tool_name"],
                    "status": "running",
                    "elapsed": round(elapsed, 2),
                    "message": f"Tool '{entry['tool_name']}' exceeded {entry['timeout']}s timeout but is still running ({elapsed:.1f}s elapsed). You may call check_tool_status(call_id='{call_id}') to check again, or proceed with other tasks.",
                }

    def wait(self, call_id: str, poll_interval: float = 1.0) -> dict:
        """Block until the tool call completes. Returns final status dict."""
        while True:
            status = self.poll(call_id)
            if status["status"] in ("done", "error", "not_found"):
                return status
            time.sleep(poll_interval)

    def get_status(self, call_id: str) -> str:
        """Get status as a JSON string for tool response."""
        status = self.poll(call_id)
        return json.dumps(status, ensure_ascii=False)

    def list_calls(self) -> list[dict]:
        """Return all tracked calls."""
        with self._lock:
            return [self.poll(cid) for cid in self._calls]

    def _run(self, call_id: str, tool_name: str, arguments: dict, action_fn):
        with self._lock:
            self._calls[call_id]["status"] = "running"

        try:
            result = action_fn(arguments)
            with self._lock:
                self._calls[call_id]["status"] = "done"
                self._calls[call_id]["result"] = result.get("content", str(result))
                self._calls[call_id]["end_time"] = time.time()
        except Exception as e:
            with self._lock:
                self._calls[call_id]["status"] = "error"
                self._calls[call_id]["error"] = str(e)
                self._calls[call_id]["end_time"] = time.time()

    def _cleanup_old(self, max_age: float = 3600):
        """Remove completed calls older than max_age seconds."""
        now = time.time()
        with self._lock:
            stale = []
            for cid, entry in self._calls.items():
                if entry["status"] in ("done", "error") and entry.get("end_time"):
                    if now - entry["end_time"] > max_age:
                        stale.append(cid)
            for cid in stale:
                del self._calls[cid]


# Singleton
tracker = ToolCallTracker()
