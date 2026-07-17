"""DeepSeek provider — OpenAI-compatible API."""

import os

PROVIDER = {
    "name": "deepseek",
    "display_name": "DeepSeek",
    "api_type": "openai",
    "base_url": "https://api.deepseek.com/v1/",
    "env_key": "DEEPSEEK_API_KEY",
    "api_key": os.getenv("DEEPSEEK_API_KEY", ""),
    "models": {
        "deepseek_chat": {
            "name": "deepseek-chat",
            "description": "DeepSeek Chat — general-purpose model",
            "context_length": 64000,
        },
        "deepseek_v4_flash": {
            "name": "deepseek-v4-flash",
            "description": "DeepSeek V4 Flash — fast and cost-effective",
            "context_length": 64000,
        },
    },
}
