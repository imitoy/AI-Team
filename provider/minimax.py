"""MiniMax provider."""

import os

PROVIDER = {
    "name": "minimax",
    "display_name": "MiniMax",
    "api_type": "openai",
    "base_url": "https://api.minimax.io/v1",
    "env_key": "MINIMAX_API_KEY",
    "api_key": os.getenv("MINIMAX_API_KEY", ""),
    "models": {},
}
