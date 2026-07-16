"""GLM (Zhipu AI) provider — uses the zhipuai SDK.

Models: https://open.bigmodel.cn/api/paas/v4/
Docs:   https://docs.bigmodel.cn
"""

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
        "glm_5_flash": {
            "name": "glm-5-flash",
            "description": "GLM-5 Flash — fast and lightweight",
            "context_length": 128000,
        },
        "glm_4_air": {
            "name": "glm-4-air",
            "description": "GLM-4 Air — cost-effective general model",
            "context_length": 128000,
        },
    },
}
