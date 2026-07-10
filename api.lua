local api = {}

local luapython = require "luapython"
local models = require "models"
local json = require "cjson"
local roles = require "roles"
local tools = require "tools"

function api.select(model)
    local model_info = models[model]
    return api[model_info.api_type]
end

api.openai = {}

api.openai.OpenAI = luapython.import("openai.OpenAI")
api.openai.onTool = function(openai_api, id, tool_name, arguments) return openai_api, id, tool_name, arguments end
api.openai.__index = api.openai

function api.openai.generatemessage(role_name)
    return {{role = "system", content = roles[role_name].system_prompt}}
end

function api.openai.create(model, role_name)
    local openai_api = {}
    local model_name = model.name
    setmetatable(openai_api, api.openai)
    local OpenAI = api.openai.OpenAI
    local client = OpenAI({
        api_key = model.authentication.api_key,
        base_url = model.base_url
    })
    openai_api.client = client
    openai_api.model = model
    openai_api.model_name = model_name
    openai_api.messages = api.openai.generatemessage(role_name)
    openai_api.role_name = role_name
    openai_api.tools_index = {}
    
    local ctools = {}
    for _, tool_name in ipairs(roles[role_name].tools)do
        if tools[tool_name] and tools[tool_name].tool then
            table.insert(ctools, tools[tool_name].tool)
            openai_api.tools_index[tools[tool_name].tool["function"].name] = tool_name
        end
    end
    if #ctools == 0 then
        ctools = nil
    end
    openai_api.completion_create = {
        model = model_name,
        messages = openai_api.messages,
        tools = ctools,
        temperature = 0,
        reasoning_effort="medium",
        extra_body={thinking={type="enabled"}}
    }
    return openai_api
end

function api.openai:appendUserMessage(message)
    table.insert(self.messages, {role = "user", content = message})
    self.completion_create.messages = self.messages
    print("[INFO] Role: ", self.role_name)
    print("[INFO] User message appended:", message)
end

function api.openai:send()
    local function create_completion()
        local response = self.client.chat.completions.create(self.completion_create)
        return response
    end

    local response
    repeat
        local ok, response_in = pcall(create_completion)
        if not ok then
            print("[ERROR] Failed to create completion:", response_in)
            print("Retry? (Y/n)")
            local retry = io.read()
            if retry:lower() == "n" then
                print("[INFO] Aborting completion request.")
                return
            end
        else
            response = response_in
        end
    until ok

    local message = response.choices[0].message
    table.insert(self.messages, message)
    if message.tool_calls then
        for _, tool_call in ipairs(luapython.astable(message.tool_calls)) do
            print("[INFO] Role: ", self.role_name)
            print("[INFO] Tool call received:", tool_call["function"].name, tool_call["function"].arguments)
            local arguments = json.decode(tool_call["function"].arguments)
            self:onTool(tool_call.id, self.tools_index[tool_call["function"].name], arguments)
        end
        self:send()
    elseif message.content and #message.content > 0 then
        print("[INFO] Role: ", self.role_name)
        print("[INFO] Model response:", message.content)
    elseif message.reasoning_content and #message.reasoning_content > 0 then
        print("[INFO] Role: ", self.role_name)
        print("[INFO] Model reasoning content:", message.reasoning_content)
    end
end

function api.openai:toolcall(id, name, content)
    local message = {
        role = "tool",
        content = content,
        name = name,
        tool_call_id = id
    }
    table.insert(self.messages, message)
    self.completion_create.messages = self.messages
    print("[INFO] Role: ", self.role_name)
    print("[INFO] Tool call response appended:", name, content)
end

return api
