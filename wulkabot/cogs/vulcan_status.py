import discord
from discord import app_commands
from discord.ext import commands

from .. import bot
from ..utils import constants, vulcan_status
from ..utils.vulcan_status import Result, Status


def status_embed(status: list[tuple[str, Status]]) -> discord.Embed:
    ok = []
    errors = []

    for domain, result in status:
        match result.state:
            case Result.OK:
                ok.append(domain)
                continue
            case Result.DATABASE_UPDATE:
                icon = "🔄"
            case Result.BREAK:
                icon = "⚠️"
            case Result.ERROR:
                icon = "‼️"
            case Result.TIMEOUT:
                icon = "⌛"
            case _:
                icon = "❓"

        errors.append(f"{icon} {domain}: {result.message or result.status_code}")

    if errors:
        error_text = "\n".join(errors)
    else:
        error_text = "🟢 Wszystko działa!"

    if ok:
        ok_text = ", ".join(ok)
    else:
        ok_text = "🔥 Nic nie działa"

    return (
        discord.Embed(title="Status dziennika", colour=constants.ACCENT_COLOR)
        .add_field(name="Błędy", value=error_text, inline=False)
        .add_field(name="Działające usługi", value=ok_text, inline=False)
    )


class VulcanStatus(commands.Cog):
    def __init__(self, bot: bot.Wulkabot) -> None:
        super().__init__()
        self.bot = bot

    @app_commands.command()
    async def status(self, interaction: discord.Interaction):
        """Sprawdza status dziennika"""
        await interaction.response.defer(thinking=True)

        status = await vulcan_status.check_all(self.bot.http_client)
        embed = status_embed(status)

        await interaction.followup.send(embed=embed)


async def setup(bot: bot.Wulkabot):
    await bot.add_cog(VulcanStatus(bot))
