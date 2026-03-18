local api = {}

local luapython = require"luapython"
local models = require"models"
local avatar = require"avatar"

function api.select(model){
    local model_info = models[model]
    return api[model_info.api_type]
}

api.openai = {}

function api.openai.create(model)
    local OpenAI = luapython.import"openai.OpenAI"
    local client = OpenAI({
        api_key = model.authentication.api_key,
        base_url = model.base_url
    })
    return client
end

function api.openai.