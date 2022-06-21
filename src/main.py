import nextcord
from nextcord.ext import commands
from os import getenv
from dotenv import load_dotenv
import slash_commands.commands as slashcommands

intents = nextcord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="$")

@bot.event
async def on_ready():
    print("bot is now ready")

load_dotenv()
test_guild = int(getenv("GUILD_ID"))

slashcommands.init(bot, test_guild)

bot.run(getenv("TOKEN"))