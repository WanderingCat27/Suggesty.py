import json

import nextcord

from d_bot import BOT

file_loc = "data.json"
with open(file_loc, 'r', encoding="utf8") as f:
    data = json.load(f)

def get():
    return data

def save():
    json_object = json.dumps(data, indent = 4)
    with open(file_loc, "w", encoding="utf8") as f:
        f.write(json_object)

def set_role(role : nextcord.Role):
    data["role-id"] = role.id
    save()

def get_role() ->  nextcord.role:
    if "role-id" not in data:
        return None
    c = data["suggestion-channel-id"]
    if c == None:
        return None

    return get_suggestion_channel().guild.get_role(data["role-id"])

def get_suggestion_channel() ->  nextcord.abc.GuildChannel:
    if "suggestion-channel-id" not in data:
        return None
    return BOT.get_channel(data["suggestion-channel-id"])

def set_suggestion_channel(channel : nextcord.abc.GuildChannel):
    data["suggestion-channel-id"] = channel.id
    save()

def get_suggestion_log_channel() -> nextcord.abc.GuildChannel:
    if "suggestion-log-channel-id" not in data:
        return None
    return BOT.get_channel(data["suggestion-log-channel-id"])

def set_suggestion_log_channel(channel : nextcord.abc.GuildChannel):
    data["suggestion-log-channel-id"] = channel.id
    save()



def get_up_emoji():
    return data["up"]
def get_down_emoji():
    return data["down"]

def get_watching():
    if "watch_suggestion_channel" in data:
        return data["watch_suggestion_channel"]
    else:
        data["watch_suggestion_channel"] = True
        save()
        return True

def set_watching(b : bool):
    data["watch_suggestion_channel"] = b
    save()