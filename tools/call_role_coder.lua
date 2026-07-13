local roles = require("roles")

local role_self = "coder"

local function build_description()
    local role_names = {}
    for i, role in ipairs(roles) do
        if role.name ~= role_self then
            table.insert(role_names, tostring(i) .. ". " .. role.name .. " - " .. role.description)
        end
    end
    return table.concat(role_names, "\n")
end

local function build_tool_description()
    local role_names = {}
    for i, role in ipairs(roles) do
        table.insert(role_names, tostring(i) .. ". " .. role.name .. " - " .. role.description)
    end
    return table.concat(role_names, "\n")
end

return {
    name = "call_role_coder",
    description = "Call other co-workers to complete your mission. Your choices are: " .. build_description(),
    tool = {
        type = "function",
        ["function"] = {
            name = "call_role",
            description = "Call other co-workers to complete your mission. Your choices are: " .. build_tool_description(),
            parameters = {
                type = "object",
                properties = {
                    role_name = {
                        type = "string",
                        description = "The name of the role to call"
                    },
                    input_data = {
                        type = "string",
                        description = "The input data to send to the called role"
                    }
                },
                required = {"role_name", "input_data"}
            }
        }
    },
    action = function(input)
        if not (AskProceed("call_role")) then
            return { success = false, message = "Tool calling denied by user" }
        end
        local role_name = input.role_name
        local input_data = input.input_data
        local communication = require("communication")
        local model = require("models").deepseek_v4_flash
        local comm = communication:new(model, role_name)
        comm:appendUserMessage(input_data)
        comm:send()
        local response_message = comm.api.messages[#comm.api.messages]
        print("[INFO] Final response:", response_message.content)
        return { success = true, content = response_message.content }
    end
}