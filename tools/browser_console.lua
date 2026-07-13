local BROWSER_SCRIPT = "tools/browser.py"

return {
    name = "browser_console",
    description = "Get browser console output and JavaScript errors from the current page. Returns console.log/warn/error/info messages and uncaught JS exceptions.",
    tool = {
        type = "function",
        ["function"] = {
            name = "browser_console",
            description = "Get browser console output and JavaScript errors from the current page. Returns console.log/warn/error/info messages and uncaught JS exceptions. Use this to detect silent errors, failed API calls, and application warnings.",
            parameters = {
                type = "object",
                properties = {
                    clear = {
                        type = "boolean",
                        description = "If true, clear the message buffers after reading"
                    }
                },
                required = {}
            }
        }
    },
    action = function(input)
        local flag = ""
        if input and input.clear then
            flag = " --clear"
        end
        local cmd = "python3 " .. BROWSER_SCRIPT .. " console" .. flag
        local p = io.popen(cmd)
        if not p then
            return { success = false, content = "Failed to get console output" }
        end
        local result = p:read("*a")
        p:close()
        return { success = true, content = result }
    end
}