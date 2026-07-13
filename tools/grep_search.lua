return {
    name = "grep_search",
    description = "Search file contents using a regex pattern. Returns matching files with line numbers and content.",
    tool = {
        type = "function",
        ["function"] = {
            name = "grep_search",
            description = "Search file contents using a regex pattern. Returns matching files with line numbers. Supports basic regex patterns. Use this to find where a function is defined, search for specific code patterns, or locate references to a symbol.",
            parameters = {
                type = "object",
                properties = {
                    pattern = {
                        type = "string",
                        description = "The regex pattern to search for (e.g., 'function.*handle', 'local tools', 'require')"
                    },
                    file_glob = {
                        type = "string",
                        description = "Optional file glob to limit search (e.g., '*.lua', '*.py', '*.ts'). Default: all files."
                    }
                },
                required = {"pattern"}
            }
        }
    },
    action = function(input)
        local pattern = input.pattern
        local file_glob = input.file_glob
        local escaped_pattern = pattern:gsub("'", "'\\''")
        local cmd
        if file_glob and file_glob ~= "" then
            local escaped_glob = file_glob:gsub("'", "'\\''")
            cmd = "grep -rn --include='" .. escaped_glob .. "' '" .. escaped_pattern .. "' . --exclude-dir=.git 2>/dev/null | head -100"
        else
            cmd = "grep -rn '" .. escaped_pattern .. "' . --exclude-dir=.git 2>/dev/null | head -100"
        end
        local p = io.popen(cmd)
        if not p then
            return { success = false, content = "Failed to search files" }
        end
        local result = p:read("*a")
        p:close()
        if result == "" then
            return { success = true, content = "No matches found for: " .. pattern }
        end
        return { success = true, content = result }
    end
}