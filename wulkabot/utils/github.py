"""
Wulkabot
Copyright (C) 2022-present Stanisław Jelnicki
"""

from typing import Any

import aiohttp


class GitHub:
    def __init__(self) -> None:
        self._http = aiohttp.ClientSession(
            base_url="https://api.github.com", headers={"Accept": "application/vnd.github.v3+json"}
        )

    async def fetch_repo(self, owner: str, repo: str) -> dict[str, Any]:
        response = await self._http.get(f"/repos/{owner}/{repo}")
        response.raise_for_status()
        return await response.json()

    async def fetch_branches(self, owner: str, repo: str) -> list[str]:
        response = await self._http.get(f"/repos/{owner}/{repo}/branches")
        response.raise_for_status()
        branches = await response.json()
        return [branch["name"] for branch in branches]

    async def fetch_issue(self, owner: str, repo: str, issue_number: int) -> dict[str, Any]:
        response = await self._http.get(f"/repos/{owner}/{repo}/issues/{issue_number}")
        response.raise_for_status()
        return await response.json()

    async def close(self):
        await self._http.close()
