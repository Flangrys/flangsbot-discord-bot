import asyncio
import logging

import discord
from discord.ext import commands

from src.commands import help_command
from src.configuration import environs, loggers
from src.managers import extensions, sisinfo
from src.types import version


class Flangsbot(commands.Bot):

    __version__: version.ClientVersion

    __CLIENT_SECRET_KEY: str
    __CLIENT_DEBUG_MODE: bool

    __logger: logging.Logger

    __extensions_manager: extensions.ExtensionsManager
    __sisinfo_manager: sisinfo.SisinfoManager

    def __init__(self, *, version: version.ClientVersion) -> None:
        super().__init__(
            command_prefix="$fl",
            help_command=help_command.HelpCommand(),
            intents=discord.Intents.all(),
        )

        self.__version__ = version

        self.__logger = loggers.logger("discord")

        # Setting up environ variables.
        self.__CLIENT_SECRET_KEY = environs.get_environ("FLANGSBOT_SECRET_KEY")
        self.__CLIENT_DEBUG_MODE = environs.get_bool_environ("FLANGSBOT_DEBUG_MODE")

        self.__extensions_manager = extensions.ExtensionsManager(self)
        self.__sisinfo_manager = sisinfo.SisinfoManager(self)

    def get_loop(self) -> asyncio.AbstractEventLoop:
        return self.loop

    async def setup_hook(self) -> None:
        self.__logger.info("[setup] Setting up some things...")

        await self.__extensions_manager.load_all_extensions()
        await self.__sisinfo_manager.setup()

        extensions = self.__extensions_manager.get_enabled_extensions()

        if len(extensions) == 0:
            self.__logger.warn("[extensions_manager] no cogs were loaded.")

    async def launcher(self) -> None:
        self.__logger.info("[launcher] Launching...")

        async with self as bot:
            await bot.login(token=bot.__CLIENT_SECRET_KEY)
            await bot.connect(reconnect=True)

    async def on_ready(self) -> None:
        await self.tree.sync(guild=discord.Object(946064284209778801))

        self.__logger.info("[application_commands] Synced commands")
