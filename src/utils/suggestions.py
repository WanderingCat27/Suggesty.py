from datetime import datetime

import nextcord

import d_bot as bot
import utils.json_utils as json_utils

class SuggestionMark: 
    def __init__(self, name : str, color_code : nextcord.Colour, push_to_log : bool):
        self.name = name
        self.color_code = color_code
        self.push_to_log = push_to_log
    
Accept = SuggestionMark("Accepted", nextcord.Colour.green(), True)
Wait = SuggestionMark("Waiting", nextcord.Colour.yellow(), False)
Deny = SuggestionMark("Denied", nextcord.Colour.red(), True)

COLOR_CODE = nextcord.Colour.from_rgb(59, 176, 255)
suggesty_id = "*** Suggesty Bot ***"

def is_suggestion_embed(m : nextcord.Message):
    return m.author.id == bot.BOT.user.id and len(m.embeds) > 0 and ((len(m.embeds[0].fields) > 0 and "submitter" in m.embeds[0].fields[0].name.lower()) or (m.embeds[0].footer.text != nextcord.Embed.Empty and suggesty_id in m.embeds[0].footer.text))



def create_suggestion_embed(message, user : nextcord.User): 
    e = nextcord.Embed(color=COLOR_CODE)
    # e.set_thumbnail("https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fcdn.pixabay.com%2Fphoto%2F2016%2F03%2F30%2F02%2F21%2Fidea-1289871_960_720.jpg&f=1&nofb=1")
    n = user.nick
    if n == None:
        n = user.name
    e.set_author(name=n, icon_url=user.avatar.url)


    e.title="**Suggestion**:"
    e.description=message
    e.set_footer(text=suggesty_id + ' • user-id: ' + str(user.id))
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
    a : nextcord.Message
    r = json_utils.get_role()
    c = ''
    if r != None:
        c = r.mention
    a = await json_utils.get_suggestion_channel().send(content=c, embed=create_suggestion_embed(message, user))
    await a.add_reaction(json_utils.get_up_emoji())
    await a.add_reaction(json_utils.get_down_emoji())
    await a.create_thread(name="Discussion")

async def create_finished_suggestion_embed(suggestion_message : nextcord.Message, reason : str, status : SuggestionMark) -> nextcord.Embed:
    suggestion_embed = suggestion_message.embeds[0]
    if suggestion_embed.footer.text == nextcord.Embed.Empty or suggesty_id not in suggestion_embed.footer.text:
        return create_finished_suggestion_embed_old(suggestion_message, reason, status)  
    for r in suggestion_message.reactions:
        r : nextcord.Reaction
        if r.emoji == json_utils.get_up_emoji():
            num_pro = r.count - 1
        elif r.emoji == json_utils.get_down_emoji():
            num_against = r.count - 1

    e = nextcord.Embed()

    e.color = status.color_code
    e.title = status.name
    e.description = suggestion_embed.description

    e.set_author(name=suggestion_embed.author.name, icon_url=suggestion_embed.author.icon_url)
    # e.set_thumbnail("https://www.publicdomainpictures.net/pictures/120000/velka/office-stamp.jpg")
    
    t = suggestion_embed.timestamp.strftime("%b %d %y %I:%M %p")

    if reason != "":
        e.add_field(name='Reason', value=reason)
    e.add_field(name="Votes", value="{num_pro} {json_utils.get_up_emoji()} to {num_against} {json_utils.get_down_emoji()}")
    
    s = suggestion_embed.footer.text.split('user-id: ')
    id = ''
    if len(s) > 1:
        id = ' • user-id: ' + s[1]
    e.set_footer(text=f"Submitted: {t}{id}")

    return e

async def create_finished_suggestion_embed_old(suggestion_message : nextcord.Message, reason : str, status : SuggestionMark):
    suggestion_content = suggestion_message.embeds[0].fields[0].value
    submitter = suggestion_message.embeds[0].fields[0].name

    passed : bool
    if status == Accept:
        passed = True
    elif status == Deny:
        passed = False

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

async def mark(id, reason, status : SuggestionMark):
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
    if not is_suggestion_embed(m):
        print("invalid suggestion message seleceted")
        return False
    if status.push_to_log: 
        e = await create_finished_suggestion_embed(m, reason, status)
        e : nextcord.Embed
        c = ''
        if e.footer.text != nextcord.Embed.Empty and 'user-id' in e.footer.text:
            c = log.guild.get_member(int(e.footer.text.split('user-id: ')[1])).mention

        await log.send(content=c, embed=e)
        await m.delete()
    else:
        e = m.embeds[0].copy()
        e.color = status.color_code 
        e.title = "Suggestion -- " + status.name + ":"
        r = ""
        if reason:
            r = "- " + reason + "\n"
        if e.footer.text == nextcord.Embed.Empty:
            e.set_footer(text=r)
        else:
            e.set_footer(text= r + e.footer.text)
        await  m.edit(embed=e)
    return True
