import logging

from discord import Client, Embed, Interaction
from discord.app_commands import CommandTree
from discord.app_commands.errors import AppCommandError, CheckFailure

from src.errors import (
    TransferException,
)


class FlangsbotCommandTree(CommandTree):
    __logger: logging.Logger

    def __init__(self, client: Client):
        super().__init__(client, fallback_to_global=True)

        self.__logger = logging.Logger(__name__)
        self.__logger.setLevel(logging.DEBUG)

    @staticmethod
    def __build_exception_embed(*, exception: Exception, description: str) -> Embed:
        embed = Embed(title="Reported exception", description=description)
        embed.add_field(name="Class", value=type(exception))
        embed.add_field(name="Exception", value=exception)

        return embed

    async def on_error(self, interaction: Interaction, error: AppCommandError) -> None:
        if isinstance(error, CheckFailure):
            return await interaction.followup.send(
                embed=self.__build_exception_embed(
                    exception=error,
                    description="❎ A check precondition failed because:",
                )
            )

        elif isinstance(error, TransferException):
            return await interaction.followup.send(
                embed=self.__build_exception_embed(
                    exception=error,
                    description="❎ The transfer process failed because:",
                )
            )

        elif isinstance(error, ValueError):
            return await interaction.followup.send(
                embed=self.__build_exception_embed(
                    exception=error,
                    description="❎ The argument does not satisfies the required value because:",
                )
            )

        elif isinstance(error, TypeError):
            return await interaction.followup.send(
                embed=self.__build_exception_embed(
                    exception=error,
                    description="❎ The argument does not satisfies the required type because:",
                )
            )

        elif isinstance(error, AppCommandError):
            self.__logger.warning("An unhandled exception was raised.", error)

            return await interaction.followup.send(
                embed=self.__build_exception_embed(
                    exception=error,
                    description="❎ An unhandled exception has occurred.",
                )
            )
