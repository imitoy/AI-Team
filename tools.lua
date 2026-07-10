local luapython = require("luapython")
local roles = require("roles")

if not luapython.isLoadedNative() then
    luapython.load()
end

local tools = {
        {
            name = "json_output",
            description = "Output the result in JSON format",
            handle = {
                communication = function (communication)
                    communication.api.completion_create.response_format = {
                        type = "json_object",
                    }
                end
            }
        },
        {
            name = "get_weather",-- for testing tool calling
            description = "Get current weather in a city. Input should be in JSON format: {\"city\": \"City Name\"}",
            tool = {
                type = "function",
                ["function"] = {
                    name = "get_weather",
                    description = "Get current weather in a city. Input should be in JSON format: {\"city\": \"City Name\"}",
                    parameters = {
                        type = "object",
                        properties = {
                            city = {
                                type = "string",
                                description = "The name of the city to get weather for"
                            }
                        },
                        required = {"city"}
                    }
                }
            },
            action = function (input)
                local city = input.city
                -- Here you would normally call a weather API to get the actual weather data.
                -- For demonstration purposes, we'll return a mock weather report.
                local weather_report = "The current weather in " .. city .. " is sunny with a temperature of 25°C."
                return { success = true, content = weather_report }
            end
        },
        {
            name = "call_role_architect",
            description = "Call other co-workers to complete your mission. Your choices are: " .. (function(role_self)
                local role_names = {}
                for i, role in ipairs(roles) do
                    if role.name ~= role_self then
                        table.insert(role_names, tostring(i) .. ". " .. role.name.." - "..role.description)
                    end
                end
                return table.concat(role_names, "\n")
            end)("architect"),
            tool = {
                type = "function",
                ["function"] = {
                    name = "call_role",
                    description = "Call other co-workers to complete your mission. Your choices are: " .. (function()
                        local role_names = {}
                        for i, role in ipairs(roles) do
                            table.insert(role_names, tostring(i) .. ". " .. role.name.." - "..role.description)
                        end
                        return table.concat(role_names, "\n")
                    end)(),
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
            action = function (input)
                if not(AskProceed("call_role")) then
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
        },
         {
            name = "call_role_coder",
            description = "Call other co-workers to complete your mission. Your choices are: " .. (function(role_self)
                local role_names = {}
                for i, role in ipairs(roles) do
                    if role.name ~= role_self then
                        table.insert(role_names, tostring(i) .. ". " .. role.name.." - "..role.description)
                    end
                end
                return table.concat(role_names, "\n")
            end)("coder"),
            tool = {
                type = "function",
                ["function"] = {
                    name = "call_role",
                    description = "Call other co-workers to complete your mission. Your choices are: " .. (function()
                        local role_names = {}
                        for i, role in ipairs(roles) do
                            table.insert(role_names, tostring(i) .. ". " .. role.name.." - "..role.description)
                        end
                        return table.concat(role_names, "\n")
                    end)(),
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
            action = function (input)
                if not(AskProceed("call_role")) then
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
        },
       {
            name = "call_role_organizer",
            description = "Call other co-workers to complete your mission. Your choices are: " .. (function(role_self)
                local role_names = {}
                for i, role in ipairs(roles) do
                    if role.name ~= role_self then
                        table.insert(role_names, tostring(i) .. ". " .. role.name.." - "..role.description)
                    end
                end
                return table.concat(role_names, "\n")
            end)("organizer"),
            tool = {
                type = "function",
                ["function"] = {
                    name = "call_role",
                    description = "Call other co-workers to complete your mission. Your choices are: " .. (function()
                        local role_names = {}
                        for i, role in ipairs(roles) do
                            table.insert(role_names, tostring(i) .. ". " .. role.name.." - "..role.description)
                        end
                        return table.concat(role_names, "\n")
                    end)(),
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
            action = function (input)
                if not(AskProceed("call_role")) then
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
        },
{
            name = "call_role_reviewer",
            description = "Call other co-workers to complete your mission. Your choices are: " .. (function(role_self)
                local role_names = {}
                for i, role in ipairs(roles) do
                    if role.name ~= role_self then
                        table.insert(role_names, tostring(i) .. ". " .. role.name.." - "..role.description)
                    end
                end
                return table.concat(role_names, "\n")
            end)("reviewer"),
            tool = {
                type = "function",
                ["function"] = {
                    name = "call_role",
                    description = "Call other co-workers to complete your mission. Your choices are: " .. (function()
                        local role_names = {}
                        for i, role in ipairs(roles) do
                            table.insert(role_names, tostring(i) .. ". " .. role.name.." - "..role.description)
                        end
                        return table.concat(role_names, "\n")
                    end)(),
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
            action = function (input)
                if not(AskProceed("call_role")) then
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
        },
{
            name = "call_role_security",
            description = "Call other co-workers to complete your mission. Your choices are: " .. (function(role_self)
                local role_names = {}
                for i, role in ipairs(roles) do
                    if role.name ~= role_self then
                        table.insert(role_names, tostring(i) .. ". " .. role.name.." - "..role.description)
                    end
                end
                return table.concat(role_names, "\n")
            end)("security"),
            tool = {
                type = "function",
                ["function"] = {
                    name = "call_role",
                    description = "Call other co-workers to complete your mission. Your choices are: " .. (function()
                        local role_names = {}
                        for i, role in ipairs(roles) do
                            table.insert(role_names, tostring(i) .. ". " .. role.name.." - "..role.description)
                        end
                        return table.concat(role_names, "\n")
                    end)(),
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
            action = function (input)
                if not(AskProceed("call_role")) then
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
        },
{
            name = "call_role_test",
            description = "Call other co-workers to complete your mission. Your choices are: " .. (function(role_self)
                local role_names = {}
                for i, role in ipairs(roles) do
                    if role.name ~= role_self then
                        table.insert(role_names, tostring(i) .. ". " .. role.name.." - "..role.description)
                    end
                end
                return table.concat(role_names, "\n")
            end)("test"),
            tool = {
                type = "function",
                ["function"] = {
                    name = "call_role",
                    description = "Call other co-workers to complete your mission. Your choices are: " .. (function()
                        local role_names = {}
                        for i, role in ipairs(roles) do
                            table.insert(role_names, tostring(i) .. ". " .. role.name.." - "..role.description)
                        end
                        return table.concat(role_names, "\n")
                    end)(),
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
            action = function (input)
                if not(AskProceed("call_role")) then
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
        },

        {
            name = "write_file",
            description = "Write content to a file. Input should be in JSON format: {\"file_name\": \"example.txt\", \"content\": \"file content\"}",
            tool = {
                type = "function",
                ["function"] = {
                    name = "write_file",
                    description = "Write content to a file. Input should be in JSON format: {\"file_name\": \"example.txt\", \"content\": \"file content\"}",
                    parameters = {
                        type = "object",
                        properties = {
                            file_name = {
                                type = "string",
                                description = "The name of the file to write to"
                            },
                            content = {
                                type = "string",
                                description = "The content to write to the file"
                            }
                        },
                        required = {"file_name", "content"}
                    }
                }
            },
            action = function (input)
                local file_name = input.file_name
                local content = input.content
                print("\\e[0;36mWriting file: ")
                print(content)
                print("-> will be written to: "..file_name)
                if not(AskProceed("write_file")) then
                    return { success = false, message = "Tool calling denied by user" }
                end
                local file, errmsg = io.open(file_name, "w")
                if file then
                    file:write(content)
                    file:close()
                    return { success = true, content = "File written successfully" }
                else
                    return { success = false, content = "Failed to write file: "..errmsg }
                end
            end
        },
        {
            name = "read_file",
            description = "Read content from a file. Input should be in JSON format: {\"file_name\": \"example.txt\"}",
            tool = {
                type = "function",
                ["function"] = {
                    name = "read_file",
                    description = "Read content from a file. Input should be in JSON format: {\"file_name\": \"example.txt\"}",
                    parameters = {
                        type = "object",
                        properties = {
                            file_name = {
                                type = "string",
                                description = "The name of the file to read from"
                            }
                        },
                        required = {"file_name"}
                    }
                }
            },
            action = function (input)
                local file_name = input.file_name
                -- Read content from the specified file
                local file, errmsg = io.open(file_name, "r")
                if file then
                    local content = file:read("*a")
                    file:close()
                    if not content then
                        return { success = false, content = "File not found" }
                    end
                    return { success = true, content = content }
                else
                    return { success = false, content = "Failed to read file:"..errmsg }
                end
            end
        },
        {
            name = "edit_file",
            description = "Edit content of a file with replacement. Input should be in JSON format: {\"file_name\": \"example.txt\", \"replace\": \"old content\", \"content\": \"new file content\"}",
            tool = {
                type = "function",
                ["function"] = {
                    name = "edit_file",
                    description = "Edit content of a file with replacement. Input should be in JSON format: {\"file_name\": \"example.txt\", \"replace\": \"old content\", \"content\": \"new file content\"}",
                    parameters = {
                        type = "object",
                        properties = {
                            file_name = {
                                type = "string",
                                description = "The name of the file to edit"
                            },
                            replace = {
                                type = "string",
                                description = "The content to replace in the file"
                            },
                            content = {
                                type = "string",
                                description = "The new content to write to the file"
                            }
                        },
                        required = {"file_name", "replace", "content"}
                    }
                }
            },
            action = function (input)
                local file_name = input.file_name
                local replace = input.replace  -- old text to find
                local content = input.content  -- new text to replace with
                -- Read the existing file content
                print("\\e[0;36mEditing file: ")
                print(replace)
                print("-> will be replaced as ->")
                print(content)
                print("-> in: "..file_name)
                if not(AskProceed("edit_file")) then
                    return { success = false, content = "Tool calling denied by user" }
                end
                local file, errmsg = io.open(file_name, "r")
                if not file then
                    return { success = false, content = "Failed to read file:"..errmsg }
                end
                local existing_content = file:read("*a")
                file:close()

                -- Perform a simple string substitution first (works for single-line,
                -- and avoids splitting logic whenever possible)
                local replaced
                do
                    local s, e = string.find(replace, content, 1, true)
                    if s then
                        replaced = replace:sub(1, s-1)..content..replace:sub(e+1,-1)
                    end
                end
                if replaced then
                    file, errmsg = io.open(file_name, "w")
                    if file then
                        file:write(replaced)
                        file:close()
                        return { success = true, content = "File edited successfully" }
                    else
                        return { success = false, content = "Failed to write file: "..errmsg }
                    end
                end

                -- Fallback: line-by-line trim-agnostic matching for multi-line replacements
                local function lines(str)
                    if str:sub(-1, -1) ~= "\n" then
                        str = str .. "\n"
                    end
                    local index = 1
                    return function()
                        local new_index = str:find("\n", index)
                        if not new_index then
                            return nil
                        end
                        local ret = str:sub(index, new_index-1)
                        index = new_index + 1
                        return ret
                    end
                end
                local function equal(str1, str2)
                    str1 = str1:gsub("^ +", "")
                    str1 = str1:gsub(" +$", "")
                    str2 = str2:gsub("^ +", "")
                    str2 = str2:gsub(" +$", "")
                    return str1 == str2
                end
                local existing_content_table = {}
                local replace_table = {}
                local content_table = {}
                for line in lines(existing_content) do
                    table.insert(existing_content_table, line)
                end
                for line in lines(replace) do
                    table.insert(replace_table, line)
                end
                for line in lines(content) do
                    table.insert(content_table, line)
                end
                local s
                for index, split in ipairs(existing_content_table) do
                    local find = false
                    if equal(split, replace_table[1]) then
                        find = true
                        for index_int, split_int in ipairs(replace_table) do
                            if not(equal(existing_content_table[index+index_int-1], split_int)) then
                                find = false
                                break
                            end
                        end
                    end
                    if find then
                        s = index
                        break
                    end
                end
                if not s then
                    return { success = false, content = "Replace content not found" }
                end
                -- Remove all matched lines starting at position s
                for i = 1, #replace_table do
                    table.remove(existing_content_table, s)
                end
                -- Insert new content lines at position s
                for i = #content_table, 1, -1 do
                    table.insert(existing_content_table, s, content_table[i])
                end
                existing_content = table.concat(existing_content_table, "\n")
                file, errmsg = io.open(file_name, "w")
                if file then
                    file:write(existing_content)
                    file:close()
                    return { success = true, content = "File edited successfully" }
                else
                    return { success = false, content = "Failed to edit file:"..errmsg }
                end
            end
        },
        {
            name = "list_files",
            description = "List all files in the current directory",
            tool = {
                type = "function",
                ["function"] = {
                    name = "list_files",
                    description = "List all files in the current directory",
                    parameters = {
                        type = "object",
                        properties = {},
                        required = luapython.list{}
                    }
                }
            },
            action = function (input)
                local files_content
                local p = io.popen("ls -R")
                if not p then
                    return { success = false, content = "Failed to list files" }
                end
                files_content = p:read("*a")
                p:close()
                return { success = true, content = files_content }
            end
        },
        {
            name = "run_command",
            description = "Run a shell command. Input should be in JSON format: {\"command\": \"ls -l\", \"detach\": false}",
            tool = {
                type = "function",
                ["function"] = {
                    name = "run_command",
                    description = "Run a shell command. Input should be in JSON format: {\"command\": \"ls -l\", \"detach\": false}",
                    parameters = {
                        type = "object",
                        properties = {
                            command = {
                                type = "string",
                                description = "The shell command to run"
                            },
                            detach = {
                                type = "boolean",
                                description = "Wheather to detach the process. Turn it on if you run a background long process.",
                            }
                        },
                        required = {"command", "detach"}
                    }
                }
            },
            action = function (input)
                local command = input.command
                local detach = input.detach
                print("\\e[0;36mRunning command: ")
                print(command)
                print("-> will be executed")
                if not(AskProceed("run_command")) then
                    return { success = false, content = "Command execution denied by user" }
                end
                if detach then
                    local luv = require("luv")
                    local execute_str = "os.execute(\""..string.format("%q", command).."\")"
                    local id = os.time()
                    local thread = luv.new_thread(execute_str)
                    _G.run_command = _G.run_command or {}
                    _G.run_command[id] = thread
                    return { success = true, content = "Execute staring with run id "..id }
                else
                    local p = io.popen(command)
                    if not p then
                        return { success = false, content = "Failed to run command" }
                    end
                    local result = p:read("*a")
                    p:close()
                    return { success = true, content = result }
                end
            end
        },
        {
            name = "kill_process",
            description = "Kill a detached process. Input should be in JSON format: {\"id\": \"1783687230\"}",
            tool = {
                type = "function",
                ["function"] = {
                    name = "kill_process",
                    description = "Kill a detached process. Input should be in JSON format: {\"id\": \"1783687230\"}",
                    parameters = {
                        type = "object",
                        properties = {
                            id = {
                                type = "string",
                                description = "The process id to kill"
                            },
                        },
                        required = {"id"}
                    }
                }
            },
            action = function (input)
                local id = input.id
                if not(AskProceed("kill_process")) then
                    return { success = false, content = "Command execution denied by user" }
                end
                if _G.run_command[tostring(id)] then
                end
            end
        },
        {
            name = "read_architect",
            description = "Read ARCHITECT.md.",
            tool = {
                type = "function",
                ["function"] = {
                    name = "read_architect",
                    description = "Read ARCHITECT.md",
                    parameters = {
                        type = "object",
                        properties = {},
                        required = luapython.list{}
                    }
                }
            },
            action = function (input)
                local file_name = "ARCHITECT.md"
                -- Read content from the specified file
                local file, errmsg = io.open(file_name, "r")
                if file then
                    local content = file:read("*a")
                    file:close()
                    return { success = true, content = content }
                else
                    return { success = true, content = "File is empty. " }
                end
            end
        },
        {
            name = "write_architect",
            description = "Write architecture to ARCHITECT.md. Input should be in JSON format: {\"content\": \"file content\"}",
            tool = {
                type = "function",
                ["function"] = {
                    name = "write_architect",
                    description = "Write architecture to ARCHITECT.md. Input should be in JSON format: {\"content\": \"file content\"}",
                    parameters = {
                        type = "object",
                        properties = {
                            content = {
                                type = "string",
                                description = "The content to write to the ARCHITECT.md"
                            }
                        },
                        required = {"content"}
                    }
                }
            },
            action = function (input)
                local file_name = "ARCHITECT.md"
                local content = input.content
                print("\\e[0;36mWriting file: ")
                print(content)
                print("-> will be written to: "..file_name)
                if not(AskProceed("write_file")) then
                    return { success = false, message = "Tool calling denied by user" }
                end
                local file, errmsg = io.open(file_name, "w")
                if file then
                    file:write(content)
                    file:close()
                    return { success = true, content = "File written successfully" }
                else
                    return { success = false, content = "Failed to write file: "..errmsg }
                end
            end
        },
    }

    local metatable = {
        __index = function(table, key)
            if tonumber(key) then
                return rawget(table, key)
            end
            for _, tool in ipairs(table) do
                if rawget(tool, "name") == key then
                    return tool
                end
            end
            return nil
        end
    }

    setmetatable(tools, metatable)

    return tools
