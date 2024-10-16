from typing import Any, Callable, Coroutine, List, Mapping

from discord.ext.commands import Bot, HelpCommand
from discord.ext.commands.cog import Cog
from discord.ext.commands.context import Context
from discord.ext.commands.core import Command
from discord.ext.commands.errors import CommandError


class CustomHelpCommand(HelpCommand):

    def __init__(self, **options: Any) -> None:
        super().__init__(**options)

    async def send_bot_help(self, mapping: Mapping[Cog | None, List[Command[Any, Callable[..., Any], Any]]]) -> None:  # type: ignore
        return await super().send_bot_help(mapping)

    async def on_help_command_error(
        self, ctx: Context[Bot], error: CommandError
    ) -> Coroutine[Any, Any, None]:

        return super().on_help_command_error(ctx, error)
