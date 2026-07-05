luapython = require("luapython")
luapython.load()

local models = require("models")
local api = require("api")
local communication = require("communication")

local c = communication:new(models.deepseek_v4_flash, "organizer")
print("Communication created with model:", c.model_name)

while true do
    io.write("Enter your message (or type 'exit' to quit): ")
    local user_input = io.read()
    if user_input == "exit" then
        break
    end

    c.api:appendUserMessage(user_input)
    c.api:send()

    -- Assuming the API returns a response in c.api.messages
    local last_message = c.api.messages[#c.api.messages]
    print("Model response:", last_message.content)
end