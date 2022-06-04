import asyncio
import os

import dotenv

from . import bot


async def main():
    dotenv.load_dotenv(override=True)

    async with bot.Wulkabot() as client:
        await client.start(os.environ["DISCORD_TOKEN"])


if __name__ == "__main__":
    asyncio.run(main())
