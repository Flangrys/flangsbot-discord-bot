import asyncio
import typing

from discord.ext import commands

from src.cache import storage
from src.services import abc


class AbstractManager:

    __bot: commands.Bot
    __service: abc.AbstractService | None
    __tasks: asyncio.TaskGroup
    __cache: storage.CacheStorage

    def __init__(
        self, client: commands.Bot, *, service: abc.AbstractService | None
    ) -> None:
        self.__bot = client
        self.__service = service

    async def setup(self) -> None:
        if self.__service == None:
            return

        await self.__service.setup()

    @property
    def cache(self) -> storage.CacheStorage: ...

    @property
    def task(self) -> asyncio.Task: ...

    @property
    def client(self) -> commands.Bot:
        return self.__bot
