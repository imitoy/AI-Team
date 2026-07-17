"""Provider package — aggregates all model providers.

Each provider module defines a PROVIDER dict with:
    name:        Provider identifier
    display_name: Human-readable name
    api_type:    API interface type ("openai", "glm", "anthropic")
    base_url:    Default API endpoint
    env_key:     Environment variable for API key
    api_key:     Resolved API key
    models:      Dict of model_key -> {name, description, context_length, ...} (optional fallback)

Models can also be fetched dynamically via refresh_models() which calls
each provider's API to list available models.

Usage:
    from provider import MODELS, PROVIDERS, get_model, get_provider, refresh_models
"""

from __future__ import annotations

import importlib

_PROVIDER_MODULES = [
    "anthropic", "deepseek", "openrouter", "glm",
    "xai", "minimax", "kimi", "alibaba",
    "stepfun", "xiaomi", "novita",
]

MODELS: dict[str, dict] = {}
PROVIDERS: dict[str, dict] = {}


def _load_all():
    for mod_name in _PROVIDER_MODULES:
        try:
            mod = importlib.import_module(f"provider.{mod_name}")
            provider = mod.PROVIDER
            PROVIDERS[provider["name"]] = provider
            for model_key, model_info in provider.get("models", {}).items():
                _register_model(provider, model_key, model_info)
        except Exception as e:
            print(f"[WARN] Failed to load provider '{mod_name}': {e}")


def _register_model(provider: dict, model_key: str, model_info: dict):
    merged = {
        "api_type": provider["api_type"],
        "base_url": provider["base_url"],
        "api_key": provider["api_key"],
        "provider": provider["name"],
    }
    merged.update(model_info)
    MODELS[model_key] = merged


def refresh_models(provider_name: str | None = None):
    """Fetch available models from provider APIs and update the registry.

    Args:
        provider_name: Specific provider to refresh, or None for all.
    """
    providers_to_refresh = (
        [PROVIDERS[provider_name]] if provider_name
        else PROVIDERS.values()
    )
    for prov in providers_to_refresh:
        api_key = prov.get("api_key", "")
        if not api_key:
            continue
        api_type = prov["api_type"]
        base_url = prov["base_url"]
        try:
            if api_type == "anthropic":
                from api.anthropic import AnthropicAPI
                models = AnthropicAPI.list_models(api_key, base_url)
            elif api_type == "glm":
                from api.glm import GLMAPI
                models = GLMAPI.list_models(api_key, base_url)
            else:
                from api.openai import OpenAIAPI
                models = OpenAIAPI.list_models(api_key, base_url)

            if models:
                # Replace hardcoded models with API results
                # Remove old models for this provider
                old_keys = [k for k, v in MODELS.items() if v.get("provider") == prov["name"]]
                for k in old_keys:
                    del MODELS[k]
                # Register new models
                for m in models:
                    key = m["id"].replace("/", "_").replace(".", "_").replace("-", "_")
                    _register_model(prov, key, {
                        "name": m["id"],
                        "description": f"{m['id']} ({prov['display_name']})",
                    })
                print(f"[provider] Refreshed {len(models)} models from {prov['name']}")
        except Exception as e:
            print(f"[WARN] Failed to refresh models for {prov['name']}: {e}")


def get_model(model_key: str) -> dict | None:
    return MODELS.get(model_key)


def get_provider(provider_name: str) -> dict | None:
    return PROVIDERS.get(provider_name)


def list_models() -> list[str]:
    return list(MODELS.keys())


def list_providers() -> list[str]:
    return list(PROVIDERS.keys())


_load_all()
