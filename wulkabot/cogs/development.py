from discord.ext import commands

from .. import bot


class Development(commands.Cog):
    def __init__(self, bot: bot.Wulkabot) -> None:
        super().__init__()
        self.bot = bot

    @commands.command()
    @commands.has_role("Maintainer")
    async def sync(self, ctx: commands.Context):
        """Synchronizuje komendy bota"""

        commands = await self.bot.tree.sync()
        commands_str = ", ".join(c.name for c in commands)
        await ctx.reply(f"Zsynchronizowano **{len(commands)}** komend\n{commands_str}")


async def setup(bot: bot.Wulkabot):
    await bot.add_cog(Development(bot))
