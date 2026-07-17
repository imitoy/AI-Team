"""Anthropic API client with tool calling support.

Uses the official anthropic SDK. Anthropic uses a different wire format
than OpenAI — this adapter normalizes the interface to match OpenAIAPI.
"""

from __future__ import annotations

import json
from typing import Any

from anthropic import Anthropic

from provider import MODELS
from roles import get_role
from tools import get_tool


class AnthropicAPI:
    """Wraps the Anthropic Messages API with tool dispatch."""

    # Max tokens required by Anthropic, reasonable default
    DEFAULT_MAX_TOKENS = 8192

    def __init__(self, model_key: str, role_name: str):
        model = MODELS[model_key]
        self.client = Anthropic(api_key=model["api_key"])
        self.model_name = model["name"]
        self.role_name = role_name
        role = get_role(role_name)
        self._system_prompt = role["system_prompt"] if role else ""
        self._messages: list[dict] = []  # Anthropic-format messages

        # Build tool schemas, converting OpenAI format to Anthropic format
        self.tools_index: dict[str, str] = {}
        ctools = []
        role_tools = role["tools"] if role else []
        for tool_name in role_tools:
            tool = get_tool(tool_name)
            if tool:
                schema = tool.schema if hasattr(tool, "schema") else tool.get("schema")
                if schema:
                    oai_fn = schema["function"]
                    # Anthropic format: name, description, input_schema
                    ctools.append({
                        "name": oai_fn["name"],
                        "description": oai_fn.get("description", ""),
                        "input_schema": oai_fn.get("parameters", {"type": "object", "properties": {}, "required": []}),
                    })
                    self.tools_index[oai_fn["name"]] = tool_name
        self.tools = ctools if ctools else None

    @property
    def messages(self) -> list[dict]:
        """Return messages in OpenAI-compatible format for compatibility."""
        result = []
        if self._system_prompt:
            result.append({"role": "system", "content": self._system_prompt})
        for msg in self._messages:
            result.append(self._anthropic_to_openai_msg(msg))
        return result

    def append_user_message(self, message: str):
        self._messages.append({"role": "user", "content": message})
        print(f"[INFO] Role: {self.role_name}")
        print(f"[INFO] User message appended: {message}")

    def send(self):
        """Send conversation and handle tool calls recursively."""
        while True:
            response = self._create_completion()
            stop_reason = response.stop_reason

            # Build the assistant message
            assistant_msg = {"role": "assistant", "content": []}
            for block in response.content:
                if block.type == "text":
                    assistant_msg["content"].append({"type": "text", "text": block.text})
                elif block.type == "tool_use":
                    assistant_msg["content"].append({
                        "type": "tool_use",
                        "id": block.id,
                        "name": block.name,
                        "input": block.input,
                    })
                elif block.type == "thinking":
                    # Store thinking for display
                    print(f"[INFO] Role: {self.role_name}")
                    print(f"[INFO] Model reasoning: {block.thinking[:200]}...")

            self._messages.append(assistant_msg)

            if stop_reason == "tool_use":
                # Collect tool_use blocks and dispatch
                tool_blocks = [b for b in response.content if b.type == "tool_use"]
                tool_results = []
                for tb in tool_blocks:
                    fn_name = tb.name
                    fn_args = tb.input
                    print(f"[INFO] Role: {self.role_name}")
                    print(f"[INFO] Tool call received: {fn_name} {fn_args}")

                    tool_key = self.tools_index.get(fn_name, fn_name)
                    result = self.on_tool(tb.id, tool_key, fn_args)
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": tb.id,
                        "content": result,
                    })
                    print(f"[INFO] Role: {self.role_name}")
                    print(f"[INFO] Tool call response appended: {fn_name} {result[:200]}")

                # Append tool results as a user message
                self._messages.append({"role": "user", "content": tool_results})
                # Continue loop for next model response
            else:
                # Normal end — extract text response
                text = response.content[0].text if response.content else ""
                if text:
                    print(f"[INFO] Role: {self.role_name}")
                    print(f"[INFO] Model response: {text}")
                break

    def on_tool(self, call_id: str, tool_name: str, arguments: dict) -> str:
        """Dispatch a tool call. Returns result string."""
        tool = get_tool(tool_name)
        if not tool:
            return "Tool not found"
        action_fn = tool.action if hasattr(tool, "action") else tool.get("action")
        if action_fn:
            result = action_fn(arguments)
            return result.get("content", str(result))
        return "Tool has no action"

    def _create_completion(self):
        """Create a completion with retry."""
        kwargs = {
            "model": self.model_name,
            "max_tokens": self.DEFAULT_MAX_TOKENS,
            "messages": self._messages,
            "temperature": 0,
        }
        if self._system_prompt:
            kwargs["system"] = self._system_prompt
        if self.tools:
            kwargs["tools"] = self.tools

        while True:
            try:
                return self.client.messages.create(**kwargs)
            except Exception as e:
                print(f"[ERROR] Failed to create completion: {e}")
                retry = input("Retry? (Y/n): ").strip()
                if retry.lower() == "n":
                    raise

    @staticmethod
    def _anthropic_to_openai_msg(msg: dict) -> dict:
        """Convert an Anthropic-format message to OpenAI format for compatibility."""
        role = msg.get("role", "")
        if role == "assistant":
            content = msg.get("content", [])
            text = ""
            tool_calls = []
            if isinstance(content, str):
                text = content
            elif isinstance(content, list):
                for block in content:
                    if block.get("type") == "text":
                        text += block.get("text", "")
                    elif block.get("type") == "tool_use":
                        tool_calls.append({
                            "id": block.get("id"),
                            "type": "function",
                            "function": {
                                "name": block.get("name"),
                                "arguments": json.dumps(block.get("input", {})),
                            },
                        })
            result = {"role": "assistant", "content": text}
            if tool_calls:
                result["tool_calls"] = tool_calls
            return result
        elif role == "user":
            content = msg.get("content", "")
            if isinstance(content, list):
                return {"role": "user", "content": json.dumps(content)}
            return {"role": "user", "content": str(content)}
        return msg

    @staticmethod
    def list_models(api_key: str, base_url: str) -> list[dict]:
        """List available models from the Anthropic API."""
        from anthropic import Anthropic
        client = Anthropic(api_key=api_key)
        models = []
        try:
            for m in client.models.list():
                models.append({
                    "id": m.id,
                    "display_name": m.display_name,
                    "created_at": str(m.created_at) if m.created_at else "",
                })
        except Exception as e:
            print(f"[WARN] Failed to list Anthropic models: {e}")
        return models
