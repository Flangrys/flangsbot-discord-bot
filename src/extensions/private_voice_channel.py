import discord
from discord import CategoryChannel, Interaction, VoiceChannel, app_commands
from discord.ext import commands

from src.client import Flangsbot
from src.configuration import environs
from src.errors import NotAChannelException, NotAGuildException, TransferException
from src.views.channel_creation import ChannelCreationModal, ChannelPoliciesView


class PrivateVoiceChannel(commands.Cog):

    DEBUG_GUILD = environs.get_guild_environ("FLANGSBOT_DEBUG_GUILD")

    def __init__(self, bot: "Flangsbot"):
        self.bot = bot

    @app_commands.command(
        name="new_channel",
        description="Create a new voice channel.",
    )
    @app_commands.guilds(DEBUG_GUILD)
    @app_commands.guild_only
    async def create_voice_channel(self, interaction: Interaction):
        # 1. [X] Send a user a modal for customizing the channel name.
        # 2. [ ] Retrieve the category where the channel will be created.
        # 3. [ ] Create a channel with the specified user limit and policies.
        # 4. [ ] Ask the user if they want customize the allowed users or permissions.

        if not interaction.guild:
            raise NotAGuildException("Cannot run this command outside a guild.")

        if not isinstance(interaction.user, discord.Member):
            raise TransferException("Cannot transfer a non-member user to achannel.")

        if not interaction.user.voice:
            raise TransferException(
                "Cannot transfer a user which is not connected to a voice channel."
            )

        channel_creation_modal = ChannelCreationModal()
        channel_policies_view = ChannelPoliciesView()

        await interaction.response.send_modal(channel_creation_modal)
        await channel_creation_modal.wait()

        await interaction.followup.send(view=channel_policies_view)
        await channel_policies_view.wait()

        # TODO: Retrieves this data from the database
        guild_voice_command_channel = 1249868084077002804
        guild_voice_category: CategoryChannel
        guild_voice_channel: VoiceChannel

        if not (ch := interaction.guild.get_channel(guild_voice_command_channel)):
            raise NotAChannelException("Cannot find the root voice channel.")

        if not (category := ch.category):
            raise NotAChannelException("Cannot find the root voice category channel.")

        guild_voice_category = category

        guild_voice_channel = await interaction.guild.create_voice_channel(
            name=channel_creation_modal.channel_name.value,
            reason=f"flangsbot.command#new_channel@{interaction.user.name}",
            category=guild_voice_category,
            user_limit=10,
        )

        await interaction.user.move_to(
            channel=guild_voice_channel,
            reason="flansgbot.command.transfer#new_channel",
        )

        return None


async def setup(bot: "Flangsbot"):
    await bot.add_cog(PrivateVoiceChannel(bot))
