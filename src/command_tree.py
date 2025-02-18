import logging

from discord import Client, Embed, Interaction
from discord.app_commands import CommandTree
from discord.app_commands.errors import AppCommandError

from src.errors import (
    NotAChannelException,
    NotAGuildException,
    NotAMemberException,
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
        embed = Embed(title="Reported exception.", description=description)
        embed.add_field(inline=True, name="Class", value=type(exception))
        embed.add_field(inline=True, name="Exception ", value=exception)
        embed.add_field(inline=True, name="Traceback", value=exception.__traceback__)

        return embed

    async def on_error(self, interaction: Interaction, error: AppCommandError) -> None:
        match error:
            case NotAChannelException():
                await interaction.response.send_message(
                    embed=self.__build_exception_embed(
                        exception=error,
                        description="❎ A channel-related check failed:",
                    )
                )

            case NotAGuildException():
                await interaction.response.send_message(
                    embed=self.__build_exception_embed(
                        exception=error,
                        description="❎ A guild-related check failed:",
                    )
                )

            case NotAMemberException():
                await interaction.response.send_message(
                    embed=self.__build_exception_embed(
                        exception=error,
                        description="❎ A member-related check failed:",
                    )
                )

            case TransferException():
                await interaction.response.send_message(
                    embed=self.__build_exception_embed(
                        exception=error,
                        description="❎ A voice channel transfer-related check failed:",
                    )
                )

            case err:
                await interaction.response.send_message(
                    embed=self.__build_exception_embed(
                        exception=err,
                        description="❎ An unhandled exception just raised :)",
                    )
                )
                self.__logger.warning("An unhandled exception was raised.", err)
