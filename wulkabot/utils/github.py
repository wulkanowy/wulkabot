"""
Wulkabot
Copyright (C) 2022-present Stanisław Jelnicki
"""

from typing import Any

import aiohttp


class GitHub:
    def __init__(self, http_client: aiohttp.ClientSession) -> None:
        self._http = http_client

    async def fetch_repo(self, owner: str, repo: str) -> dict[str, Any] | None:
        response = await self._http.get(f"/repos/{owner}/{repo}")
        if response.ok:
            return await response.json()

    async def close(self):
        await self.close()
