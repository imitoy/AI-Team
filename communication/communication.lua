local api = require("api")
local avatar = require("avatar")
local json = require("cjson")

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
                if tool.name == tool_name and tool.handle and tool.handle.communication then
                    tool.handle.communication(mcommunication)
                end
            end
        end
    end
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

function communication:send(content)
    if type(self) ~= "table" or not self.register then
        error("self: recognize failed")
    end
    self.api:send(content)
    local f = self.api:get()
    local co = coroutine.create(f)
    local message = ""
    do
        local p1, p2 = false, false
        while true do
            local ret, finished, stream, is_reasoning = coroutine.resume(co)
            if not ret then
                error("Execute failed: "..finished)
            elseif finished then
                local cocall = is_reasoning
                local continue = false
                local ctool = nil
                local lastret = nil
                local tool_call = false
                repeat
                    if ctool then
                        local ret, clastret = self:call(ctool.name, ctool.arguments)
                        lastret = clastret
                    end
                    tool_call = ctool and true or false
                    local ret, ccontinue, cctool = coroutine.resume(cocall, lastret)
                    continue = ccontinue
                    ctool = cctool
                until continue
                if tool_call then
                    return self:send(nil)
                else
                    break
                end
            end
            if is_reasoning == true then
                if p1 == false then
                    print("<Reasoning>")
                    p1 = true
                end
            elseif is_reasoning == false then
                if p2 == false then
                    print("\n</Reasoning>")
                    p2 = true
                end
            end
            io.write(stream)
            io.flush()
            if not is_reasoning then
                message = message .. stream
            end
        end
    end
    print("")
    return message
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
    local avatar_obj = avatar.getAvatar(avatar_name)
    if not avatar_obj then
        error("Avatar "..avatar_name.." not found")
    end
    local model = self.model
    local c = communication:new(model, avatar_obj)
    table.insert(self.clist, c)
    self.ccurrent = c
    if content then
        return self:send(content)
    end
end

function cmanager:terminateCommunication()
    self.clist[#self.clist] = nil
    self.ccurrent = self.clist[#self.clist]
end

function cmanager:send(content)
    local c = self.ccurrent
    local message = c:send(content)
    return message
end

function cmanager:start()
    print("Welcome to the AI Team Communication System!")
    print("Type your message and press Enter to send:")
    local content = io.read()
    local avatar_name = "项目经理"
    self:newCommunication(nil, avatar_name)
    while true do
        if #self.clist == 0 then
            print("No active communication. Exiting.")
            break
        end
        local response = self:send(content)
        print("\27[32mResponse: " .. response .. "\27[0m")
        if not AskProceed("continue") then
            break
        end
        response = json.decode(response)
        if response.target == "上级" then
            if #self.clist == 1 then
                print("Please enter your message:")
                content = io.read()
            else
                self:terminateCommunication()
            end
        else
            self:newCommunication(nil, response.target)
            content = response.content
        end
    end
end

return cmanager
