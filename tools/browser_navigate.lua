local BROWSER_SCRIPT = "tools/browser.py"

return {
    name = "browser_navigate",
    description = "Navigate to a URL in the browser. Returns page snapshot automatically.",
    tool = {
        type = "function",
        ["function"] = {
            name = "browser_navigate",
            description = "Navigate to a URL in the browser. Returns the page title, URL, and a text snapshot of the page content.",
            parameters = {
                type = "object",
                properties = {
                    url = {
                        type = "string",
                        description = "The URL to navigate to (e.g. https://example.com)"
                    }
                },
                required = {"url"}
            }
        }
    },
    action = function(input)
        local url = input.url
        local cmd = "python3 " .. BROWSER_SCRIPT .. " navigate " .. url
        local p = io.popen(cmd)
        if not p then
            return { success = false, content = "Failed to start browser" }
        end
        local result = p:read("*a")
        p:close()
        return { success = true, content = result }
    end
}