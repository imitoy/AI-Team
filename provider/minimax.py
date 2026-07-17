"""MiniMax provider — OpenAI-compatible API."""

import os

PROVIDER = {
    "name": "minimax",
    "display_name": "MiniMax",
    "api_type": "openai",
    "base_url": "https://api.minimax.io/v1",
    "env_key": "MINIMAX_API_KEY",
    "api_key": os.getenv("MINIMAX_API_KEY", ""),
    "models": {
        "minimax_m3": {
            "name": "MiniMax-M3",
            "description": "MiniMax M3 — flagship with reasoning mode",
            "context_length": 1000000,
        },
        "minimax_m2": {
            "name": "MiniMax-M2.1",
            "description": "MiniMax M2.1 — fast and efficient",
            "context_length": 128000,
        },
        "minimax_m1": {
            "name": "MiniMax-M1",
            "description": "MiniMax M1 — open-weight hybrid reasoning model",
            "context_length": 256000,
        },
    },
}
