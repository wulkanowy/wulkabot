import asyncio

import discord
from discord import app_commands
from discord.ext import commands

from .. import bot
from ..utils import github, wulkanowy_manager
from ..utils.constants import ACCENT_COLOR, BUILDS_CHANNEL_ID, GITHUB_REPO
from ..utils.wulkanowy_manager import WulkanowyBuild, WulkanowyManagerException

OTHER_DOWNLOADS = " | ".join(
    (
        "[Google Play](https://play.google.com/store/apps/details?id=io.github.wulkanowy)",
        "[GitHub](https://github.com/wulkanowy/wulkanowy/releases)",
        "[F-Droid](https://f-droid.org/en/packages/io.github.wulkanowy)",
        "[AppGallery](https://appgallery.huawei.com/app/C101440411)",
        f"<#{BUILDS_CHANNEL_ID}>",
    )
)


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
        await interaction.response.defer(thinking=True)

        release = await self.github.fetch_latest_release(*GITHUB_REPO)
        download_urls = []
        for asset in release["assets"]:
            name = asset["name"]
            url = asset["browser_download_url"]
            download_urls.append(f"[{name}]({url})")
        download_urls = "\n".join(download_urls)

        pulls = await self.github.fetch_open_pulls(*GITHUB_REPO)
        branches = ["develop"]
        branches.extend((pull["head"]["ref"] for pull in pulls))
        builds: list[WulkanowyBuild | WulkanowyManagerException] = await asyncio.gather(
            *map(self.wulkanowy_manager.fetch_branch_build, branches), return_exceptions=True
        )
        lines = "\n".join(
            (
                f"`{build.build_number}` – [{branch}]({build.download_url})"
                for branch, build in zip(branches, builds, strict=True)
                if isinstance(build, WulkanowyBuild)
            )
        )

        text = "\n".join(
            (
                f'**Najnowsza wersja {release["name"]}**',
                download_urls,
                "",
                "**Wersje testowe**",
                lines,
                "",
                "**Inne źródła**",
                OTHER_DOWNLOADS,
            )
        )
        embed = discord.Embed(title="Pobierz Wulkanowego!", description=text, color=ACCENT_COLOR)
        await interaction.followup.send(embed=embed)


async def setup(bot: bot.Wulkabot):
    await bot.add_cog(Wulkanowy(bot))
