local api = require("api")

local communication = {}

function communication:new(model)
	local mcommunication = {}
	setmetatable(mcommunication, { __index = self })
	mcommunication.api = api.select(model)
	mcommunication.client, mcommunication.model = mcommunication.api.create(model)
	return mcommunication
end

function communication:send(str, user)
	if type(user) == nil then
		user = "user"
	elseif type(user) ~= "string" then
		error("user: string expected, got " .. type(user))
	end
	return self.api.newchat(self.client, self.model, user, str)
end

return communication

