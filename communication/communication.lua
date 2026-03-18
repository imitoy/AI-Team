local api = require"api"

local communication = {}

function communication:new(model)
    local mcommunication = {}
    

function communication:send(str, user)
    if type(user) == nil then
        user = "user"
    else type(user) ~= "string" then
        error("user: string expected, got "..type(user))
    end
    
    