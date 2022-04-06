"""
Wulkabot
Copyright (C) 2022-present Stanisław Jelnicki
"""

import aiohttp


class GitHub:
    def __init__(self) -> None:
        self._http = aiohttp.ClientSession(base_url="https://api.github.com")

    async def fetch_repo(self, owner: str, repo: str) -> dict[str, str | int | None]:
        response = await self._http.get(f"/repos/{owner}/{repo}")
        response.raise_for_status()
        return await response.json()

    async def fetch_branches(self, owner: str, repo: str) -> list[str]:
        response = await self._http.get(f"/repos/{owner}/{repo}/branches")
        response.raise_for_status()
        branches = await response.json()
        return [branch["name"] for branch in branches]

    async def close(self):
        await self._http.close()
