import discord


class DeleteButton(discord.ui.View):
    def __init__(self, timeout: float | None = 30):
        super().__init__(timeout=timeout)
        self.message: discord.Message | None = None

    @discord.ui.button(label="Usuń", style=discord.ButtonStyle.danger)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        message = interaction.message
        await message.edit(
            content=f"Wiadomość usunięta przez {interaction.user}", embeds=[], attachments=[], view=None, delete_after=5
        )
        self.stop()

    async def on_timeout(self) -> None:
        await self.message.edit(view=None)
        self.stop()
