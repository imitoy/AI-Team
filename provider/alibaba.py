"""Alibaba / DashScope provider."""

import os

PROVIDER = {
    "name": "alibaba",
    "display_name": "Alibaba Cloud (Qwen)",
    "api_type": "openai",
    "base_url": "https://dashscope-intl.aliyuncs.com/compatible-mode/v1",
    "env_key": "DASHSCOPE_API_KEY",
    "api_key": os.getenv("DASHSCOPE_API_KEY", ""),
    "models": {},
}
