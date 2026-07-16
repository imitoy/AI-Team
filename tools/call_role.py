"""call_role tools — delegate work to other team members.

Registers one call_role_<role> tool per role, each with a tailored description
listing the other available roles.
"""

from __future__ import annotations

from roles import ROLES, build_role_list

_DEFAULT_MODEL = "deepseek_v4_flash"


def _make_action(caller_role: str):
    """Create an action function for a specific caller role."""
    def _action(input: dict) -> dict:
        # Lazy imports to avoid circular dependency
        from communication import Communication, ask_proceed
        if not ask_proceed("call_role"):
            return {"success": False, "message": "Tool calling denied by user"}
        target_role = input.get("role_name", "")
        input_data = input.get("input_data", "")
        comm = Communication.get_or_create(_DEFAULT_MODEL, target_role)
        comm.append_user_message(input_data)
        comm.send()
        response = comm.last_response
        if response:
            print(f"[INFO] Final response from {target_role}: {response}")
            return {"success": True, "content": response}
        return {"success": False, "content": "No response from role"}
    return _action


TOOLS = []
for _role in ROLES:
    _rn = _role["name"]
    _desc = build_role_list(exclude=_rn)
    _full = build_role_list()
    TOOLS.append({
        "name": f"call_role_{_rn}",
        "description": f"Call other co-workers to complete your mission. Your choices are:\n{_desc}",
        "schema": {
            "type": "function",
            "function": {
                "name": "call_role",
                "description": f"Call other co-workers to complete your mission. Your choices are:\n{_full}",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "role_name": {
                            "type": "string",
                            "description": "The name of the role to call",
                        },
                        "input_data": {
                            "type": "string",
                            "description": "The input data to send to the called role",
                        },
                    },
                    "required": ["role_name", "input_data"],
                },
            },
        },
        "action": _make_action(_rn),
    })
