"""GLM (Zhipu AI) API client with tool calling and thinking mode support.

Uses the official zhipuai SDK. GLM API docs: https://docs.bigmodel.cn
"""

from __future__ import annotations

import json
from typing import Any

from zhipuai import ZhipuAI

from provider import MODELS
from roles import get_role
from tools import get_tool


class GLMAPI:
    """Wraps the Zhipu AI (GLM) chat completions endpoint with tool dispatch."""

    def __init__(self, model_key: str, role_name: str):
        model = MODELS[model_key]
        self.client = ZhipuAI(api_key=model["api_key"])
        self.model_name = model["name"]
        self.role_name = role_name
        role = get_role(role_name)
        system_prompt = role["system_prompt"] if role else ""
        self.messages: list[dict] = [{"role": "system", "content": system_prompt}]

        # Build tool schemas from the role's tool list
        self.tools_index: dict[str, str] = {}
        ctools = []
        role_tools = role["tools"] if role else []
        for tool_name in role_tools:
            tool = get_tool(tool_name)
            if tool:
                schema = tool.schema if hasattr(tool, "schema") else tool.get("schema")
                if schema:
                    ctools.append(schema)
                    fn_name = schema["function"]["name"]
                    self.tools_index[fn_name] = tool_name
        self.tools = ctools if ctools else None

        self.completion_kwargs: dict[str, Any] = {
            "model": self.model_name,
            "messages": self.messages,
            "temperature": 0,
        }
        if self.tools:
            self.completion_kwargs["tools"] = self.tools

    def append_user_message(self, message: str):
        self.messages.append({"role": "user", "content": message})
        print(f"[INFO] Role: {self.role_name}")
        print(f"[INFO] User message appended: {message}")

    def send(self):
        """Send the conversation to the model and handle tool calls recursively."""
        while True:
            response = self._create_completion()
            message = response.choices[0].message

            # Convert to dict and append
            msg_dict = message.model_dump()
            self.messages.append(msg_dict)

            # GLM supports reasoning_content (thinking mode)
            reasoning = getattr(message, "reasoning_content", None)
            if reasoning:
                print(f"[INFO] Role: {self.role_name}")
                print(f"[INFO] Model reasoning: {reasoning[:200]}...")

            if message.tool_calls:
                for tool_call in message.tool_calls:
                    fn_name = tool_call.function.name
                    fn_args = tool_call.function.arguments
                    print(f"[INFO] Role: {self.role_name}")
                    print(f"[INFO] Tool call received: {fn_name} {fn_args}")

                    tool_key = self.tools_index.get(fn_name, fn_name)
                    arguments = json.loads(fn_args) if fn_args else {}

                    result = self.on_tool(tool_call.id, tool_key, arguments)
                    self.tool_call_result(tool_call.id, fn_name, result)
                # Continue the loop for the next model response
            elif message.content:
                print(f"[INFO] Role: {self.role_name}")
                print(f"[INFO] Model response: {message.content}")
                break
            else:
                break

    def on_tool(self, call_id: str, tool_name: str, arguments: dict) -> str:
        """Dispatch a tool call. Returns the result string."""
        tool = get_tool(tool_name)
        if not tool:
            return "Tool not found"
        action_fn = tool.action if hasattr(tool, "action") else tool.get("action")
        if action_fn:
            result = action_fn(arguments)
            return result.get("content", str(result))
        return "Tool has no action"

    def tool_call_result(self, call_id: str, name: str, content: str):
        """Append a tool result message."""
        self.messages.append({
            "role": "tool",
            "content": content,
            "name": name,
            "tool_call_id": call_id,
        })
        print(f"[INFO] Role: {self.role_name}")
        print(f"[INFO] Tool call response appended: {name} {content[:200]}")

    def _create_completion(self) -> Any:
        """Create a completion with retry on failure."""
        while True:
            try:
                return self.client.chat.completions.create(**self.completion_kwargs)
            except Exception as e:
                print(f"[ERROR] Failed to create completion: {e}")
                retry = input("Retry? (Y/n): ").strip()
                if retry.lower() == "n":
                    raise
