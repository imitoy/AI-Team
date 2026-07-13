return {
    name = "write_file",
    description = 'Write content to a file. Input should be in JSON format: {"file_name": "example.txt", "content": "file content"}',
    tool = {
        type = "function",
        ["function"] = {
            name = "write_file",
            description = 'Write content to a file. Input should be in JSON format: {"file_name": "example.txt", "content": "file content"}',
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
    action = function(input)
        local file_name = input.file_name
        local content = input.content
        print("\\e[0;36mWriting file: ")
        print(content)
        print("-> will be written to: " .. file_name)
        if not (AskProceed("write_file")) then
            return { success = false, message = "Tool calling denied by user" }
        end
        local file, errmsg = io.open(file_name, "w")
        if file then
            file:write(content)
            file:close()
            return { success = true, content = "File written successfully" }
        else
            return { success = false, content = "Failed to write file: " .. errmsg }
        end
    end
}