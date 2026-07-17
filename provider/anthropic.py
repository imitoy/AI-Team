"""Anthropic provider — native Anthropic API."""

import os

PROVIDER = {
    "name": "anthropic",
    "display_name": "Anthropic",
    "api_type": "anthropic",
    "base_url": "https://api.anthropic.com",
    "env_key": "ANTHROPIC_API_KEY",
    "api_key": os.getenv("ANTHROPIC_API_KEY", ""),
    "models": {
        "claude_sonnet_4": {
            "name": "claude-sonnet-4-20250514",
            "description": "Claude Sonnet 4 — balanced performance",
            "context_length": 200000,
        },
    },
}
