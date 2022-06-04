import asyncio

import discord
from discord import app_commands
from discord.ext import commands

from .. import bot
from ..utils import github, wulkanowy_manager
from ..utils.wulkanowy_manager import WulkanowyBuild, WulkanowyManagerException


class Wulkanowy(commands.Cog):
    def __init__(self, bot: bot.Wulkabot) -> None:
        super().__init__()
        self.bot = bot
        self.github = github.GitHub()
        self.wulkanowy_manager = wulkanowy_manager.WulkanowyManager()

    async def cog_unload(self) -> None:
        await self.github.close()
        await self.wulkanowy_manager.close()

    @app_commands.command()
    async def pobierz(self, interaction: discord.Interaction):
        branches = await self.github.fetch_branches("wulkanowy", "wulkanowy")
        builds: list[WulkanowyBuild | WulkanowyManagerException] = await asyncio.gather(
            *(map(self.wulkanowy_manager.fetch_branch_build, branches)), return_exceptions=True
        )
        text = []
        for branch, build in zip(branches, builds, strict=True):
            if isinstance(build, WulkanowyBuild):
                text.append(f"{branch}: [pobierz]({build.download_url})")
            else:
                text.append(f"{branch}: brak")
        embed = discord.Embed(
            title="Pobierz najnowsze wersje testowe!", description="\n".join(text)
        )
        await interaction.response.send_message(embed=embed)


async def setup(bot: bot.Wulkabot):
    await bot.add_cog(Wulkanowy(bot))
