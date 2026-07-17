"""StepFun provider — OpenAI-compatible API with coding plan support."""

import os

PROVIDER = {
    "name": "stepfun",
    "display_name": "StepFun",
    "api_type": "openai",
    "base_url": "https://api.stepfun.ai/step_plan/v1",
    "env_key": "STEPFUN_API_KEY",
    "api_key": os.getenv("STEPFUN_API_KEY", ""),
    "models": {
        "step_3_5": {
            "name": "step-3.5",
            "description": "Step 3.5 — flagship model",
            "context_length": 128000,
        },
        "step_3_5_flash": {
            "name": "step-3.5-flash",
            "description": "Step 3.5 Flash — fast and efficient",
            "context_length": 128000,
        },
    },
}
