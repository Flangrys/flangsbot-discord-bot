import logging
from typing import Any, Coroutine

from discord.client import Client
from discord.ext.commands.bot import BotBase

from commands import help_command
from configuration import environs
from src.managers.extensions import ExtensionsManager


class Flangsbot(BotBase, Client):

    CLIENT_SECRET_KEY: str
    CLIENT_DEBUG_MODE: bool

    __logger: logging.Logger
    extensions_manager: ExtensionsManager

    def __init__(self, **options):
        self.__logger = logging.Logger(__name__, logging.INFO)

        self.extensions_manager = ExtensionsManager(self)

        self.CLIENT_SECRET_KEY = environs.get_environs("FLANGSBOT_SECRET_KEY")
        self.CLIENT_DEBUG_MODE = environs.get_bool_environs("FLANGSBOT_DEBUG_MODE")

        self.command_prefix = "fl$"
        self.help_command = help_command.HelpCommand()

    def start(self, *args, **kwargs):
        raise NotImplementedError("this method is currently unavailable")

    async def setup_hook(self) -> Coroutine[Any, Any, None]:
        await self.extensions_manager.load_all_extensions()
        return super().setup_hook()
