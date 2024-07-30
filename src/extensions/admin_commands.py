import discord
from discord import ui
from discord.ext import commands

from src.client import Flangsbot


class ManageExtensionsModal(ui.Modal):

    extension_name = ui.TextInput(
        label="Extension Name", style=discord.TextStyle.paragraph
    )
    extension_condition = ui.Select(
        placeholder="Extension status",
        min_values=1,
        max_values=1,
        options=[
            discord.SelectOption(
                label="Enable", value="enable", description="Enable the extension"
            ),
            discord.SelectOption(
                label="Disable", value="disable", description="Disable the extension"
            ),
        ],
    )

    def __init__(self) -> None:
        super().__init__(
            title="manage_extensions_modal",
            timeout=60.0,
        )

        self.add_item(self.extension_name)
        self.add_item(self.extension_condition)

    async def on_submit(self, interaction: discord.Interaction) -> None: ...


class AdministratorCommands(commands.Cog):

    __bot: "Flangsbot"

    def __init__(self, bot: "Flangsbot") -> None:
        self.__bot = bot

    async def reload_extensions(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_message(view=ManageExtensionsModal())


async def setup(bot: "Flangsbot") -> None:
    await bot.add_cog(AdministratorCommands(bot))
