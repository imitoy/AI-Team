local models = {}

models.deepseek = {
    name = "DeepSeek",
    description = "DeepSeek",
    base_url = "https://api.deepseek.com/v1/",
    api_type = "openai",
    authentication = {
        method = "API Key",
        api_key = "sk-0515b8c266044807842aabdbe3c1d7ee",
        --header = "Authorization: Bearer YOUR_API_KEY"
    },
    models = {
        "deepseek-chat",
        "deepseek-reasoner",
    },
    tools = {
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
                print("Proceed?(Y/n)\\e[0m")
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
                local replace = input.replace
                local content = input.content
                -- Read the existing file content
                print("\\e[0;36mEditing file: ")
                print(replace)
                print("-> will be replaced as ->")
                print(content)
                print("-> in: "..file_name)
                print("Proceed?(Y/n)\\e[0m")
                if not(AskProceed("edit_file")) then
                    return { success = false, content = "Tool calling denied by user" }
                end
                local file, errmsg = io.open(file_name, "r")
                if not file then
                    return { success = false, content = "Failed to read file:"..errmsg }
                end
                local existing_content = file:read("*a")
                file:close()
                -- Replace the specified content
                existing_content = string.gsub(existing_content, replace, content)
                -- Write the updated content back to the file
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
                        required = {}
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
            description = "Run a shell command. Input should be in JSON format: {\"command\": \"ls -l\"}",
            tool = {
                type = "function",
                ["function"] = {
                    name = "run_command",
                    description = "Run a shell command. Input should be in JSON format: {\"command\": \"ls -l\"}",
                    parameters = {
                        type = "object",
                        properties = {
                            command = {
                                type = "string",
                                description = "The shell command to run"
                            }
                        },
                        required = {"command"}
                    }
                }
            },
            action = function (input)
                local command = input.command
                print("\\e[0;36mRunning command: ")
                print(command)
                print("-> will be executed")
                print("Proceed?(Y/n)\\e[0m")
                if not(AskProceed("run_command")) then
                    return { success = false, content = "Command execution denied by user" }
                end
                local p = io.popen(command)
                if not p then
                    return { success = false, content = "Failed to run command" }
                end
                local result = p:read("*a")
                p:close()
                return { success = true, content = result }
            end
        }
    }
}

return models
