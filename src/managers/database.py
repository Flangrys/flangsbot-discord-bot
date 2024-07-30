from discord.ext import commands

from src.services import database


class DatabaseManager:

    __bot: commands.Bot
    __service: database.DatabaseService

    def __init__(self, bot: commands.Bot) -> None:
        self.__bot = bot

    def __setup_services(self) -> None: ...
