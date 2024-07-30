from discord.ext import commands
from discord.ext.commands import context

from src.client import Flangsbot


class AutoRole(commands.Cog):

    bot: "Flangsbot"

    def __init__(self, bot: "Flangsbot") -> None:
        self.bot = bot

    @commands.Cog.listener("on_join")
    async def new_user_join(self) -> None:
        pass


async def setup(bot: "Flangsbot"):
    """Extension Entrypoint.

    Args:
        bot (Flangsbot): The bot.
    """

    await bot.add_cog(AutoRole(bot))
