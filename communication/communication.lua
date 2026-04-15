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
    mcmanager.ccurrent = nil
    return mcmanager
end

function cmanager:newCommunication(content, avatar_name)
    model = model or self.model
    local avatar_obj = avatar.getAvatar(avatar_name)
    if not avatar_obj then
        error("Avatar "..avatar_name.." not found")
    end
    local c = communication:new(model, avatar_obj)
    table.insert(self.clist, c)
    self.ccurrent = c
    if content then
        self:send(content)
    end
end

function cmanager:send(content)
    local c = self.ccurrent
    local f = c:send(content)
    local co = coroutine.create(f)
    local message
    do
        local p1, p2 = false, false
        while true do
            local ret, finished, stream, is_reasoning = coroutine.resume(co)
            if not ret then
                error("Execute failed: "..finished)
            elseif finished then
                message = stream
                break
            end
            if is_reasoning == true then
                if p1 == false then
                    print("<Reasoning>")
                    p1 = true
                end
            elseif is_reasoning == false then
                if p2 == false then
                    print("</Reasoning>")
                    p2 = true
                end
            end
        end
    end
    return message
end

return cmanager
