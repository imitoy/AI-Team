"""Tool registry — auto-discovers and loads all tool modules.

Each tool module can either:
- Define `name`, `schema`, `action` at module level (single tool), OR
- Define `TOOLS` as a list of dicts with keys: name, description, schema, action (multi-tool)
"""

from __future__ import annotations

import importlib
from typing import Any


# Ordered list of tool module names to load
_TOOL_MODULES = [
    "json_output",
    "get_weather",
    "call_role",
    "write_file",
    "read_file",
    "edit_file",
    "list_files",
    "run_command",
    "kill_process",
    "read_architect",
    "write_architect",
    # Browser tools
    "browser_navigate",
    "browser_snapshot",
    "browser_click",
    "browser_type",
    "browser_scroll",
    "browser_back",
    "browser_press",
    "browser_console",
    # Claude Code coding tools
    "glob_files",
    "grep_search",
    "check_tool_status",
]

_registry: dict[str, Any] = {}


def _load_all():
    """Import each tool module and register its tool(s)."""
    for mod_name in _TOOL_MODULES:
        try:
            mod = importlib.import_module(f"tools.{mod_name}")

            # Multi-tool module: defines TOOLS list
            if hasattr(mod, "TOOLS"):
                for tool in mod.TOOLS:
                    _registry[tool["name"]] = tool
            # Single-tool module: defines name + action at module level
            elif hasattr(mod, "name"):
                _registry[mod.name] = mod
        except Exception as e:
            print(f"[WARN] Failed to load tool '{mod_name}': {e}")

    # ---- Load MCP tools (if MCP package is available) ----
    _load_mcp_tools()


def _load_mcp_tools():
    """Discover and register MCP tools if MCP servers are configured."""
    try:
        from tools.mcp import _MCP_MANAGER, _register_to_global
        if _MCP_MANAGER is not None:
            _register_to_global()
    except Exception as e:
        print(f"[INFO] MCP tools not loaded: {e}")


def get_tool(name: str):
    """Look up a tool by name. Returns the tool object or None."""
    return _registry.get(name)


def all_tools() -> list[Any]:
    """Return all loaded tool objects."""
    return list(_registry.values())


def all_names() -> list[str]:
    """Return all loaded tool names."""
    return list(_registry.keys())


# Auto-load on import
_load_all()
