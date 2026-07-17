"""Kimi / Moonshot provider."""

import os

PROVIDER = {
    "name": "kimi",
    "display_name": "Kimi (Moonshot)",
    "api_type": "openai",
    "base_url": "https://api.moonshot.ai/v1",
    "env_key": "MOONSHOT_API_KEY",
    "api_key": os.getenv("MOONSHOT_API_KEY", ""),
    "models": {},
}
