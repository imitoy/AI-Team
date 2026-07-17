"""API package — factory that selects the right backend based on model's api_type."""

from __future__ import annotations

from provider import MODELS


def create_api(model_key: str, role_name: str):
    """Create an API client based on the model's api_type.

    Args:
        model_key: Key into MODELS dict (e.g. "deepseek_v4_flash", "glm_5")
        role_name: The role to configure system prompt and tools for.

    Returns:
        An API client instance (OpenAIAPI, GLMAPI, or AnthropicAPI).
    """
    model = MODELS[model_key]
    api_type = model.get("api_type", "openai")

    if api_type == "glm":
        from api.glm import GLMAPI
        return GLMAPI(model_key, role_name)
    elif api_type == "anthropic":
        from api.anthropic import AnthropicAPI
        return AnthropicAPI(model_key, role_name)
    else:
        from api.openai import OpenAIAPI
        return OpenAIAPI(model_key, role_name)
