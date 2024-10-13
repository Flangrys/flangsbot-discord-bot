import datetime
import typing

from discord.ext import commands

from src.services import sisinfo
from src.types import manager_interface


class Notification(typing.TypedDict):
    date: datetime.date
    title: str
    description: str
    author: str


class Agenda(typing.TypedDict):
    date: datetime.date
    title: str
    description: str


class SisinfoManager(manager_interface.ManagerInterface):

    __service: sisinfo.SYSINFOService

    def __init__(self, bot: commands.Bot) -> None:
        super().__init__(bot)
        self.__service = sisinfo.SYSINFOService()

    async def setup(self) -> None:
        await self.__service.setup()

    def request_notifications(self) -> list[Notification]: ...

    def request_calendar(self) -> list[Agenda]: ...
