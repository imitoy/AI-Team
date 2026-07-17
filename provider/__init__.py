"""Provider package — aggregates all model providers.

Each provider module defines a PROVIDER dict with:
    name:        Provider display name
    api_type:    API interface type ("openai", "glm", ...)
    base_url:    Default API endpoint
    env_key:     Environment variable for API key
    models:      Dict of model_key -> {name, description, ...}

Usage:
    from provider import MODELS, get_model, get_provider
"""

from __future__ import annotations

import importlib

# Ordered list of provider modules to load
_PROVIDER_MODULES = [
    "anthropic",
    "deepseek",
    "openrouter",
    "glm",
    "xai",
    "minimax",
    "kimi",
    "alibaba",
    "stepfun",
    "xiaomi",
    "novita",
]

# Aggregated model registry: model_key -> {name, description, api_type, base_url, api_key, ...}
MODELS: dict[str, dict] = {}

# Provider registry: provider_name -> provider dict
PROVIDERS: dict[str, dict] = {}


def _load_all():
    """Import each provider module and merge its models into the global registry."""
    for mod_name in _PROVIDER_MODULES:
        try:
            mod = importlib.import_module(f"provider.{mod_name}")
            provider = mod.PROVIDER
            PROVIDERS[provider["name"]] = provider
            # Merge provider-level fields into each model entry
            for model_key, model_info in provider.get("models", {}).items():
                merged = {
                    "api_type": provider["api_type"],
                    "base_url": provider["base_url"],
                    "api_key": provider["api_key"],
                    "provider": provider["name"],
                }
                merged.update(model_info)
                MODELS[model_key] = merged
        except Exception as e:
            print(f"[WARN] Failed to load provider '{mod_name}': {e}")


def get_model(model_key: str) -> dict | None:
    """Look up a model by key. Returns the model dict or None."""
    return MODELS.get(model_key)


def get_provider(provider_name: str) -> dict | None:
    """Look up a provider by name."""
    return PROVIDERS.get(provider_name)


def list_models() -> list[str]:
    """Return all registered model keys."""
    return list(MODELS.keys())


def list_providers() -> list[str]:
    """Return all registered provider names."""
    return list(PROVIDERS.keys())


# Auto-load on import
_load_all()
