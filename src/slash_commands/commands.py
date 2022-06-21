from nextcord.ext import commands
from nextcord import Embed, Interaction, SlashOption

# suggestion bot commands
# suggest
# accept
# decline
# maybe/discussing/hold
# anon suggest
# suggest channel
# suggest log channel


def init(bot : commands.Bot, test_guild : int):
    @bot.slash_command(guild_ids=[test_guild])
    async def suggest(
    interaction: Interaction,
    message: str = SlashOption(
        name="message_text",
        description="Choose the best dog from this autocompleted list!",
        required=True,
    )):
        # sends the autocompleted result
        
        await interaction.response.send_message(" submitted by %s \n %s" %(interaction.user.mention, message))

  