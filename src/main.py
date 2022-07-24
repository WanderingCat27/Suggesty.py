import nextcord
from nextcord.ext import commands
from os import getenv
from dotenv import load_dotenv
import d_bot as bot

from slash_commands.commands import register_commands
from utils.json_utils import get_suggestion_channel, get_watching
from utils.suggestions import create_suggestion




@bot.BOT.event
async def on_ready():
    print("bot is now ready")

@bot.BOT.event
async def on_message(message : nextcord.Message):
    if get_watching() and message.channel == get_suggestion_channel() and message.author.id != bot.BOT.user.id and message.type == nextcord.MessageType.default:
        await create_suggestion(message.content, message.author)
        await message.delete()

load_dotenv()
register_commands(bot.BOT)



bot.BOT.run(getenv("TOKEN"))