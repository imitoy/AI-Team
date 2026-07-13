return {
    name = "edit_file",
    description = 'Edit content of a file with replacement. Input should be in JSON format: {"file_name": "example.txt", "replace": "old content", "content": "new file content"}',
    tool = {
        type = "function",
        ["function"] = {
            name = "edit_file",
            description = 'Edit content of a file with replacement. Input should be in JSON format: {"file_name": "example.txt", "replace": "old content", "content": "new file content"}',
            parameters = {
                type = "object",
                properties = {
                    file_name = {
                        type = "string",
                        description = "The name of the file to edit"
                    },
                    replace = {
                        type = "string",
                        description = "The content to replace in the file"
                    },
                    content = {
                        type = "string",
                        description = "The new content to write to the file"
                    }
                },
                required = {"file_name", "replace", "content"}
            }
        }
    },
    action = function(input)
        local file_name = input.file_name
        local replace = input.replace  -- old text to find
        local content = input.content  -- new text to replace with
        -- Read the existing file content
        print("\\e[0;36mEditing file: ")
        print(replace)
        print("-> will be replaced as ->")
        print(content)
        print("-> in: " .. file_name)
        if not (AskProceed("edit_file")) then
            return { success = false, content = "Tool calling denied by user" }
        end
        local file, errmsg = io.open(file_name, "r")
        if not file then
            return { success = false, content = "Failed to read file:" .. errmsg }
        end
        local existing_content = file:read("*a")
        file:close()

        -- Perform a simple string substitution first (works for single-line,
        -- and avoids splitting logic whenever possible)
        local replaced
        do
            local s, e = string.find(existing_content, content, 1, true)
            if s then
                replaced = existing_content:sub(1, s - 1) .. content .. existing_content:sub(e + 1, -1)
            end
        end
        if replaced then
            file, errmsg = io.open(file_name, "w")
            if file then
                file:write(replaced)
                file:close()
                return { success = true, content = "File edited successfully" }
            else
                return { success = false, content = "Failed to write file: " .. errmsg }
            end
        end

        -- Fallback: line-by-line trim-agnostic matching for multi-line replacements
        local function lines(str)
            if str:sub(-1, -1) ~= "\n" then
                str = str .. "\n"
            end
            local index = 1
            return function()
                local new_index = str:find("\n", index)
                if not new_index then
                    return nil
                end
                local ret = str:sub(index, new_index - 1)
                index = new_index + 1
                return ret
            end
        end
        local function equal(str1, str2)
            str1 = str1:gsub("^ +", "")
            str1 = str1:gsub(" +$", "")
            str2 = str2:gsub("^ +", "")
            str2 = str2:gsub(" +$", "")
            return str1 == str2
        end
        local existing_content_table = {}
        local replace_table = {}
        local content_table = {}
        for line in lines(existing_content) do
            table.insert(existing_content_table, line)
        end
        for line in lines(replace) do
            table.insert(replace_table, line)
        end
        for line in lines(content) do
            table.insert(content_table, line)
        end
        local s
        for index, split in ipairs(existing_content_table) do
            local find = false
            if equal(split, replace_table[1]) then
                find = true
                for index_int, split_int in ipairs(replace_table) do
                    if not (equal(existing_content_table[index + index_int - 1], split_int)) then
                        find = false
                        break
                    end
                end
            end
            if find then
                s = index
                break
            end
        end
        if not s then
            return { success = false, content = "Replace content not found" }
        end
        -- Remove all matched lines starting at position s
        for i = 1, #replace_table do
            table.remove(existing_content_table, s)
        end
        -- Insert new content lines at position s
        for i = #content_table, 1, -1 do
            table.insert(existing_content_table, s, content_table[i])
        end
        existing_content = table.concat(existing_content_table, "\n")
        file, errmsg = io.open(file_name, "w")
        if file then
            file:write(existing_content)
            file:close()
            return { success = true, content = "File edited successfully" }
        else
            return { success = false, content = "Failed to edit file:" .. errmsg }
        end
    end
}