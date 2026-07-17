"""NovitaAI provider."""

import os

PROVIDER = {
    "name": "novita",
    "display_name": "NovitaAI",
    "api_type": "openai",
    "base_url": "https://api.novita.ai/openai/v1",
    "env_key": "NOVITA_API_KEY",
    "api_key": os.getenv("NOVITA_API_KEY", ""),
    "models": {},
}
