"""xAI provider — Grok models."""

import os

PROVIDER = {
    "name": "xai",
    "display_name": "xAI (Grok)",
    "api_type": "openai",
    "base_url": "https://api.x.ai/v1",
    "env_key": "XAI_API_KEY",
    "api_key": os.getenv("XAI_API_KEY", ""),
    "models": {
        "grok": {
            "name": "grok-4.3",
            "description": "Grok 4.3 — flagship reasoning model",
            "context_length": 1000000,
        },
    },
}
