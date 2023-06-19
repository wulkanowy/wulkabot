import re
from typing import Any

import aiohttp
import discord
from discord.ext import commands

from .. import bot
from ..utils import github
from ..utils.constants import GITHUB_REPO
from ..utils.views import DeleteButton

Repo = tuple[str, str]


def parse_repo(text: str, *, default_owner: str | None = None) -> Repo | None:
    """
    Parses repository name and owner

    "wulkanowy/sdk" => ("wulkanowy", "sdk")
    "sdk" => None
    "sdk", default_owner="wulkanowy" => ("wulkanowy", "sdk")
    """
    repo = text.split("/")

    match len(repo):
        case 1:
            if default_owner is not None:
                owner, repo = default_owner, repo[0]
            else:
                return None
        case 2:
            owner, repo = repo
        case _:
            return None

    return (owner, repo)


def parse_issue(
    text: str, *, default_owner: str | None = None, default_repo: str | None = None
) -> tuple[Repo, int] | None:
    """
    Parses an issue or a pull request string
    """
    if "#" not in text:
        return None
    repo, issue_number = text.rsplit("#", 1)
    try:
        issue_number = int(issue_number)
    except ValueError:
        return None
    if issue_number <= 0:
        return None

    if repo:
        repo = parse_repo(repo, default_owner=default_owner)
        if repo is None:
            return None
    elif default_owner is None or default_repo is None:
        return None
    else:
        repo = (default_owner, default_repo)

    return (repo, issue_number)


def find_repo_in_channel_topic(topic: str) -> Repo | None:
    key = "https://github.com/"
    for word in topic.split():
        if word.startswith(key):
            return parse_repo(word[len(key) :])


class GitHub(commands.Cog):
    def __init__(self, bot: bot.Wulkabot) -> None:
        super().__init__()
        self.bot = bot
        self.github = github.GitHub()

    async def cog_load(self) -> None:
        result = await self.bot.http_client.get(
            "https://raw.githubusercontent.com/ozh/github-colors/master/colors.json"
        )
        self.github_colors: dict[str, dict[str, str | None]] = await result.json(content_type=None)

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
                color=self.get_github_color(repo["language"]),
            )
            .set_thumbnail(url=repo["owner"]["avatar_url"])
            .set_footer(text=footer)
        )

    def github_issue_embed(self, issue: dict[str, Any]) -> discord.Embed:
        is_pull_request = "pull_request" in issue
        title = f'{"Pull request" if is_pull_request else "Issue"} #{issue["number"]}\n{issue["title"][:128]}'
        body = issue["body"]
        if body is not None and len(body) > 256:
            body = None

        color = None
        if issue["state"] == "open":
            color = 0x2DA44E  # --color-open-emphasis
        elif issue["state"] == "closed":
            color = 0xCF222E  # --color-closed-emphasis
        if is_pull_request:
            pull_request = issue["pull_request"]
            if pull_request["merged_at"] is not None:
                color = 0x8250DF  # --color-done-emphasis
            elif issue["draft"]:
                color = 0x6E7781  # --color-neutral-emphasis

        user = issue["user"]
        comments = issue["comments"]
        footer = f"💬 {comments}"

        return (
            discord.Embed(title=title, url=issue["html_url"], description=body, color=color)
            .set_author(name=user["login"], url=user["html_url"], icon_url=user["avatar_url"])
            .set_footer(text=footer)
        )

    def get_github_color(self, language: str | None) -> int | None:
        if language is None:
            return None
        color = self.github_colors[language]["color"]
        if color is None:
            return 0xF5AAB9
        return int(color.removeprefix("#"), 16)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        if message.author.bot:
            return

        # `dict.fromkeys` allows us to deduplicate the list whilst preserving order
        words = dict.fromkeys(message.content.casefold().split()).keys()
        embeds = []

        try:
            topic = message.channel.topic  # type: ignore
        except AttributeError:
            channel_repo = GITHUB_REPO
        else:
            if topic is not None:
                channel_repo = find_repo_in_channel_topic(topic)
                if channel_repo is None:
                    channel_repo = GITHUB_REPO
            else:
                channel_repo = GITHUB_REPO

        for word in words:
            match = parse_issue(word, default_owner=channel_repo[0], default_repo=channel_repo[1])
            if match is not None:
                repo, issue_number = match
                repo = repo or GITHUB_REPO
                try:
                    issue = await self.github.fetch_issue(*repo, issue_number)
                except aiohttp.ClientResponseError:
                    continue
                embeds.append(self.github_issue_embed(issue))
            else:
                match = parse_repo(word)
                if match is not None:
                    try:
                        repo = await self.github.fetch_repo(*match)
                    except aiohttp.ClientResponseError:
                        continue
                    embeds.append(self.github_repo_embed(repo))

        if embeds:
            view = DeleteButton(message.author)
            reply = await message.reply(embeds=embeds[:3], view=view)
            view.message = reply


async def setup(bot: bot.Wulkabot):
    await bot.add_cog(GitHub(bot))
