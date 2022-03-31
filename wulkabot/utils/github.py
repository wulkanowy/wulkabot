"""
Wulkabot
Copyright (C) 2022-present Stanisław Jelnicki
"""

from typing import Any

import aiohttp


class GitHub:
    def __init__(self) -> None:
        self._http = aiohttp.ClientSession(base_url="https://api.github.com")

    async def fetch_repo(self, owner: str, repo: str) -> dict[str, Any] | None:
        response = await self._http.get(f"/repos/{owner}/{repo}")
        if response.ok:
            return await response.json()

    async def close(self):
        await self._http.close()
