local luapython = require("luapython")

return {
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
                required = luapython.list {}
            }
        }
    },
    action = function(input)
        local files_content
        local p = io.popen("ls -R")
        if not p then
            return { success = false, content = "Failed to list files" }
        end
        files_content = p:read("*a")
        p:close()
        return { success = true, content = files_content }
    end
}