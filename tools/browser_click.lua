local BROWSER_SCRIPT = "tools/browser.py"

return {
    name = "browser_click",
    description = "Click on an element identified by its ref ID from the snapshot (e.g., '@e5').",
    tool = {
        type = "function",
        ["function"] = {
            name = "browser_click",
            description = "Click on an element identified by its ref ID from the snapshot (e.g., '@e5', '@e12'). The ref IDs are shown in square brackets in the snapshot output.",
            parameters = {
                type = "object",
                properties = {
                    ref = {
                        type = "string",
                        description = "The element reference from the snapshot (e.g., '@e5', '@e12')"
                    }
                },
                required = {"ref"}
            }
        }
    },
    action = function(input)
        local ref = input.ref
        local cmd = "python3 " .. BROWSER_SCRIPT .. " click " .. ref
        local p = io.popen(cmd)
        if not p then
            return { success = false, content = "Failed to click element" }
        end
        local result = p:read("*a")
        p:close()
        return { success = true, content = result }
    end
}