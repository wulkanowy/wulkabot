"""
Wulkabot
Copyright (C) 2022-present Stanisław Jelnicki
"""

import discord
from discord import app_commands
from discord.ext import commands

from .. import bot


class Development(commands.Cog):
    def __init__(self, bot: bot.Wulkabot) -> None:
        super().__init__()
        self.bot = bot

    @app_commands.command()
    async def sync(self, interaction: discord.Interaction, current_guild: bool = False):
        """Synchronizuje komendy bota"""
        # temporary check, needs refactoring
        if not await self.bot.is_owner(interaction.user):
            await interaction.response.send_message("nie", ephemeral=True)
            return

        if interaction.guild is None:
            current_guild = False
        elif current_guild:
            self.bot.tree.copy_global_to(guild=interaction.guild)

        commands = await self.bot.tree.sync(guild=interaction.guild if current_guild else None)
        commands_str = ", ".join(c.name for c in commands)
        destination = "guild" if current_guild else "global"
        await interaction.response.send_message(
            f"Synced **{len(commands)} {destination}** commands\n{commands_str}"
        )

    @app_commands.command()
    async def reload(self, interaction: discord.Interaction):
        """Przeładowuje komendy bota"""
        # temporary check, needs refactoring
        if not await self.bot.is_owner(interaction.user):
            await interaction.response.send_message("nie", ephemeral=True)
            return

        await self.bot.reload_extensions()
        await interaction.response.send_message("Reloaded successfuly")


async def setup(bot: bot.Wulkabot):
    await bot.add_cog(Development(bot))
