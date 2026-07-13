local BROWSER_SCRIPT = "tools/browser.py"

return {
    name = "browser_press",
    description = "Press a keyboard key. Useful for submitting forms (Enter), navigating (Tab), or keyboard shortcuts.",
    tool = {
        type = "function",
        ["function"] = {
            name = "browser_press",
            description = "Press a keyboard key. Useful for submitting forms (Enter), navigating (Tab), or keyboard shortcuts like Escape.",
            parameters = {
                type = "object",
                properties = {
                    key = {
                        type = "string",
                        description = "Key to press (e.g., 'Enter', 'Tab', 'Escape', 'ArrowDown', 'ArrowUp')"
                    }
                },
                required = {"key"}
            }
        }
    },
    action = function(input)
        local key = input.key
        local cmd = "python3 " .. BROWSER_SCRIPT .. " press " .. key
        local p = io.popen(cmd)
        if not p then
            return { success = false, content = "Failed to press key" }
        end
        local result = p:read("*a")
        p:close()
        return { success = true, content = result }
    end
}