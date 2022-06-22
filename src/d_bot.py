from nextcord.ext import commands
import nextcord

intents = nextcord.Intents.default()
intents.message_content = True

global BOT
BOT = commands.Bot(command_prefix="$", intents=intents)

async def get_bot():
    global bot
    return BOT