"""Communication manager — orchestrates conversations, tool dispatch, and role delegation."""

from __future__ import annotations

import os
import time

from api import OpenAIAPI
from models import MODELS


# --- AskProceed ---
_approved: set[str] = set()
_auto_approve = os.getenv("AI_TEAM_AUTO_APPROVE", "").lower() in ("1", "true", "yes")


def ask_proceed(tag: str) -> bool:
    """Ask the user whether to proceed with a tool action."""
    if tag in _approved or _auto_approve:
        return True
    while True:
        resp = input(f"Proceed with {tag}? [(Y)es/(n)o/(a)bort/yesforall]: ").strip()
        if resp in ("Y", "y", ""):
            return True
        elif resp in ("n", "N"):
            return False
        elif resp in ("a", "A"):
            print("Abort.")
            raise SystemExit(0)
        elif resp == "yesforall":
            _approved.add(tag)
            return True
        else:
            print("Invalid input. Enter Y, n, a, or yesforall.")


# --- Communication ---
_registered: list["Communication"] = []


class Communication:
    """Manages a conversation with a specific role, backed by an API client."""

    def __init__(self, model_key: str, role_name: str):
        self.role_name = role_name
        self.model_key = model_key
        self.model = MODELS[model_key]
        self.api = OpenAIAPI(model_key, role_name)
        self.id = int(time.time())

    def append_user_message(self, message: str):
        self.api.append_user_message(message)

    def send(self):
        self.api.send()

    @property
    def last_response(self) -> str | None:
        """Get the last assistant message content."""
        for msg in reversed(self.api.messages):
            if msg.get("role") == "assistant" and msg.get("content"):
                return msg["content"]
        return None

    @staticmethod
    def get_or_create(model_key: str, role_name: str) -> "Communication":
        """Reuse an existing Communication for the same role, or create a new one."""
        for comm in _registered:
            if comm.role_name == role_name:
                comm.model_key = model_key
                comm.model = MODELS[model_key]
                return comm
        comm = Communication(model_key, role_name)
        _registered.append(comm)
        return comm
