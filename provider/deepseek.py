"""DeepSeek provider — OpenAI-compatible API.

Models: https://api.deepseek.com/v1/
"""

import os

PROVIDER = {
    "name": "deepseek",
    "display_name": "DeepSeek",
    "api_type": "openai",
    "base_url": "https://api.deepseek.com/v1/",
    "env_key": "DEEPSEEK_API_KEY",
    "api_key": os.getenv("DEEPSEEK_API_KEY", ""),
    "models": {
        "deepseek_v4_flash": {
            "name": "deepseek-v4-flash",
            "description": "DeepSeek V4 Flash — fast and cost-effective",
            "context_length": 64000,
        },
        "deepseek_v4": {
            "name": "deepseek-v4",
            "description": "DeepSeek V4 — full capability model",
            "context_length": 64000,
        },
        "deepseek_r1": {
            "name": "deepseek-reasoner",
            "description": "DeepSeek R1 — reasoning model",
            "context_length": 64000,
        },
    },
}
