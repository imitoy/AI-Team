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
                -- Write content to the specified file
                local file = io.open(file_name, "w")
                if file then
                    file:write(content)
                    file:close()
                    return { success = true, message = "File written successfully" }
                else
                    return { success = false, message = "Failed to write file" }
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
                local file = io.open(file_name, "r")
                if file then
                    local content = file:read("*a")
                    file:close()
                    return { success = true, content = content }
                else
                    return { success = false, message = "Failed to read file" }
                end
            end
        },
        {
            name = "edit_file",
            description = "Edit content of a file. Input should be in JSON format: {\"file_name\": \"example.txt\", \"content\": \"new file content\"}",
            tool = {
                type = "function",
                ["function"] = {
                    name = "edit_file",
                    description = "Edit content of a file. Input should be in JSON format: {\"file_name\": \"example.txt\", \"content\": \"new file content\"}",
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
                        required = {"file_name", "content"}
                    }
                }
            },
            action = function (input)
                local file_name = input.file_name
                local content = input.content
                -- Write content to the specified file
                local file = io.open(file_name, "w")
                if file then
                    file:write(content)
                    file:close()
                    return { success = true, message = "File edited successfully" }
                else
                    return { success = false, message = "Failed to edit file" }
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
                local files = {}
                local p = io.popen("ls")
                for file in io.popen("ls"):lines() do
                    table.insert(files, file)
                end
                return { success = true, files = files }
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
                local result = io.popen(command):read("*a")
                return { success = true, result = result }
            end
        }
    }
}

return models
