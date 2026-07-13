return {
    name = "glob_files",
    description = "Find files matching a glob pattern (e.g., '**/*.lua', '*.py', 'src/**/*.ts'). Uses glob-style pattern matching to locate files.",
    tool = {
        type = "function",
        ["function"] = {
            name = "glob_files",
            description = "Find files matching a glob pattern. Returns all file paths that match the given pattern. Examples: '**/*.lua' finds all Lua files recursively, '*.py' finds Python files in current directory.",
            parameters = {
                type = "object",
                properties = {
                    pattern = {
                        type = "string",
                        description = "The glob pattern to search for (e.g., '**/*.lua', '*.py', 'src/**/*.ts')"
                    }
                },
                required = {"pattern"}
            }
        }
    },
    action = function(input)
        local pattern = input.pattern
        -- Use find command with glob matching (Linux/Unix)
        local cmd = 'find . -path "./.git" -prune -o -path "' .. pattern:gsub("'", "'\\''") .. '" -print 2>/dev/null | head -200'
        -- But that's not quite right. Use fd or find with proper glob
        -- Better: use shopt -s globstar and find
        local escaped = pattern:gsub("'", "'\\''")
        local cmd2 = 'bash -c \'shopt -s globstar 2>/dev/null; ls -1d ' .. escaped .. ' 2>/dev/null; [[ $? -ne 0 ]] && find . -path "./.git" -prune -o -path "' .. escaped .. '" -print 2>/dev/null\' | head -200'
        local p = io.popen(cmd2)
        if not p then
            return { success = false, content = "Failed to search files" }
        end
        local result = p:read("*a")
        p:close()
        local lines = {}
        for line in result:gmatch("[^\n]+") do
            if line ~= "" then
                table.insert(lines, line)
            end
        end
        if #lines == 0 then
            return { success = true, content = "No files found matching: " .. pattern }
        end
        local output = table.concat(lines, "\n")
        return { success = true, content = output }
    end
}