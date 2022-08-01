import nextcord
from nextcord.ext import commands
from nextcord import ChannelType, Interaction, Role, SlashOption

import utils.suggestions as suggestions
import utils.json_utils as json_utils
import d_bot as bot


# suggestion bot commands
# suggest
# accept
# decline
# maybe/discussing/hold
# anon suggest
# suggest channel
# suggest log channel


def register_commands(bot : commands.Bot):

    @bot.message_command()
    async def accept(interaction: nextcord.Interaction, message: nextcord.Message):
        if await suggestions.mark(message.id, "", suggestions.Accept):
             await interaction.response.send_message(ephemeral=True, embed=suggestions.create_command_success_embed(f"suggestion status: Accept -- moved to {json_utils.get_suggestion_log_channel().mention}"))
        else:
             await interaction.response.send_message(ephemeral=True, embed=suggestions.create_command_error_embed(f"message selected was not a suggestion"))
  
  
    @bot.message_command()
    async def deny(interaction: nextcord.Interaction, message: nextcord.Message):
        if await suggestions.mark(message.id, "", suggestions.Deny):
             await interaction.response.send_message(ephemeral=True, embed=suggestions.create_command_success_embed(f"suggestion status: Deny -- moved to {json_utils.get_suggestion_log_channel().mention}"))
        else:
             await interaction.response.send_message(ephemeral=True, embed=suggestions.create_command_error_embed(f"message selected was not a suggestion"))

    @bot.message_command()
    async def waiting(interaction: nextcord.Interaction, message: nextcord.Message):
        if await suggestions.mark(message.id, "", suggestions.Wait):
             await interaction.response.send_message(ephemeral=True, embed=suggestions.create_command_success_embed("suggestion status: Held -- updated suggestion"))
        else:
             await interaction.response.send_message(ephemeral=True, embed=suggestions.create_command_error_embed(f"message selected was not a suggestion"))


    
    @bot.slash_command(default_member_permissions = 1)
    async def suggest(
    interaction: Interaction,
    message: str = SlashOption(
        name="message_text",
        description="suggestion to submit",
        required=True,
    )):
        # sends the autocompleted result
        
        if not json_utils.get_suggestion_channel():
            await interaction.response.send_message(ephemeral=True, embed=suggestions.create_command_error_embed(f"a suggestion channel has not been set"))
        else:
            await suggestions.create_suggestion(message, interaction.user)            
            await interaction.response.send_message(ephemeral=True, embed=suggestions.create_command_success_embed(f"created suggestion, see {json_utils.get_suggestion_channel().mention}"))

    @bot.slash_command(default_member_permissions = 8)
    async def suggestion_notif(
    interaction: Interaction,
    role: Role = SlashOption(
        name="role",
        description="Choose the role that should me @ whenever a suggestion is submitted",
        required=True,
        autocomplete=False
    )):
        x = await interaction.response.send_message(ephemeral=True, embed=suggestions.create_command_success_embed(f"set {role} as notification role"))
        json_utils.set_role(role)

    @bot.slash_command(default_member_permissions = 8)
    async def suggestion_channel(
    interaction: Interaction,
    channel: nextcord.abc.GuildChannel = SlashOption(
        name="channel",
        description="Choose the channel where submitted suggestions should go",
        required=True,
        autocomplete=False
    )):
        if channel.type == ChannelType.text:
            x = await interaction.response.send_message(ephemeral=True, embed=suggestions.create_command_success_embed(f"set {channel.mention} as suggestion channel"))
            json_utils.set_suggestion_channel(channel)
        else:
            await interaction.response.send_message(ephemeral=True, embed=suggestions.create_command_error_embed(f"suggestion channel needs to be a text channel, {channel.mention} is a {channel.type} channel"))


    @bot.slash_command(default_member_permissions = 8)
    async def suggestion_log_channel(
    interaction: Interaction,
    channel: nextcord.abc.GuildChannel = SlashOption(
        name="channel",
        description="Choose the channel where finished suggestion votes should go",
        required=True,
        autocomplete=False
    )):
        if channel.type == ChannelType.text:
            await interaction.response.send_message(ephemeral=True, embed=suggestions.create_command_success_embed(f"set {channel.mention} as suggestion log channel"))
            json_utils.set_suggestion_log_channel(channel)
        else:
            await interaction.response.send_message(ephemeral=True, embed=suggestions.create_command_error_embed(f"suggestion log channel needs to be a text channel, {channel.mention} is a {channel.type} channel"))


    l = [suggestions.Accept.name, suggestions.Wait.name, suggestions.Deny.name]
    @bot.slash_command(default_member_permissions = 8)
    async def mark(
    interaction: Interaction,
    status: str = SlashOption(
        name="status",
        description="Status to mark the suggestion as",
        required=True
    ),
    message_id: str = SlashOption(
        name="message_id",
        description="right click message and click copy message id",
        required=True
    ),
    reason: str = SlashOption(
        name="reason",
        description="reason for acceptance/rejection",
        required=False
    )):
        if status not in l:
            await interaction.response.send_message(ephemeral=True, embed=suggestions.create_command_error_embed(f"The status {status} is not a defined status, use {l}"))
            return
        x = 0
        try:
            x = int(message_id)
        except:
            await interaction.response.send_message(ephemeral=True, embed=suggestions.create_command_error_embed(f"message id is not an int: {message_id}"))
            return
        m : suggestions.SuggestionMark
        if status.lower() == suggestions.Accept.name.lower():
            m = suggestions.Accept
        elif status.lower() == suggestions.Wait.name.lower():
            m = suggestions.Wait
        elif status.lower() == suggestions.Deny.name.lower():
            m = suggestions.Deny

        if await suggestions.mark(x, reason, m):
            await interaction.response.send_message(ephemeral=True, embed=suggestions.create_command_success_embed(f"suggestion status: {m.name} -- moved to {json_utils.get_suggestion_log_channel().mention}"))
        else:
            await interaction.response.send_message(ephemeral=True, embed=suggestions.create_command_error_embed(f"Make sure suggestion log channel is setup and the message id is correct"))
    @mark.on_autocomplete("status")
    async def status_autocomplete(interaction: Interaction, status: str):
        if not status:
            # send the full autocomplete list
            await interaction.response.send_autocomplete(l)
            return
        await interaction.response.send_autocomplete([s for s in l if s.lower().startswith(status.lower())])

def get_bot():
    return bot.BOT
