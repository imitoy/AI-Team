local BROWSER_SCRIPT = "tools/browser.py"

return {
    name = "browser_back",
    description = "Navigate back to the previous page in browser history.",
    tool = {
        type = "function",
        ["function"] = {
            name = "browser_back",
            description = "Navigate back to the previous page in browser history. Requires browser_navigate to be called first.",
            parameters = {
                type = "object",
                properties = {},
                required = {}
            }
        }
    },
    action = function(input)
        local cmd = "python3 " .. BROWSER_SCRIPT .. " back"
        local p = io.popen(cmd)
        if not p then
            return { success = false, content = "Failed to go back" }
        end
        local result = p:read("*a")
        p:close()
        return { success = true, content = result }
    end
}