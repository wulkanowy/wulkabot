"""
Wulkabot
Copyright (C) 2022-present Stanisław Jelnicki
"""

import pkgutil
import types

import aiohttp
import discord
from discord.ext import commands

from . import cogs


class Wulkabot(commands.Bot):
    def __init__(self) -> None:
        super().__init__(
            command_prefix=commands.when_mentioned_or("."),
            help_command=commands.MinimalHelpCommand(),
            intents=discord.Intents(guilds=True, messages=True, message_content=True),
            allowed_mentions=discord.AllowedMentions.none(),
        )

    async def setup_hook(self) -> None:
        await self.load_extensions(cogs)
        self.http_client = aiohttp.ClientSession()

    async def on_connect(self) -> None:
        print(f"Connected as {self.user}")

    async def close(self) -> None:
        await super().close()
        await self.http_client.close()

    @staticmethod
    def find_extensions(module: types.ModuleType) -> set[str]:
        def unqualify(name: str) -> str:
            return name.rsplit(".", maxsplit=1)[-1]

        extensions = set()
        for package in pkgutil.walk_packages(module.__path__, module.__name__ + "."):
            if package.ispkg or unqualify(package.name).startswith("_"):
                continue
            extensions.add(package.name)
        return extensions

    async def load_extensions(self, package: types.ModuleType) -> None:
        for extension in self.find_extensions(package):
            await self.load_extension(extension)

    async def reload_extensions(self) -> None:
        for extension in set(self.extensions):
            await self.reload_extension(extension)
