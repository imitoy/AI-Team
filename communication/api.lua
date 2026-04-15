local api = {}

local luapython = require "luapython"
local models = require "models"

function api.select(model)
    local model_info = models[model]
    return api[model_info.api_type]
end

api.openai = {}

api.openai.__index = api.openai

function api.openai.generatemessage(avatar)
    return {{role = "system", content = avatar.system}}
end

function api.openai.create(model, avatar)
    local openai_api = {}
    local model_name = avatar.model
    setmetatable(openai_api, api.openai)
    local OpenAI = luapython.import("openai.OpenAI")
    local client = OpenAI({
        api_key = model.authentication.api_key,
        base_url = model.base_url
    })
    openai_api.client = client
    openai_api.model = model
    openai_api.model_name = model_name
    openai_api.messages = api.openai.generatemessage(avatar)
    
    local tools = {}
    for _, tool in ipairs(models.tools)do
        local add = false
        for _, tool_name in ipairs(avatar.tools)do
            if tool_name == tool.name then
                add = true
                break
            end
        end
        if add then
            if tool.tool then
                table.insert(tools, tool.tool)
            end
        end
    end
    if #tools == 0 then
        tools = nil
    end
    openai_api.completion_create = {
        model = model_name,
        messages = openai_api.messages,
        stream = true,
        tools = tools
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
        local reasoning = true
        for chunk in self.response() do
            reasoning = chunk.choices[0].delta.content == nil
            local stream = chunk.choices[0].delta.content or chunk.choices[0].delta.reasoning_content
            message = message .. (stream or "")
            coroutine.yield(false, stream, reasoning)
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
