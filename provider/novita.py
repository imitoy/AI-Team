"""NovitaAI provider — OpenAI-compatible API aggregator."""

import os

PROVIDER = {
    "name": "novita",
    "display_name": "NovitaAI",
    "api_type": "openai",
    "base_url": "https://api.novita.ai/openai/v1",
    "env_key": "NOVITA_API_KEY",
    "api_key": os.getenv("NOVITA_API_KEY", ""),
    "models": {
        "novita_deepseek_v3": {
            "name": "deepseek/deepseek-v3-0324",
            "description": "DeepSeek V3 via NovitaAI",
            "context_length": 64000,
        },
        "novita_kimi_k2": {
            "name": "moonshotai/kimi-k2.5",
            "description": "Kimi K2.5 via NovitaAI",
            "context_length": 128000,
        },
        "novita_glm_5": {
            "name": "zai-org/glm-5",
            "description": "GLM-5 via NovitaAI",
            "context_length": 128000,
        },
    },
}
