local models = {}

models.deepseek = {
    name = "DeepSeek",
    description = "DeepSeek",
    base_url = "https://api.deepseek.com/v1/",
    api_type = "openai",
    authentication = {
        method = "API Key",
        api_key = "YOUR_API_KEY",
        --header = "Authorization: Bearer YOUR_API_KEY"
    },
    models = {
        "deepseek-chat",
    }
}

return models
