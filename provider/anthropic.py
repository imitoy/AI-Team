"""Anthropic provider — native Anthropic API (Claude models).

NOTE: api_type is "anthropic" which uses a non-OpenAI-compatible transport.
This provider is listed for model reference only; implementation needs a native adapter.
"""

import os

PROVIDER = {
    "name": "anthropic",
    "display_name": "Anthropic",
    "api_type": "anthropic",
    "base_url": "https://api.anthropic.com",
    "env_key": "ANTHROPIC_API_KEY",
    "api_key": os.getenv("ANTHROPIC_API_KEY", ""),
    "models": {
        "anthropic_opus_4": {
            "name": "claude-opus-4-20250514",
            "description": "Claude Opus 4 — strongest reasoning and coding",
            "context_length": 200000,
        },
        "anthropic_sonnet_4": {
            "name": "claude-sonnet-4-20250514",
            "description": "Claude Sonnet 4 — balanced performance",
            "context_length": 200000,
        },
        "anthropic_haiku_4": {
            "name": "claude-haiku-4-20250514",
            "description": "Claude Haiku 4 — fast and lightweight",
            "context_length": 200000,
        },
    },
}
