return {
    name = "write_architect",
    description = 'Write architecture to ARCHITECT.md. Input should be in JSON format: {"content": "file content"}',
    tool = {
        type = "function",
        ["function"] = {
            name = "write_architect",
            description = 'Write architecture to ARCHITECT.md. Input should be in JSON format: {"content": "file content"}',
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
    action = function(input)
        local file_name = "ARCHITECT.md"
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