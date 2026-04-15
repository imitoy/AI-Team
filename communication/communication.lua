local api = require("api")
local avatar = require("avatar")

local communication = {}

communication.__index = communication

function communication:new(model, model_name, avatar_name)
    local mcommunication = {}
    setmetatable(mcommunication, self)
    mcommunication.register = true
    mcommunication.api = api[model.api_type].create(model, model_name, avatar_name)
    mcommunication.avatar_name = avatar_name or "Default"
    mcommunication.model_name = model_name
    mcommunication.model = model
    local avatar_obj = avatar.getAvatar(avatar_name)
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
