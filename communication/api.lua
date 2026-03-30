local api = {}

local luapython = require"luapython"
local models = require"models"
local avatar = require"avatar"

function api.select(model)
    local model_info = models[model]
    return api[model_info.api_type]
end

api.openai = {}

function api.openai.create(model)
    local OpenAI = luapython.import"openai.OpenAI"
    local client = OpenAI({
        api_key = model.authentication.api_key,
        base_url = model.base_url
    })
    return client, model
end

function api.openai.newchat(client, model, origin, message)
    local response = client.chat.completions.create({
        model = model.model,
        messages = type(origin) == "table" and origin or {
            {role = "system", content = avatar.getAvatar(origin).system},
            {role = "user", content = message}
        },
        stream = false
    })
    return response.choices[0].message.content
end

return api