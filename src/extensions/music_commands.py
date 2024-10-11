import discord
from discord.ext import commands

from src.client import Flangsbot


class Music(commands.Cog):

    bot: "Flangsbot"

    def __init__(self, bot: "Flangsbot") -> None:
        self.bot = bot

    async def search(self) -> None: ...

    async def play(self) -> None: ...

    async def pause(self) -> None: ...

    async def next(self) -> None: ...

    async def rewind(self) -> None: ...

    async def join(self) -> None: ...


async def setup(bot: "Flangsbot"):
    await bot.add_cog(Music(bot))
