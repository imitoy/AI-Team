local api = {}

local luapython = require "luapython"
local models = require "models"
local avatar = require "avatar"

function api.select(model)
    local model_info = models[model]
    return api[model_info.api_type]
end

api.openai = {}


api.openai.defaultmessage = {
    system = "You are a helpful assistant.",
}

function api.openai.generatemessage(avatar_name)
    if avatar_name == nil then
        return api.openai.defaultmessage
    end
    for i, v in ipairs(avatar) do
        if v.name == avatar_name then
            return v
        end
    end
    return nil
end

function api.openai.create(model)
    local OpenAI = luapython.impor("openai.OpenAI")
    local client = OpenAI({
        api_key = model.authentication.api_key,
        base_url = model.base_url
    })
    return client, model
end

function api.openai.send(client, model, model_name, messages)
    do
        local find = false
        for i, v in ipairs(model.models) do
            if v == model_name then
                find = true
            end
        end
        if not (find) then
            error("api.openai,send: model_name " .. model_name .. " not found")
        end
    end
    if type(messages) ~= "table" then
        error("api.openai.send: messages: table expected, got " .. type(messages))
    end
    local response = client.chat.completions.create({
        model = model_name,
        messages = messages,
        stream = true
    })
    return response
end

function api.openai.get(response, messages)
    local message = ""
    for chunk in response() do
        local stream = chunk.choices[0].delta.content
        message = message .. stream
        coroutine.yield(false, stream)
    end
    return true, messages
end

return api
