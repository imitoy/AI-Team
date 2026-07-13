return {
    name = "run_command",
    description = 'Run a shell command. Input should be in JSON format: {"command": "ls -l", "detach": false}',
    tool = {
        type = "function",
        ["function"] = {
            name = "run_command",
            description = 'Run a shell command. Input should be in JSON format: {"command": "ls -l", "detach": false}',
            parameters = {
                type = "object",
                properties = {
                    command = {
                        type = "string",
                        description = "The shell command to run"
                    },
                    detach = {
                        type = "boolean",
                        description = "Wheather to detach the process. Turn it on if you run a background long process."
                    }
                },
                required = {"command", "detach"}
            }
        }
    },
    action = function(input)
        local command = input.command
        local detach = input.detach
        print("\\e[0;36mRunning command: ")
        print(command)
        print("-> will be executed")
        if not (AskProceed("run_command")) then
            return { success = false, content = "Command execution denied by user" }
        end
        if detach then
            local luv = require("luv")
            local execute_str = "os.execute(\"" .. string.format("%q", command) .. "\")"
            local id = os.time()
            local thread = luv.new_thread(execute_str)
            _G.run_command = _G.run_command or {}
            _G.run_command[id] = thread
            return { success = true, content = "Execute staring with run id " .. id }
        else
            local p = io.popen(command)
            if not p then
                return { success = false, content = "Failed to run command" }
            end
            local result = p:read("*a")
            p:close()
            return { success = true, content = result }
        end
    end
}