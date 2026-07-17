"""OpenRouter provider — OpenAI-compatible aggregator API."""

import os

PROVIDER = {
    "name": "openrouter",
    "display_name": "OpenRouter",
    "api_type": "openai",
    "base_url": "https://openrouter.ai/api/v1",
    "env_key": "OPENROUTER_API_KEY",
    "api_key": os.getenv("OPENROUTER_API_KEY", ""),
    "models": {},  # OpenRouter has 100+ models, fetch via refresh_models()
}
