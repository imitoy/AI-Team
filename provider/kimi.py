"""Kimi / Moonshot provider — OpenAI-compatible API.

Base URL: https://api.moonshot.ai/v1
"""

import os

PROVIDER = {
    "name": "kimi",
    "display_name": "Kimi (Moonshot)",
    "api_type": "openai",
    "base_url": "https://api.moonshot.ai/v1",
    "env_key": "MOONSHOT_API_KEY",
    "api_key": os.getenv("MOONSHOT_API_KEY", ""),
    "models": {
        "kimi_k3": {
            "name": "kimi-k3",
            "description": "Kimi K3 — latest coding and reasoning model",
            "context_length": 256000,
        },
        "kimi_k2_6": {
            "name": "kimi-k2.6",
            "description": "Kimi K2.6 — strong coding with thinking mode",
            "context_length": 256000,
        },
        "moonshot_v1_128k": {
            "name": "moonshot-v1-128k",
            "description": "Moonshot V1 — general generation model, 128K context",
            "context_length": 128000,
        },
    },
}
