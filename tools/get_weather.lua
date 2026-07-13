return {
    name = "get_weather",
    description = 'Get current weather in a city. Input should be in JSON format: {"city": "City Name"}',
    tool = {
        type = "function",
        ["function"] = {
            name = "get_weather",
            description = 'Get current weather in a city. Input should be in JSON format: {"city": "City Name"}',
            parameters = {
                type = "object",
                properties = {
                    city = {
                        type = "string",
                        description = "The name of the city to get weather for"
                    }
                },
                required = {"city"}
            }
        }
    },
    action = function(input)
        local city = input.city
        -- Here you would normally call a weather API to get the actual weather data.
        -- For demonstration purposes, we'll return a mock weather report.
        local weather_report = "The current weather in " .. city .. " is sunny with a temperature of 25°C."
        return { success = true, content = weather_report }
    end
}