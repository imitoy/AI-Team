local BROWSER_SCRIPT = "tools/browser.py"

return {
    name = "browser_scroll",
    description = "Scroll the page in a direction. Use this to reveal more content below or above the current viewport.",
    tool = {
        type = "function",
        ["function"] = {
            name = "browser_scroll",
            description = "Scroll the page in a direction. Use 'down' to reveal more content below the current viewport, 'up' to scroll back.",
            parameters = {
                type = "object",
                properties = {
                    direction = {
                        type = "string",
                        description = "Direction to scroll: 'up' or 'down'",
                        enum = {"up", "down"}
                    }
                },
                required = {"direction"}
            }
        }
    },
    action = function(input)
        local direction = input.direction
        local cmd = "python3 " .. BROWSER_SCRIPT .. " scroll " .. direction
        local p = io.popen(cmd)
        if not p then
            return { success = false, content = "Failed to scroll" }
        end
        local result = p:read("*a")
        p:close()
        return { success = true, content = result }
    end
}