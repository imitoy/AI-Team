local tools = {}

-- Load all tool files in order
local tool_files = {
    "json_output",
    "get_weather",
    "call_role_architect",
    "call_role_coder",
    "call_role_organizer",
    "call_role_reviewer",
    "call_role_security",
    "call_role_tester",
    "write_file",
    "read_file",
    "edit_file",
    "list_files",
    "run_command",
    "kill_process",
    "read_architect",
    "write_architect",
    -- Browser tools
    "browser_navigate",
    "browser_snapshot",
    "browser_click",
    "browser_type",
    "browser_scroll",
    "browser_back",
    "browser_press",
    "browser_console",
    -- Claude Code coding tools
    "glob_files",
    "grep_search",
}

for _, name in ipairs(tool_files) do
    table.insert(tools, require("tools." .. name))
end

-- Set up metatable for name-based access
local metatable = {
    __index = function(table, key)
        if tonumber(key) then
            return rawget(table, key)
        end
        for _, tool in ipairs(tools) do
            if rawget(tool, "name") == key then
                return tool
            end
        end
        return nil
    end
}

setmetatable(tools, metatable)

return tools