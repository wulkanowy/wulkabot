import json

import discord
from discord import app_commands
from discord.ext import commands

from .. import PATH


def load_questions() -> dict[str, str]:
    with open(PATH / "resources" / "faq.json") as faq:
        return json.load(faq)


class FAQ(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        super().__init__()
        self.bot = bot
        self.questions = load_questions()

    async def question_autocomplete(
        self, interaction: discord.Interaction, current: str
    ) -> list[app_commands.Choice[str]]:
        return [
            app_commands.Choice(name=question, value=question)
            for question in self.questions
            if current.casefold() in question.casefold()
        ]

    @app_commands.command()
    @app_commands.autocomplete(question=question_autocomplete)
    async def faq(self, interaction: discord.Interaction, question: str) -> None:
        """Często zadawane pytania"""
        if question in self.questions:
            await interaction.response.send_message(self.questions[question])
        else:
            await interaction.response.send_message("Nieznane pytanie")


async def setup(bot: commands.Bot):
    await bot.add_cog(FAQ(bot))
