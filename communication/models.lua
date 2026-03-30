local models = {}

models.deepseek = {
    name = "DeepSeek",
    description = "DeepSeek",
    base_url = "https://api.deepseek.com/v1/",
    api_type = "openai",
    authentication = {
        method = "API Key",
        api_key = "sk-0515b8c266044807842aabdbe3c1d7ee",
        --header = "Authorization: Bearer YOUR_API_KEY"
    },
    models = {
        "deepseek-chat",
        "deepseek-reasoner",
    },
    tools = {
        {
            name = "json_output",
            description = "Output the result in JSON format",
            handle = {
                communication = function (communication)
                    communication.api.completion_create.response_format = {
                        type = "json_object",
                    }
                end
            }
        }
    }
}

return models
