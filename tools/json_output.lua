return {
    name = "json_output",
    description = "Output the result in JSON format",
    handle = {
        communication = function(communication)
            communication.api.completion_create.response_format = {
                type = "json_object",
            }
        end
    }
}