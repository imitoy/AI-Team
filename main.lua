package.path = package.path .. ";./communication/?.lua"

local models = require("communication.models")
local avatar = require("communication.avatar")
local api = require("communication.api")
local communication = require("communication.communication")
local luapython = require("luapython")
luapython.load()

local json = luapython.import("json")

local last_response = ""
local avatar_name = "Product_Manager"

local no_confirm = false

local comm_data = {}
local comm_content = {}

local function comm_create(avatar_name)
    local comm = communication:new(models.deepseek, avatar.getAvatar(avatar_name).model, avatar_name)
    table.insert(comm_data, comm)
    return comm
end

comm_create("Product_Manager")

while true do
    local content = last_response

    if #comm_data == 0 then
        print("No communication channel available. Abort.")
        break
    end
    local comm = comm_data[#comm_data]

    ::input_content::
    if not(comm_content[#comm_data]) then
        print("Input your prompt:")
        content = io.read()
        if content == "" then
            print("Input is empty.")
            goto input_content
        end
    end

    ::send::
    local f = comm:send(content)

    local co = coroutine.create(f)

    last_response = ""
    while true do
        local success, finished, value, input = coroutine.resume(co)
        if not success then
            error("coroutine error: " .. tostring(finished))
        end
        if finished then
            break
        else
            io.write(value)
            io.flush()
            last_response = last_response .. input
        end
    end
    print("")

    ::continue::
    local s = ""
    if not (no_confirm) then
        print("Continue? [ (Y)es / (r)eply / (a)bort / (n)o confirm ]")
        s = io.read()
        if s == "" then
            s = "Y"
        end
    end
    if s:sub(1, 1):lower() == "y" or no_confirm then
        if avatar_name == "Prompter" then
            local response_pyobj = json.loads(last_response)
            local response = luapython.astable(response_pyobj)
            local proceed = false
            for _, v in ipairs(response) do
                if(v.target ~= "nobody") then
                    local new_comm = comm_create(v.target)
                    proceed = true
                    comm_content[#comm_data] = v.content
                end
            end
            if not proceed then
                comm_content[#comm_data] = nil
                table.remove(comm_data, #comm_data)
            end
        else
            avatar_name = "Prompter"
            local comm = comm_create(avatar_name)
            comm_content[#comm_data] = last_response
        end
    elseif s:sub(1, 1):lower() == "r" then
        print("Reply:")
        comm_content[#comm_data] = nil
    elseif s:sub(1, 1):lower() == "a" then
        print("Abort.")
        break
    else
        print("Invalid input")
        goto continue
    end
end
