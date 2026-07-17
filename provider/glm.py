"""GLM (Zhipu AI) provider."""

import os

PROVIDER = {
    "name": "glm",
    "display_name": "GLM (Zhipu AI)",
    "api_type": "glm",
    "base_url": "https://open.bigmodel.cn/api/paas/v4/",
    "env_key": "GLM_API_KEY",
    "api_key": os.getenv("GLM_API_KEY", os.getenv("ZHIPUAI_API_KEY", "")),
    "models": {
        "glm_5": {
            "name": "glm-5",
            "description": "GLM-5 — flagship model with thinking mode",
            "context_length": 128000,
        },
    },
}
