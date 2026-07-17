"""Xiaomi MiMo provider — OpenAI-compatible API."""

import os

PROVIDER = {
    "name": "xiaomi",
    "display_name": "Xiaomi MiMo",
    "api_type": "openai",
    "base_url": "https://api.xiaomimimo.com/v1",
    "env_key": "XIAOMI_API_KEY",
    "api_key": os.getenv("XIAOMI_API_KEY", ""),
    "models": {
        "mimo_v2_omni": {
            "name": "mimo-v2-omni",
            "description": "MiMo V2 Omni — multimodal vision+text model",
            "context_length": 128000,
        },
        "mimo_v2": {
            "name": "mimo-v2",
            "description": "MiMo V2 — text generation model",
            "context_length": 128000,
        },
    },
}
