local luapython = require("luapython")

return {
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
                required = luapython.list {}
            }
        }
    },
    action = function(input)
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
}