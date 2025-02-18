import logging

from discord import Game, Intents, Status
from discord.ext import commands

from src.command_tree import FlangsbotCommandTree
from src.configuration import environs, loggers
from src.services import cogs, sisinfo
from src.utils import version


class Flangsbot(commands.Bot):

    __version: version.ClientVersion
    __logger: logging.Logger

    __CLIENT_SECRET_KEY = environs.get_environ("FLANGSBOT_SECRET_KEY")
    __CLIENT_DEBUG_MODE = environs.get_bool_environ("FLANGSBOT_DEBUG_MODE")
    __CLIENT_DEBUG_GUILD = environs.get_guild_environ("FLANGSBOT_DEBUG_GUILD")

    cogs_service: cogs.CogsService
    sisinfo_service: sisinfo.SisinfoService

    def __init__(self, *, version: version.ClientVersion) -> None:
        super().__init__(
            command_prefix=commands.when_mentioned_or("flan!"),
            intents=Intents.all(),
            tree_cls=FlangsbotCommandTree,
        )

        self.__version = version

        self.__logger = loggers.logger("discord")
        self.__logger.setLevel(logging.DEBUG)

        # Setting up environ variables.

        self.cogs_service = cogs.CogsService(self)
        self.sisinfo_service = sisinfo.SisinfoService()

    async def setup_hook(self) -> None:
        self.__logger.info("[setup] Setting up some things...")

        await self.cogs_service.setup()
        await self.sisinfo_service.setup()

    async def launcher(self) -> None:
        self.__logger.info("[launcher] Launching...")

        async with self:
            await self.login(token=self.__CLIENT_SECRET_KEY)
            await self.connect(reconnect=True)

    async def on_ready(self) -> None:
        await self.tree.sync(guild=self.__CLIENT_DEBUG_GUILD)
        await self.change_presence(
            activity=Game("/help o /haaa | Para obtener ayuda."),
            status=Status.online,
        )

        self.__logger.info("[application_commands] Synced commands")
