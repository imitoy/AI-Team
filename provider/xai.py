"""xAI provider — Grok models via OpenAI-compatible API."""

import os

PROVIDER = {
    "name": "xai",
    "display_name": "xAI (Grok)",
    "api_type": "openai",
    "base_url": "https://api.x.ai/v1",
    "env_key": "XAI_API_KEY",
    "api_key": os.getenv("XAI_API_KEY", ""),
    "models": {
        "grok_4_3": {
            "name": "grok-4.3",
            "description": "Grok 4.3 — latest flagship reasoning model",
            "context_length": 1000000,
        },
        "grok_4_3_fast": {
            "name": "grok-4.3-fast",
            "description": "Grok 4.3 Fast — speed-optimized",
            "context_length": 1000000,
        },
        "grok_code": {
            "name": "grok-code-1",
            "description": "Grok Code — code generation specialist",
            "context_length": 128000,
        },
    },
}
