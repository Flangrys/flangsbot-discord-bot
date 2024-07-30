from discord.ext import commands

from src.client import Flangsbot


class WeadasCommands(commands.Cog):

    bot: "Flangsbot"

    def __init__(self, bot: "Flangsbot"):
        self.bot = bot


async def setup(bot: "Flangsbot"):
    await bot.add_cog(WeadasCommands(bot))
