local BROWSER_SCRIPT = "tools/browser.py"

return {
    name = "browser_type",
    description = "Type text into an input field identified by its ref ID. Clears the field first, then types the new text.",
    tool = {
        type = "function",
        ["function"] = {
            name = "browser_type",
            description = "Type text into an input field identified by its ref ID (e.g., '@e3'). Clears the field first, then types the new text.",
            parameters = {
                type = "object",
                properties = {
                    ref = {
                        type = "string",
                        description = "The element reference from the snapshot (e.g., '@e3')"
                    },
                    text = {
                        type = "string",
                        description = "The text to type into the field"
                    }
                },
                required = {"ref", "text"}
            }
        }
    },
    action = function(input)
        local ref = input.ref
        local text = input.text
        -- Escape single quotes for shell
        local safe_text = text:gsub("'", "'\\''")
        local cmd = "python3 " .. BROWSER_SCRIPT .. " type " .. ref .. " '" .. safe_text .. "'"
        local p = io.popen(cmd)
        if not p then
            return { success = false, content = "Failed to type" }
        end
        local result = p:read("*a")
        p:close()
        return { success = true, content = result }
    end
}