from email.message import Message
import nextcord
from datetime import datetime

import d_bot as bot
import utils.json_utils as json_utils

COLOR_CODE = nextcord.Colour.from_rgb(145, 206, 255)


def create_suggestion_embed(message, user : nextcord.User): 
    e = nextcord.Embed(color=COLOR_CODE)
    e.set_thumbnail("https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fcdn.pixabay.com%2Fphoto%2F2016%2F03%2F30%2F02%2F21%2Fidea-1289871_960_720.jpg&f=1&nofb=1")
    e.add_field(name = f"**Submitter** -- {user.display_name}", value=message)
    e.timestamp = datetime.now()
    return e


def create_command_success_embed(text : str):
    e = nextcord.Embed(color=nextcord.Colour.green())
    e.add_field(name = "Success", value=text)
    return e

def create_command_error_embed(text : str):
    e = nextcord.Embed(color=nextcord.Colour.red())
    e.add_field(name = "Failed", value=text)
    return e



async def create_suggestion(message, user):
    a = await json_utils.get_suggestion_channel().send(embed=create_suggestion_embed(message, user))
    await a.add_reaction(json_utils.get_up_emoji())
    await a.add_reaction(json_utils.get_down_emoji())

async def create_finished_suggestion_embed(suggestion_message, reason : str, passed : bool):
    suggestion_content = suggestion_message.embeds[0].fields[0].value
    submitter = suggestion_message.embeds[0].fields[0].name
    print(submitter)

    for r in  suggestion_message.reactions:
        r : nextcord.Reaction
        if r.emoji == json_utils.get_up_emoji():
            num_pro = r.count - 1
        elif r.emoji == json_utils.get_down_emoji():
            num_against = r.count - 1
            
    e = nextcord.Embed()
    if passed:
        e.color = nextcord.Colour.green()
        e.add_field(name = f"Passed \n{submitter}", value=suggestion_content)
    else:
        e.color = nextcord.Colour.red()
        e.add_field(name = f"Rejected \n{submitter}", value=suggestion_content)
    e.set_thumbnail("https://www.publicdomainpictures.net/pictures/120000/velka/office-stamp.jpg")
    t = suggestion_message.embeds[0].timestamp.strftime("%b %d %y %I:%M %p")
    e.set_footer(text=f"reason: {reason}\n\n{num_pro} voted for this suggestion \n{num_against} voted against \nsuggestion was created at {t}")

    return e

async def mark(id, reason, status):
    passed = False
    if status.lower() == "accept":
        passed = True
    elif status.lower() == "deny":
        passed = False
    else:
        return True # ignores hold rn -- not implemented
    log = json_utils.get_suggestion_log_channel()
    if log == None:
        print("no log file")
        return False
    try:
        m = await json_utils.get_suggestion_channel().fetch_message(id)
    except:
        print("message not found")
        return False
    m : nextcord.Message
    if m.author.id != bot.BOT.user.id or len(m.embeds) <= 0 or "submitter" not in m.embeds[0].fields[0].name.lower():
        print("invalid suggestion message seleceted")
        return False 
    await log.send(embed= await create_finished_suggestion_embed(m, reason, passed))
    await m.delete()
    return True
