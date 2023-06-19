from typing import Any, Literal

import aiohttp


class GitHub:
    def __init__(self) -> None:
        self._http = aiohttp.ClientSession(base_url="https://api.github.com")

    async def fetch_repo(self, owner: str, repo: str) -> dict[str, Any]:
        response = await self._http.get(f"/repos/{owner}/{repo}")
        response.raise_for_status()
        return await response.json()

    async def fetch_open_pulls(self, owner: str, repo: str):
        response = await self._http.get(
            f"/repos/{owner}/{repo}/pulls",
            params={"state": "open", "sort": "updated", "direction": "desc", "per_page": 25},
        )
        response.raise_for_status()
        return await response.json()

    async def fetch_issue(self, owner: str, repo: str, issue_number: int) -> dict[str, Any]:
        response = await self._http.get(f"/repos/{owner}/{repo}/issues/{issue_number}")
        response.raise_for_status()
        return await response.json()

    async def fetch_latest_release(self, owner: str, repo: str):
        response = await self._http.get(f"/repos/{owner}/{repo}/releases/latest")
        response.raise_for_status()
        return await response.json()

    async def close(self):
        await self._http.close()
