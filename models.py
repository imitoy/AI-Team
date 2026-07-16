"""Model configurations for AI-Team."""

import os


MODELS = {
    "deepseek_v4_flash": {
        "name": "deepseek-v4-flash",
        "description": "DeepSeek",
        "base_url": "https://api.deepseek.com/v1/",
        "api_type": "openai",
        "api_key": os.getenv("DEEPSEEK_API_KEY", ""),
    },
    "deepseek_v4_flash_openrouter": {
        "name": "deepseek/deepseek-v4-flash",
        "description": "DeepSeek via OpenRouter",
        "base_url": "https://openrouter.ai/api/v1",
        "api_type": "openai",
        "api_key": os.getenv("OPENROUTER_API_KEY", ""),
    },
    "glm_5": {
        "name": "glm-5",
        "description": "Zhipu GLM-5",
        "api_type": "glm",
        "api_key": os.getenv("GLM_API_KEY", os.getenv("ZHIPUAI_API_KEY", "")),
    },
    "glm_5_flash": {
        "name": "glm-5-flash",
        "description": "Zhipu GLM-5 Flash (fast)",
        "api_type": "glm",
        "api_key": os.getenv("GLM_API_KEY", os.getenv("ZHIPUAI_API_KEY", "")),
    },
}
