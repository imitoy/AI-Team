return {
    name = "read_file",
    description = 'Read content from a file. Input should be in JSON format: {"file_name": "example.txt"}',
    tool = {
        type = "function",
        ["function"] = {
            name = "read_file",
            description = 'Read content from a file. Input should be in JSON format: {"file_name": "example.txt"}',
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
    action = function(input)
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
            return { success = false, content = "Failed to read file:" .. errmsg }
        end
    end
}