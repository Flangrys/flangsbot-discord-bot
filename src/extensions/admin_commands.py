from discord.ext import commands

from src.client import Flangsbot


class AdministratorCommands(commands.Cog):

    __bot: "Flangsbot"

    def __init__(self, bot: "Flangsbot") -> None:
        self.__bot = bot

async def setup(bot: "Flangsbot") -> None:
    await bot.add_cog(AdministratorCommands(bot))
