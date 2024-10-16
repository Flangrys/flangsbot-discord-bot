import discord
from discord import app_commands
from discord.ext import commands

from src.client import Flangsbot


class Settings(commands.Cog):

    bot: "Flangsbot"

    def __init__(self, bot: "Flangsbot") -> None:
        self.bot = bot

    @app_commands.command(
        name="hw", description="Respond with a 'hello world!' message"
    )
    @app_commands.guilds()
    async def hello_world(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_message("Hello World!")


async def setup(bot: "Flangsbot"):
    """Extension Entrypoint.

    Args:
        bot (Flangsbot): The bot.
    """

    await bot.add_cog(Settings(bot))
