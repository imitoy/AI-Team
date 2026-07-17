"""Alibaba / DashScope provider — Qwen models via OpenAI-compatible API.

Base URL: https://dashscope-intl.aliyuncs.com/compatible-mode/v1
"""

import os

PROVIDER = {
    "name": "alibaba",
    "display_name": "Alibaba Cloud (Qwen)",
    "api_type": "openai",
    "base_url": "https://dashscope-intl.aliyuncs.com/compatible-mode/v1",
    "env_key": "DASHSCOPE_API_KEY",
    "api_key": os.getenv("DASHSCOPE_API_KEY", ""),
    "models": {
        "qwen3_max": {
            "name": "qwen3-max",
            "description": "Qwen3 Max — flagship general-purpose model",
            "context_length": 131072,
        },
        "qwen3_plus": {
            "name": "qwen3-plus",
            "description": "Qwen3 Plus — balanced performance and cost",
            "context_length": 131072,
        },
        "qwen3_turbo": {
            "name": "qwen3-turbo",
            "description": "Qwen3 Turbo — fast inference for high-throughput",
            "context_length": 131072,
        },
        "qwen_coder": {
            "name": "qwen3-coder-plus",
            "description": "Qwen3 Coder Plus — code generation specialist",
            "context_length": 131072,
        },
    },
}
