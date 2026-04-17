local api = {}

local luapython = require "luapython"
local models = require "models"
local json = require "cjson"

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
    for _, tool in ipairs(model.tools)do
        local add = false
        for _, tool_name in ipairs(avatar.tools)do
            if tool_name == tool.name and tool.tool then
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
    if type(message) == "string" then
        table.insert(self.messages, {
            role = "user",
            content = message
        })
    elseif type(message) ~= "nil" then
        error("message: string expected")
    end
    local response = self.client.chat.completions.create(self.completion_create)
    self.response = response
end

function api.openai:get()
    local function getf()
        local message = ""
        local message_content = ""
        local reasoning = true
        local tools = {}
        for chunk in self.response() do
            reasoning = chunk.choices[0].delta.reasoning_content ~= nil
            local stream = chunk.choices[0].delta.content or chunk.choices[0].delta.reasoning_content or ""
            message = message .. (stream or "")
            message_content = message_content .. (chunk.choices[0].delta.content or "")

            if chunk.choices[0].delta.tool_calls ~= nil then
                for _, tool_call in ipairs(luapython.astable(chunk.choices[0].delta.tool_calls)) do
                    local index = tool_call.index + 1
                    tools[index] = tools[index] or {}
                    tools[index].name = (tools[index].name or "") .. (tool_call['function'].name or "")
                    tools[index].arguments = (tools[index].arguments or "") .. (tool_call['function'].arguments or "")
                    tools[index].id = tools[index].id or (tool_call.id or "")
                    stream = stream .. (tool_call['function'].name or tool_call['function'].arguments or "")
                end
            end

            coroutine.yield(false, stream, reasoning)
        end

        do
            local tool_calls = nil
            if #tools > 0 then
                tool_calls = {}
                for _, tool in ipairs(tools) do
                    table.insert(tool_calls, {
                        ["function"] = {
                            name = tool.name,
                            arguments = tool.arguments
                        },
                        id = tostring(tool.id),
                        type = "function"
                    })
                end
            end
            table.insert(self.messages, {
                role = "assistant",
                content = message_content,
                tool_calls = tool_calls
            })
        end

        for _, tool in ipairs(tools) do
            tool.arguments = json.decode(tool.arguments)
        end

        local function tool_call_callback()
            for _, tool in ipairs(tools)do
                local result = coroutine.yield(false, tool)
                table.insert(self.messages, {
                    role = "tool",
                    content = result.content,
                    tool_call_id = tool.id,
                    name = tool.name
                })
            end
            return true
        end
        local cocall = coroutine.create(tool_call_callback)
        return true, message, cocall
    end
    return getf
end

return api
