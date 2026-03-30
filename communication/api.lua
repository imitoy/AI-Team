local api = {}

local luapython = require "luapython"
local models = require "models"
local avatar = require "avatar"

function api.select(model)
    local model_info = models[model]
    return api[model_info.api_type]
end

api.openai = {}

api.openai.__index = api.openai

function api.openai.generatemessage(avatar_name)
    return {{role = "system", content = avatar.getAvatar(avatar_name or "Default").system}}
end

function api.openai.create(model, model_name, avatar_name)
    local openai_api = {}
    setmetatable(openai_api, api.openai)
    local OpenAI = luapython.import("openai.OpenAI")
    local client = OpenAI({
        api_key = model.authentication.api_key,
        base_url = model.base_url
    })
    openai_api.client = client
    openai_api.model = model
    openai_api.model_name = model_name
    openai_api.messages = api.openai.generatemessage(avatar_name)
    openai_api.completion_create = {
        model = model_name,
        messages = openai_api.messages,
        stream = true,
    }

    return openai_api
end

function api.openai:send(message)
    do
        local model = self.model
        local model_name = self.model_name
        local client = self.client
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
    table.insert(self.messages, {
        role = "user",
        content = message
    })
    local response = self.client.chat.completions.create(self.completion_create)
    self.response = response
end

function api.openai:get()
    local function getf()
        local message = ""
        for chunk in self.response() do
            local stream = chunk.choices[0].delta.content or chunk.choices[0].delta.reasoning_content
            message = message .. (stream or "")
            coroutine.yield(false, stream, chunk.choices[0].delta.content or "")
        end
        table.insert(self.messages, {
            role = "assistant",
            content = message
        })
        return true, message
    end
    return getf
end

return api
