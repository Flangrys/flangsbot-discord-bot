import datetime
import re
import typing

from discord.ext import commands

from src.managers import abc
from src.services import sisinfo


class Notification(typing.TypedDict):
    date: datetime.date
    title: str
    description: str
    author: str


class Agenda(typing.TypedDict):
    date: datetime.date
    title: str
    description: str


class SisinfoManager(abc.AbstractManager):

    __service: sisinfo.SYSINFOService

    def __init__(self, bot: commands.Bot) -> None:
        super().__init__(bot, service=sisinfo.SYSINFOService())

    def request_notifications(self) -> list[Notification]: ...

    def request_calendar(self) -> list[Agenda]: ...
