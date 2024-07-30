import discord
from discord import app_commands
from discord.ext import commands

from src.client import Flangsbot


class Settings(commands.Cog):

    bot: "Flangsbot"

    managment_guild: discord.Object = discord.Object(946064284209778801)

    def __init__(self, bot: "Flangsbot") -> None:
        self.bot = bot

    @app_commands.command(
        name="hw", description="Respond with a 'hello world!' message"
    )
    @app_commands.guilds(managment_guild)
    async def hello_world(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_message("Hello World!")

    @staticmethod
    async def check_if_its_flangrys(interaction: discord.Interaction) -> bool:
        return interaction.user.id == 546542419399802884

    @app_commands.command(name="sync", description="Syncronize the bot settings.")
    @app_commands.guilds(managment_guild)
    @app_commands.check(check_if_its_flangrys)
    async def sync_settings(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_message("Syncing settings using defaults.")
        await self.bot.tree.sync()


async def setup(bot: "Flangsbot"):
    """Extension Entrypoint.

    Args:
        bot (Flangsbot): The bot.
    """

    await bot.add_cog(Settings(bot))
