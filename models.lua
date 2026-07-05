local models = {}

models.deepseek_v4_flash = {
    name = "deepseek-v4-flash",
    description = "DeepSeek",
    base_url = "https://api.deepseek.com/v1/",
    api_type = "openai",
    authentication = {
        method = "API Key",
        api_key = os.getenv("DEEPSEEK_API_KEY"),
        --header = "Authorization: Bearer YOUR_API_KEY"
    },
    tools = {}
}

models.deepseek_v4_flash_openrouter = {
    name = "deepseek/deepseek-v4-flash",
    description = "DeepSeek",
    base_url = "https://openrouter.ai/api/v1/chat/completions",
    api_type = "openai",
    authentication = {
        method = "API Key",
        api_key = os.getenv("OPENROUTER_API_KEY"),
        --header = "Authorization: Bearer YOUR_API_KEY"
    },
    tools = {}
}

return models
