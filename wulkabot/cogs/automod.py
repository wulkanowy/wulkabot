import discord
from discord.ext import commands

from .. import bot
from ..utils.text_utils import remove_diacritics
from ..utils.views import DeleteButton

IOS_REQUEST_WORDS = ("kiedy", "bedzie", "wulkanowy", "wulkanowego", "pobrac", "ogarnac")

IOS_NOTICE = """
Witam chyba nigdy

Długa odpowiedź:
Niestety Wulkanowy na iOS może się nigdy nie pojawić. Wynika to z kilku przyczyn. \
Najważniejszą jest brak czasu — Wulkanowy to projekt tworzony po godzinach przez grupę uczniów \
(niektórzy z nas już pracują) i nie mamy czasu na napisanie praktycznie całej aplikacji od nowa. \
Nie mówimy oczywiście kategorycznego „nie”, ale nie możemy zapewnić, \
że uda nam się kiedykolwiek wydać Wulkanowego na iOS.
"""


def is_ios_request(text: str, /) -> bool:
    if len(text) > 100:
        # the text is longer and doesn't look like just a simple question
        return False

    words = set(remove_diacritics(text.replace("?", "").replace("!", "")).casefold().split())

    if "ios" not in words:
        return False

    return any(word in words for word in IOS_REQUEST_WORDS)


class Automod(commands.Cog):
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        if is_ios_request(message.content):
            view = DeleteButton(message.author)
            reply = await message.reply(IOS_NOTICE, view=view)
            view.message = reply


async def setup(bot: bot.Wulkabot):
    await bot.add_cog(Automod())
