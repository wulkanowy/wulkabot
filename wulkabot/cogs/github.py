"""
Wulkabot
Copyright (C) 2022-present Stanisław Jelnicki
"""

import re
from typing import Any

import aiohttp
import discord
from discord.ext import commands

from .. import bot
from ..utils import github

GITHUB_REPO = re.compile(r"(?:\s|^)(?P<owner>[\w-]+)/(?P<repo>[\w-]+)(?:\s|$)", re.ASCII)


def match_repo(text: str) -> tuple[str, str] | None:
    if match := GITHUB_REPO.search(text):
        return (match["owner"], match["repo"])


class GitHub(commands.Cog):
    def __init__(self, bot: bot.Wulkabot) -> None:
        super().__init__()
        self.bot = bot
        self.github = github.GitHub(aiohttp.ClientSession(base_url="https://api.github.com"))

    async def cog_load(self) -> None:
        result = await self.bot.http_client.get(
            "https://raw.githubusercontent.com/ozh/github-colors/master/colors.json"
        )
        self.github_colours: dict[str, dict[str, str | None]] = await result.json(content_type=None)

    async def cog_unload(self) -> None:
        await self.github.close()

    def github_repo_embed(self, repo: dict[str, Any]) -> discord.Embed:
        description = repo["description"]
        if homepage := repo["homepage"]:
            description += f"\n\n{homepage}"
        stargazers = repo["stargazers_count"]
        forks = repo["forks_count"]
        watchers = repo["subscribers_count"]
        footer = f"⭐ {stargazers} 🍴 {forks} 👀 {watchers}"

        return (
            discord.Embed(
                title=repo["full_name"],
                url=repo["html_url"],
                description=description,
                colour=self.get_github_color(repo["language"]),
            )
            .set_thumbnail(url=repo["owner"]["avatar_url"])
            .set_footer(text=footer)
        )

    def get_github_color(self, language: str | None) -> int | None:
        if language is None:
            return None
        colour = self.github_colours[language]["color"]
        if colour is None:
            return 0xF5AAB9
        return int(colour.removeprefix("#"), 16)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        if message.author.bot:
            return

        if match := match_repo(message.content):
            if repo := await self.github.fetch_repo(*match):
                await message.reply(embed=self.github_repo_embed(repo))


async def setup(bot: bot.Wulkabot):
    await bot.add_cog(GitHub(bot))
