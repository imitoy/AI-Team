local BROWSER_SCRIPT = "tools/browser.py"

return {
    name = "browser_snapshot",
    description = "Get a text-based snapshot of the current page's accessibility tree. Shows interactive elements with ref IDs.",
    tool = {
        type = "function",
        ["function"] = {
            name = "browser_snapshot",
            description = "Get a text snapshot of the current page. Returns interactive elements with ref IDs (like @e1, @e2) for use with browser_click. Compact by default, use full=true for complete content.",
            parameters = {
                type = "object",
                properties = {
                    full = {
                        type = "boolean",
                        description = "If true, return complete page content. If false (default), return compact view with interactive elements only."
                    }
                },
                required = {}
            }
        }
    },
    action = function(input)
        local flag = ""
        if input and input.full then
            flag = " --full"
        end
        local cmd = "python3 " .. BROWSER_SCRIPT .. " snapshot" .. flag
        local p = io.popen(cmd)
        if not p then
            return { success = false, content = "Failed to get snapshot" }
        end
        local result = p:read("*a")
        p:close()
        return { success = true, content = result }
    end
}