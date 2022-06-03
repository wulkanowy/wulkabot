import discord


class DeleteButton(discord.ui.View):
    def __init__(self, invoker: discord.User | discord.Member) -> None:
        super().__init__(timeout=10)
        self.invoker = invoker
        self.message: discord.Message | None = None

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if (
            interaction.user == self.invoker
            or isinstance(interaction.user, discord.Member)
            and interaction.user.resolved_permissions.manage_messages
        ):
            return True

        await interaction.response.send_message(
            "Tylko osoba która wywołała bota może usunąć tę wiadomość", ephemeral=True
        )
        return False

    @discord.ui.button(label="Usuń", style=discord.ButtonStyle.danger)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        self.stop()
        await self.message.delete()

    async def on_timeout(self) -> None:
        await self.message.edit(view=None)
