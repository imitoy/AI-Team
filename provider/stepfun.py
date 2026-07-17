"""StepFun provider."""

import os

PROVIDER = {
    "name": "stepfun",
    "display_name": "StepFun",
    "api_type": "openai",
    "base_url": "https://api.stepfun.ai/step_plan/v1",
    "env_key": "STEPFUN_API_KEY",
    "api_key": os.getenv("STEPFUN_API_KEY", ""),
    "models": {},
}
