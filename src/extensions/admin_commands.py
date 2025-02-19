from discord import Interaction, app_commands, Object
from discord.abc import Snowflake
from discord.ext import commands

from src.client import Flangsbot


class AdministratorCommands(commands.Cog):

    guild_snowflake: Snowflake = Object(946064284209778801)
    guild_owner: Snowflake = Object(546542419399802884)

    def __init__(self, bot: "Flangsbot") -> None:
        self.bot = bot

    @app_commands.command(
        name="reload-extension",
        description="Reload a specific extension of this bot.",
    )
    @app_commands.guilds(guild_snowflake)
    @app_commands.guild_only
    async def reload_extension(self, interaction: Interaction):
        # 1. [X] Check permissions and roles.
        # 2. [ ] Ask the admin for what extension will reload.
        # 3. [ ] Retrieve the extension and reload it.
        ...


async def setup(bot: "Flangsbot") -> None:
    await bot.add_cog(AdministratorCommands(bot))
