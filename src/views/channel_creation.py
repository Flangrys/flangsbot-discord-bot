from typing import Self

from discord import Interaction, SelectOption, ui


class ChannelCreationModal(ui.Modal, title="Private Channel Creation"):
    channel_name = ui.TextInput[Self](
        label="Channel Name",
        placeholder="Type your channel name.",
        required=True,
        max_length=20,
    )

    async def on_submit(self, interaction: Interaction) -> None:
        return await interaction.response.send_message(
            f"✅ Creating channel [{self.channel_name}]", ephemeral=True
        )

    async def on_error(self, interaction: Interaction, error: Exception) -> None:
        return await interaction.response.send_message(
            "❎ An error ocurred during the process."
        )


class ChannelUserLimitSelector(ui.Select["ChannelPoliciesView"]):

    _options = [
        SelectOption(
            label="5 Users",
            value="max_five_users",
            description="Up to 5 users.",
            emoji="#️⃣",
        ),
        SelectOption(
            label="10 Users",
            value="max_ten_users",
            description="Up to 10 users.",
            emoji="#️⃣",
        ),
        SelectOption(
            label="20 Users",
            value="max_twenty_users",
            description="Up to 20 users.",
            emoji="#️⃣",
        ),
        SelectOption(
            label="50 Users",
            value="max_fifty_users",
            description="Up to 50 users.",
            emoji="#️⃣",
        ),
    ]

    def __init__(self) -> None:
        super().__init__(
            placeholder="Select a user limit...",
            options=self._options,
            min_values=1,
            max_values=1,
        )

    async def callback(self, interaction: Interaction):
        return await interaction.response.send_message(
            f"✅ Configuring the user limit."
        )


class ChannelPoliciesView(ui.View):

    channel_user_limit = ChannelUserLimitSelector()

    def __init__(self):
        super().__init__(timeout=40)

        self.add_item(self.channel_user_limit)
