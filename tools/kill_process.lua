return {
    name = "kill_process",
    description = 'Kill a detached process. Input should be in JSON format: {"id": "1783687230"}',
    tool = {
        type = "function",
        ["function"] = {
            name = "kill_process",
            description = 'Kill a detached process. Input should be in JSON format: {"id": "1783687230"}',
            parameters = {
                type = "object",
                properties = {
                    id = {
                        type = "string",
                        description = "The process id to kill"
                    }
                },
                required = {"id"}
            }
        }
    },
    action = function(input)
        local id = input.id
        if not (AskProceed("kill_process")) then
            return { success = false, content = "Command execution denied by user" }
        end
        if _G.run_command[tostring(id)] then
        end
    end
}