"""Xiaomi MiMo provider."""

import os

PROVIDER = {
    "name": "xiaomi",
    "display_name": "Xiaomi MiMo",
    "api_type": "openai",
    "base_url": "https://api.xiaomimimo.com/v1",
    "env_key": "XIAOMI_API_KEY",
    "api_key": os.getenv("XIAOMI_API_KEY", ""),
    "models": {},
}
