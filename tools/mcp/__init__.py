"""MCP (Model Context Protocol) client — connects to MCP servers and registers their tools"""

from __future__ import annotations

import asyncio
import json
import threading
from typing import Any


class MCPManager:
    """Manages MCP server connections and tool discovery."""

    def __init__(self):
        self._connections: dict[str, _MCPSession] = {}
        self._tools: dict[str, dict] = {}
        self._loop: asyncio.AbstractEventLoop | None = None
        self._thread: threading.Thread | None = None

    def connect_stdio(self, server_name: str, command: str,
                      args: list[str] | None = None,
                      env: dict[str, str] | None = None,
                      timeout: int = 120):
        self._ensure_loop()
        self._connections[server_name] = _MCPSession(
            server_name=server_name, transport="stdio",
            command=command, args=args or [], env=env or {}, timeout=timeout)

    def connect_http(self, server_name: str, url: str,
                     headers: dict[str, str] | None = None, timeout: int = 120):
        self._ensure_loop()
        self._connections[server_name] = _MCPSession(
            server_name=server_name, transport="http",
            url=url, headers=headers or {}, timeout=timeout)

    def discover_tools(self):
        self._ensure_loop()
        future = asyncio.run_coroutine_threadsafe(self._discover_all(), self._loop)
        future.result(timeout=60)

    def get_tools(self) -> dict[str, dict]:
        return dict(self._tools)

    def call_tool(self, tool_name: str, arguments: dict) -> str:
        tool = self._tools.get(tool_name)
        if not tool:
            return json.dumps({"error": f"Tool not found: {tool_name}"})
        session = self._connections.get(tool["server"])
        if not session or not session.is_connected:
            return json.dumps({"error": f"MCP server '{tool['server']}' not connected"})
        future = asyncio.run_coroutine_threadsafe(
            self._call_tool_async(session, tool["original_name"], arguments), self._loop)
        try:
            return future.result(timeout=session.timeout)
        except Exception as e:
            return json.dumps({"error": str(e)})

    def shutdown(self):
        if self._loop:
            async def _close():
                for s in self._connections.values():
                    await s.close()
            try:
                asyncio.run_coroutine_threadsafe(_close(), self._loop).result(timeout=10)
            except Exception:
                pass
            self._loop.call_soon_threadsafe(self._loop.stop)
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=5)

    def _ensure_loop(self):
        if self._loop is not None:
            return
        self._loop = asyncio.new_event_loop()
        self._thread = threading.Thread(target=lambda: (asyncio.set_event_loop(self._loop), self._loop.run_forever()), daemon=True)
        self._thread.start()

    async def _discover_all(self):
        results = await asyncio.gather(
            *[self._discover_one(s) for s in self._connections.values()],
            return_exceptions=True)
        for session, result in zip(self._connections.values(), results):
            if isinstance(result, Exception):
                print(f"[MCP] Discovery failed for '{session.server_name}': {result}")

    async def _discover_one(self, session: _MCPSession):
        from mcp import ClientSession
        if session.transport == "stdio":
            from mcp.client.stdio import stdio_client
            params = _make_stdio_params(session.command, session.args, session.env)
            # Keep transport and session alive for subsequent tool calls
            transport_ctx = stdio_client(params)
            session._transport = await transport_ctx.__aenter__()
            read, write = session._transport
            session_ctx = ClientSession(read, write)
            session._session = await session_ctx.__aenter__()
            await session._session.initialize()
            session.is_connected = True
            result = await session._session.list_tools()
            self._register_tools(session, result.tools)
        elif session.transport == "http":
            from mcp.client.streamable_http import streamablehttp_client
            transport_ctx = streamablehttp_client(session.url, headers=session.headers)
            session._transport = await transport_ctx.__aenter__()
            read, write, _ = session._transport
            session_ctx = ClientSession(read, write)
            session._session = await session_ctx.__aenter__()
            await session._session.initialize()
            session.is_connected = True
            result = await session._session.list_tools()
            self._register_tools(session, result.tools)

    def _register_tools(self, session: _MCPSession, mcp_tools):
        for tool in mcp_tools:
            name = f"mcp_{session.server_name}_{_sanitize(tool.name)}"
            self._tools[name] = {
                "name": name,
                "description": tool.description or f"MCP tool: {tool.name}",
                "schema": {
                    "type": "function",
                    "function": {
                        "name": name,
                        "description": tool.description or f"MCP tool: {tool.name}",
                        "parameters": tool.inputSchema or {"type": "object", "properties": {}, "required": []},
                    },
                },
                "action": _make_mcp_action(name),
                "original_name": tool.name,
                "server": session.server_name,
            }
            print(f"[MCP] Registered tool: {name} (from {session.server_name})")

    async def _call_tool_async(self, session: _MCPSession, tool_name: str, arguments: dict):
        if session._session is None:
            return json.dumps({"error": "Session not initialized"})
        result = await session._session.call_tool(tool_name, arguments)
        parts = []
        for item in result.content:
            if hasattr(item, "text"):
                parts.append(item.text)
            elif hasattr(item, "type") and item.type == "text":
                parts.append(item.text)
        return json.dumps({"result": "\n".join(parts)})


class _MCPSession:
    def __init__(self, server_name: str, transport: str, **kwargs):
        self.server_name = server_name
        self.transport = transport
        self.command = kwargs.get("command", "")
        self.args = kwargs.get("args", [])
        self.env = kwargs.get("env", {})
        self.url = kwargs.get("url", "")
        self.headers = kwargs.get("headers", {})
        self.timeout = kwargs.get("timeout", 120)
        self.is_connected = False
        self._session: Any = None
        self._transport: Any = None

    async def close(self):
        if self._session:
            try:
                await self._session.__aexit__(None, None, None)
            except Exception:
                pass
        if self._transport:
            try:
                await self._transport.__aexit__(None, None, None)
            except Exception:
                pass
        self.is_connected = False
        self._session = None
        self._transport = None


def _sanitize(name: str) -> str:
    return "".join(c if c.isalnum() else "_" for c in name)


def _make_stdio_params(command: str, args: list[str], env: dict[str, str]):
    from mcp import StdioServerParameters
    import os
    merged = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "HOME": os.environ.get("HOME", "/tmp")}
    merged.update(env)
    return StdioServerParameters(command=command, args=args, env=merged)


# ------------------------------------------------------------------
# Singleton
# ------------------------------------------------------------------

_MCP_MANAGER: MCPManager | None = None


def configure(servers: dict[str, dict] | None = None):
    """Configure and initialize MCP connections.

    servers: Optional dict of server_name -> {"command": "...", "args": [...]} or {"url": "..."}
    """
    global _MCP_MANAGER
    if servers is None:
        servers = _load_servers_config()
    if not servers:
        return
    _MCP_MANAGER = MCPManager()
    for name, config in servers.items():
        if "url" in config:
            _MCP_MANAGER.connect_http(name, config["url"],
                                       headers=config.get("headers", {}),
                                       timeout=config.get("timeout", 120))
        else:
            _MCP_MANAGER.connect_stdio(name, config["command"],
                                        args=config.get("args", []),
                                        env=config.get("env", {}),
                                        timeout=config.get("timeout", 120))
    try:
        _MCP_MANAGER.discover_tools()
        _register_to_global()
    except Exception as e:
        print(f"[MCP] Discovery failed: {e}")
        _MCP_MANAGER = None


def _register_to_global():
    """Register all discovered MCP tools into the main tools registry."""
    if _MCP_MANAGER is None:
        return
    from tools import _registry
    for name, tool in _MCP_MANAGER.get_tools().items():
        _registry[name] = tool


def _load_servers_config() -> dict[str, dict]:
    import os as _os
    raw = _os.environ.get("MCP_SERVERS_JSON", "")
    if raw:
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            pass
    for path in [_os.path.expanduser("~/.ai-team/mcp_servers.json"),
                 _os.path.join(_os.getcwd(), "mcp_servers.json")]:
        if _os.path.isfile(path):
            try:
                with open(path) as f:
                    return json.load(f)
            except Exception:
                pass
    return {}


def _make_mcp_action(tool_name: str):
    def action(input: dict) -> dict:
        if _MCP_MANAGER is None:
            return {"success": False, "content": "MCP not configured"}
        result = _MCP_MANAGER.call_tool(tool_name, input)
        try:
            parsed = json.loads(result)
            if "result" in parsed:
                return {"success": True, "content": parsed["result"]}
            if "error" in parsed:
                return {"success": False, "content": parsed["error"]}
            return {"success": True, "content": result}
        except json.JSONDecodeError:
            return {"success": True, "content": result}
    return action
