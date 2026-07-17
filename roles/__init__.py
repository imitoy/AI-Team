"""Roles package — each file defines a single ROLE dict.

Usage:
    from roles import ROLES, get_role, build_role_list
"""

from __future__ import annotations

import importlib

_ROLE_MODULES = [
    "architect",
    "coder",
    "organizer",
    "reviewer",
    "security",
    "tester",
]

ROLES: list[dict] = []


def _load_all():
    for mod_name in _ROLE_MODULES:
        try:
            mod = importlib.import_module(f"roles.{mod_name}")
            ROLES.append(mod.ROLE)
        except Exception as e:
            print(f"[WARN] Failed to load role '{mod_name}': {e}")


def get_role(name: str) -> dict | None:
    """Look up a role by name."""
    for role in ROLES:
        if role["name"] == name:
            return role
    return None


def build_role_list(exclude: str | None = None) -> str:
    """Build a human-readable list of available roles for tool descriptions."""
    lines = []
    for i, role in enumerate(ROLES, 1):
        if role["name"] != exclude:
            lines.append(f"{i}. {role['name']} - {role['description']}")
    return "\n".join(lines)


_load_all()
