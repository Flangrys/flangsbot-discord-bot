import logging

import discord
from discord.ext import commands

from src.commands import help_command
from src.configuration import environs, loggers
from src.services import sisinfo, cogs
from src.utils import version


class Flangsbot(commands.Bot):

    __version: version.ClientVersion
    __logger: logging.Logger

    __CLIENT_SECRET_KEY = environs.get_environ("FLANGSBOT_SECRET_KEY")
    __CLIENT_DEBUG_MODE = environs.get_bool_environ("FLANGSBOT_DEBUG_MODE")

    __extensions_manager: cogs.CogsService
    __sisinfo_manager: sisinfo.SisinfoService

    def __init__(self, *, version: version.ClientVersion) -> None:
        super().__init__(
            command_prefix="flan!",
            description="",
            help_command=help_command.CustomHelpCommand(),
            intents=discord.Intents.all(),
        )

        self.__version = version

        self.__logger = loggers.logger("discord")

        # Setting up environ variables.

        self.__extensions_manager = extensions.CogsService(self)

    async def setup_hook(self) -> None:
        self.__logger.info("[setup] Setting up some things...")

        await self.__extensions_manager.load_all_extensions()
        await self.__sisinfo_manager.setup()

        extensions = self.__extensions_manager.get_enabled_extensions()

        if len(extensions) == 0:
            self.__logger.warning("[extensions_manager] no cogs were loaded.")

    async def launcher(self) -> None:
        self.__logger.info("[launcher] Launching...")

        async with self as bot:
            await bot.login(token=bot.__CLIENT_SECRET_KEY)
            await bot.connect(reconnect=True)

    async def on_ready(self) -> None:
        await self.tree.sync(guild=discord.Object(946064284209778801))

        self.__logger.info("[application_commands] Synced commands")
