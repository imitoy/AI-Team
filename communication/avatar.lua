local avatar = {
    {
        name = "Boss",
        system = "You are the boss",
    }
}

function avatar.getAvatar(name)
    for _, v in ipairs(avatar) do
        if v.name == name then
            return v
        end
    end
    return nil
end

return avatar