local api = require("api")
local json = require("cjson")
local tools = require("tools")

local _G = _G

do
    local registered = {}
    AskProceed = function(tag)
        if registered[tag] then
            return true
        end
        print("Proceed?[(Y)es/(n)o/(a)bort/yesforall]")
        local input = io.read()
        if input == "Y" or input == "y" then
            return true
        elseif input == "n" or input == "N" then
            return false
        elseif input == "a" or input == "A" then
            print("Abort.")
            os.exit(0)
        elseif input == "yesforall" then
            registered[tag] = true
            return true
        else
            print("Invalid input. Please enter 'Y', 'n', 'a', or 'yesforall'.")
            return AskProceed(tag)
        end
    end
end

local communication = {}

local registered = {}

communication.__index = communication

function communication.onTool(openai_api, id, tool_name, arguments)
    local tool = tools[tool_name]
    if not tool then
        openai_api:toolcall(id, tool_name, "Tool not found")
        return
    end
    if tool.action then
        local result = tool.action(arguments)
        openai_api:toolcall(id, tool_name, result.content)
    end
end

function communication:new(model, role_name)
    for _, registered_communication in ipairs(registered) do
        if registered_communication.role_name == role_name then
            registered_communication.model = model
            registered_communication.model_name = model.name
            return registered_communication
        end
    end
    local mcommunication = {}
    setmetatable(mcommunication, self)

    mcommunication.register = true
    mcommunication.api = api[model.api_type].create(model, role_name)
    mcommunication.api.onTool = communication.onTool
    mcommunication.model_name = model.name
    mcommunication.model = model
    mcommunication.id = os.time()

    table.insert(registered, mcommunication)
    return mcommunication
end

function communication:call(tool_name, arguments)
    local tools = self.model.tools
    for _, tool in ipairs(tools) do
        if tool.name == tool_name then
            if tool.action then
                local result = tool.action(arguments)
                return true, result
            end
        end
    end
    return false, nil
end

function communication:appendUserMessage(message)
    if type(self) ~= "table" or not self.register then
        error("self: recognize failed")
    end
    self.api:appendUserMessage(message)
end

function communication:send()
    if type(self) ~= "table" or not self.register then
        error("self: recognize failed")
    end
    self.api:send()
    return message
end

return communication
