"""get_weather tool — mock weather lookup (for testing tool calling)."""

name = "get_weather"
description = 'Get current weather in a city. Input: {"city": "City Name"}'
schema = {
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": 'Get current weather in a city. Input: {"city": "City Name"}',
        "parameters": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "The name of the city to get weather for",
                }
            },
            "required": ["city"],
        },
    },
}


def action(input: dict) -> dict:
    city = input.get("city", "Unknown")
    weather_report = f"The current weather in {city} is sunny with a temperature of 25°C."
    return {"success": True, "content": weather_report}
