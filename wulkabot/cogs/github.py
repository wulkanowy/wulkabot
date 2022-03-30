"""
Wulkabot
Copyright (C) 2022-present Stanisław Jelnicki
"""

import re
from typing import Any

import aiohttp

# from discord import app_commands
import discord
from discord.ext import commands

from ..utils import github

GITHUB_REPO = re.compile(r"(?:\s|^)(?P<owner>[\w-]+)/(?P<repo>[\w-]+)(?:\s|$)", re.ASCII)


def match_repo(text: str) -> tuple[str, str] | None:
    if match := GITHUB_REPO.search(text):
        return (match["owner"], match["repo"])


def github_repo_embed(repo: dict[str, Any]) -> discord.Embed:
    description = repo["description"]
    if homepage := repo["homepage"]:
        description += f"\n\n{homepage}"
    stargazers = repo["stargazers_count"]
    forks = repo["forks_count"]
    watchers = repo["subscribers_count"]
    footer = f"⭐ {stargazers} 🍴 {forks} 👀 {watchers}"

    return (
        discord.Embed(title=repo["full_name"], url=repo["html_url"], description=description)
        .set_thumbnail(url=repo["owner"]["avatar_url"])
        .set_footer(text=footer)
    )


class GitHub(commands.Cog):
    def __init__(self) -> None:
        super().__init__()
        self.github = github.GitHub(aiohttp.ClientSession(base_url="https://api.github.com"))

    async def cog_unload(self) -> None:
        await self.github.close()

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        if message.author.bot:
            return

        if match := match_repo(message.content):
            if repo := await self.github.fetch_repo(*match):
                await message.reply(embed=github_repo_embed(repo))


async def setup(bot: commands.Bot):
    await bot.add_cog(GitHub())
