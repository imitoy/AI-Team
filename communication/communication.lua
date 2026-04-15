local api = require("api")
local avatar = require("avatar")

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

communication.__index = communication

function communication:new(model, avatar_obj)
    local mcommunication = {}
    setmetatable(mcommunication, self)

    local avatar_name = avatar_obj.name

    mcommunication.register = true
    mcommunication.api = api[model.api_type].create(model, avatar_obj)
    mcommunication.avatar_name = avatar_name
    mcommunication.model_name = model.name
    mcommunication.model = model
    local avatar_obj = avatar_obj
    if not avatar_obj then
        error("avatar " .. avatar_name .. " not found")
    end
    if avatar_obj.tools then
        for _, tool_name in ipairs(avatar_obj.tools) do
            for _, tool in ipairs(model.tools) do
                if tool.name == tool_name then
                    tool.handle.communication(mcommunication)
                end
            end
        end
    end
    return mcommunication
end

function communication:send(content)
    if type(self) ~= "table" or not self.register then
        error("self: recognize failed")
    end
    self.api:send(content)
    return self.api:get()
end

local cmanager = {}

cmanager.__index = cmanager

function cmanager:new(model)
    local mcmanager = {}
    setmetatable(mcmanager, self)
    mcmanager.model = model
    mcmanager.clist = {}
    return mcmanager
end

function cmanager:newCommunication(content, avatar_name)
    model = model or self.model
    local avatar_obj = avatar.getAvatar(avatar_name)
    if not avatar_obj then
        error("Avatar "..avatar_name.." not found")
    end
    local c = communication:new(model, avatar_obj)

return communication
