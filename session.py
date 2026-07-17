"""Session manager — persists and restores multi-role conversation sessions.

A session captures all role conversations (organizer, architect, coder, ...)
within one conversation thread. Sessions are saved as JSON files in the
state directory.

File layout:
    {state_dir}/sessions/{session_id}.json  — individual session
    {state_dir}/sessions/index.json         — session registry

Usage:
    from session import Session

    # Create
    sess = Session(topic="Build a todo app", model_key="deepseek_v4_flash")
    sess.add_user_message("Hello")
    sess.send("organizer")
    sess.save()

    # Restore
    sess = Session.load(session_id)
    sess.send("architect")  # continue where you left off

    # Manager
    from session import SessionManager
    mgr = SessionManager()
    for s in mgr.list_sessions():
        print(s.id, s.topic)
"""

from __future__ import annotations

import json
import os
import time
import uuid
from typing import Any

from paths import paths


SESSIONS_DIR = os.path.join(paths.state_dir, "sessions")
INDEX_PATH = os.path.join(SESSIONS_DIR, "index.json")


class Session:
    """A multi-role conversation session."""

    def __init__(
        self,
        topic: str = "",
        model_key: str = "deepseek_v4_flash",
        session_id: str | None = None,
    ):
        self.id = session_id or str(uuid.uuid4())[:8]
        self.topic = topic
        self.model_key = model_key
        self.created_at = time.time()
        self.updated_at = self.created_at
        # role_name -> list of messages (API-native format)
        self._role_messages: dict[str, list[dict]] = {}

    # ------------------------------------------------------------------
    # Message access
    # ------------------------------------------------------------------

    def get_messages(self, role_name: str) -> list[dict]:
        """Get the message history for a role."""
        return self._role_messages.setdefault(role_name, [])

    def set_messages(self, role_name: str, messages: list[dict]):
        """Set the message history for a role (e.g., after restore)."""
        self._role_messages[role_name] = messages

    def add_message(self, role_name: str, message: dict):
        """Append a single message to a role's history."""
        self._role_messages.setdefault(role_name, []).append(message)

    def add_user_message(self, role_name: str, content: str):
        """Append a user message to a role."""
        self.add_message(role_name, {"role": "user", "content": content})

    def has_role(self, role_name: str) -> bool:
        """Check if a role has any messages."""
        msgs = self._role_messages.get(role_name, [])
        return len(msgs) > 0

    @property
    def active_roles(self) -> list[str]:
        """Return list of role names that have messages."""
        return sorted(self._role_messages.keys())

    def message_count(self) -> int:
        """Total message count across all roles."""
        return sum(len(msgs) for msgs in self._role_messages.values())

    def last_role_message(self, role_name: str) -> str | None:
        """Get the last assistant message content for a role."""
        for msg in reversed(self.get_messages(role_name)):
            if msg.get("role") == "assistant" and msg.get("content"):
                return msg["content"]
        return None

    # ------------------------------------------------------------------
    # Interaction helpers
    # ------------------------------------------------------------------

    def send(self, role_name: str) -> str | None:
        """Send the current conversation for a role and capture the response.
        Uses Communication to talk to the model."""
        from communication import Communication

        comm = Communication.get_or_create(self.model_key, role_name)

        # Restore any saved messages into the API
        existing = self.get_messages(role_name)
        if existing and hasattr(comm.api, 'load_messages'):
            comm.api.load_messages(existing)

        comm.api.send()

        # Capture all resulting messages
        self._role_messages[role_name] = list(comm.api.messages)
        self.updated_at = time.time()
        return self.last_role_message(role_name)

    # ------------------------------------------------------------------
    # Persistence
    # ------------------------------------------------------------------

    def to_dict(self) -> dict:
        """Serialize session to a dict for JSON storage."""
        return {
            "id": self.id,
            "topic": self.topic,
            "model_key": self.model_key,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "roles": {k: list(v) for k, v in self._role_messages.items()},
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Session":
        """Restore a session from a serialized dict."""
        sess = cls(
            topic=data.get("topic", ""),
            model_key=data.get("model_key", "deepseek_v4_flash"),
            session_id=data.get("id"),
        )
        sess.created_at = data.get("created_at", sess.created_at)
        sess.updated_at = data.get("updated_at", sess.updated_at)
        for role_name, messages in data.get("roles", {}).items():
            sess._role_messages[role_name] = list(messages)
        return sess

    def save(self) -> str:
        """Save this session to its data file. Returns the file path."""
        os.makedirs(SESSIONS_DIR, exist_ok=True)
        filepath = os.path.join(SESSIONS_DIR, f"{self.id}.json")
        with open(filepath, "w") as f:
            json.dump(self.to_dict(), f, indent=2, ensure_ascii=False)
        return filepath

    @classmethod
    def load(cls, session_id: str) -> "Session | None":
        """Load a session from its data file."""
        filepath = os.path.join(SESSIONS_DIR, f"{session_id}.json")
        if not os.path.isfile(filepath):
            return None
        with open(filepath) as f:
            data = json.load(f)
        return cls.from_dict(data)

    @classmethod
    def delete(cls, session_id: str) -> bool:
        """Delete a session file. Returns True if successful."""
        filepath = os.path.join(SESSIONS_DIR, f"{session_id}.json")
        if os.path.isfile(filepath):
            os.remove(filepath)
            return True
        return False


# ------------------------------------------------------------------
# Session manager — lists, searches, manages sessions
# ------------------------------------------------------------------


class SessionManager:
    """Manages the collection of saved sessions."""

    def list_sessions(self) -> list[dict]:
        """Return a list of session summaries (id, topic, created, updated, messages)."""
        os.makedirs(SESSIONS_DIR, exist_ok=True)
        sessions = []
        for filename in sorted(os.listdir(SESSIONS_DIR)):
            if not filename.endswith(".json") or filename == "index.json":
                continue
            filepath = os.path.join(SESSIONS_DIR, filename)
            try:
                with open(filepath) as f:
                    data = json.load(f)
                sessions.append({
                    "id": data.get("id", filename[:-5]),
                    "topic": data.get("topic", ""),
                    "model_key": data.get("model_key", ""),
                    "created_at": data.get("created_at", 0),
                    "updated_at": data.get("updated_at", 0),
                    "roles": sorted(data.get("roles", {}).keys()),
                    "message_count": sum(len(v) for v in data.get("roles", {}).values()),
                    "path": filepath,
                })
            except Exception:
                continue
        # Sort by updated_at desc
        sessions.sort(key=lambda s: s.get("updated_at", 0), reverse=True)
        return sessions

    def find(self, session_id: str) -> Session | None:
        """Find and load a session by ID."""
        return Session.load(session_id)

    def delete(self, session_id: str) -> bool:
        """Delete a session by ID."""
        return Session.delete(session_id)

    def latest(self) -> Session | None:
        """Return the most recently updated session."""
        sessions = self.list_sessions()
        if sessions:
            return self.find(sessions[0]["id"])
        return None

    def prune(self, max_sessions: int = 100):
        """Remove oldest sessions when count exceeds max_sessions."""
        sessions = self.list_sessions()
        if len(sessions) <= max_sessions:
            return
        for s in sessions[max_sessions:]:
            self.delete(s["id"])
