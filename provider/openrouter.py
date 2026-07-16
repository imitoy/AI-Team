"""OpenRouter provider — OpenAI-compatible aggregator API.

Models: https://openrouter.ai/api/v1
Supports many models from different providers through a single API.
"""

import os

PROVIDER = {
    "name": "openrouter",
    "display_name": "OpenRouter",
    "api_type": "openai",
    "base_url": "https://openrouter.ai/api/v1",
    "env_key": "OPENROUTER_API_KEY",
    "api_key": os.getenv("OPENROUTER_API_KEY", ""),
    "models": {
        "deepseek_v4_flash_openrouter": {
            "name": "deepseek/deepseek-v4-flash",
            "description": "DeepSeek V4 Flash via OpenRouter",
            "context_length": 64000,
        },
        "claude_sonnet_4": {
            "name": "anthropic/claude-sonnet-4",
            "description": "Claude Sonnet 4 via OpenRouter",
            "context_length": 200000,
        },
        "gpt_4o": {
            "name": "openai/gpt-4o",
            "description": "GPT-4o via OpenRouter",
            "context_length": 128000,
        },
        "gemini_2_pro": {
            "name": "google/gemini-2-pro",
            "description": "Gemini 2 Pro via OpenRouter",
            "context_length": 1000000,
        },
    },
}
