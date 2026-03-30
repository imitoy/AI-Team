local api = require("api")

local communication = {}

communication.__index = communication

function communication:new(model, model_name, avatar_name)
    local mcommunication = {}
    setmetatable(mcommunication, self)
    mcommunication.register = true
    mcommunication.api = api[model.api_type]
    mcommunication.client = mcommunication.api.create(model)
    mcommunication.avatat_name = avatar_name
    mcommunication.model_name = model_name
    mcommunication.model = model
    return mcommunication
end

function communication:send(str, user)
    if type(self) ~= "table" or not self.register then
        error("self: recognize failed")
    end
    if type(user) == nil then
        user = "user"
    elseif type(user) ~= "string" then
        error("user: string expected, got " .. type(user))
    end
    if not self.messages then
        self.messages = communication.api.generatemessages(self.avatar_name)
    end
    table.insert(self.messages)
    self.api.send(self.client, self.model, self.model_name, self.messages)
end

return communication
