from operator import indexOf

import discord
from discord import CategoryChannel, Interaction, VoiceChannel, app_commands, Object, Embed, Color
from discord.abc import Snowflake
from discord.ext import commands

from src.client import Flangsbot
from src.configuration import environs
from src.errors import NotAChannelException, NotAGuildException, TransferException
from src.views.channel_creation import ChannelCreationModal, ChannelPoliciesView


class PrivateVoiceChannel(commands.Cog):
    DEBUG_GUILD = environs.get_guild_environ("FLANGSBOT_DEBUG_GUILD")

    guild_voice_command_channel: Snowflake = Object(1249868084077002804)
    guild_voice_category_channel: Snowflake = Object(946064285686194257)

    channel_pool: dict[Snowflake, Snowflake] = {}

    def __init__(self, bot: "Flangsbot"):
        self.bot = bot

    def register_channel(self, member: Snowflake, channel: Snowflake):
        self.channel_pool[channel] = member

    def remove_channel(self, channel: Snowflake):
        del self.channel_pool[channel]

    def get_channel_owner(self, owner: Snowflake) -> Snowflake | None:
        channels = list(self.channel_pool.keys())
        members = list(self.channel_pool.values())

        if not owner in members:
            return None

        return channels[members.index(owner)]

    @app_commands.command(
        name="new_channel",
        description="Create a new voice channel.",
    )
    @app_commands.guilds(DEBUG_GUILD)
    @app_commands.guild_only
    async def create_voice_channel(self, interaction: Interaction):
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

        voice_channel: VoiceChannel
        voice_category: CategoryChannel

        if not (voice_category := interaction.guild.get_channel(self.guild_voice_category_channel.id)):
            raise NotAChannelException("Cannot find the root voice category channel.")

        voice_channel = await interaction.guild.create_voice_channel(
            name=channel_creation_modal.channel_name.value,
            reason=f"flangsbot.command#new_channel@{interaction.user.name}",
            category=voice_category,
            user_limit=channel_policies_view.channel_user_limit.value,
        )

        await interaction.user.move_to(
            channel=voice_channel,
            reason="flansgbot.command.transfer#new_channel",
        )

        await voice_channel.send(
            embed=(
                Embed(
                    title="#️⃣ Channel Created",
                    description=f"This channel is owned by {interaction.user.mention} and was created with `/new_channel` command.",
                    color=Color.blurple()
                )
                .add_field(name="Invite your friends", value="Using the slash command `/invite` you can invite your friends to your private channel.")
                .add_field(name="Channel removal", value="This channel is automatically removed when the owner disconnects from it.")
                .add_field(name="This channel is private", value="This channel is only for you and your friends. No bots or other members are allowed to enter.")
            )
        )

        return None


async def setup(bot: "Flangsbot"):
    await bot.add_cog(PrivateVoiceChannel(bot))
