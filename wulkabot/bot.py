import pkgutil
import types

import aiohttp
import discord
from discord.ext import commands

from . import cogs


class Wulkabot(commands.Bot):
    def __init__(self) -> None:
        super().__init__(
            command_prefix=commands.when_mentioned_or("!"),
            help_command=None,
            intents=discord.Intents(guilds=True, messages=True, message_content=True),
            allowed_mentions=discord.AllowedMentions.none(),
            max_ratelimit_timeout=10,
        )

    async def setup_hook(self) -> None:
        self.http_client = aiohttp.ClientSession()
        await self.load_extensions(cogs)
        await self.tree.sync()

    async def on_connect(self) -> None:
        print(f"Connected as {self.user}")

    async def on_command_error(
        self, context: commands.Context, exception: commands.errors.CommandError, /
    ) -> None:
        if isinstance(exception, commands.CommandNotFound):
            await context.send("Taka komenda nie istnieje. Być może chcesz użyć jej wersji z `/`")
        else:
            await context.send(str(exception))

    async def close(self) -> None:
        await super().close()
        await self.http_client.close()

    @staticmethod
    def find_extensions(module: types.ModuleType) -> set[str]:
        def unqualify(name: str) -> str:
            return name.rsplit(".", maxsplit=1)[-1]

        extensions = set()
        for package in pkgutil.walk_packages(module.__path__, f"{module.__name__}."):
            if package.ispkg or unqualify(package.name).startswith("_"):
                continue
            extensions.add(package.name)
        return extensions

    async def load_extensions(self, package: types.ModuleType) -> None:
        for extension in self.find_extensions(package):
            await self.load_extension(extension)
