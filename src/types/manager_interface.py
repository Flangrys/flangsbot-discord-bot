import abc
import asyncio
import logging

from discord.ext import commands

from src.cache import storage
from src.types import service_interface


class ManagerInterface(abc.ABC):
    """
    This class represents a basic service manager.
    A service manager is understood as any pice of software that
    abstrac from the service an provides a simple api to consume
    the service.
    """

    __bot: commands.Bot
    __logger: logging.Logger
    __service: service_interface.ServiceInterface | None
    __tasks: asyncio.TaskGroup
    __cache: storage.CacheStorage

    def __init__(
        self,
        client: commands.Bot,
        *,
        service: service_interface.ServiceInterface | None
    ) -> None:
        self.__bot = client
        self.__service = service

    @abc.abstractmethod
    async def setup(self) -> None:
        """
        This method is used for initializate the
        service state, validate the internal service state, etc.
        """

    @property
    def cache(self) -> storage.CacheStorage:
        return self.__cache

    @property
    def task(self) -> asyncio.TaskGroup:
        return self.__tasks

    @property
    def client(self) -> commands.Bot:
        return self.__bot
