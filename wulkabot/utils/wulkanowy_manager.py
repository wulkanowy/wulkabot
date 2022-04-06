"""
Wulkabot
Copyright (C) 2022-present Stanisław Jelnicki
"""

from typing import Any

import aiohttp

BASE_URL = "https://manager.wulkanowy.net.pl"
WULKANOWY_HASH = "daeff1893f3c8128"


class WulkanowyBuild:
    def __init__(self, data: dict[str, Any]) -> None:
        self.build_number: int = data["build_number"]
        self.build_slug: str = data["build_slug"]
        self.artifact_slug: str = data["artifact_slug"]

    @property
    def download_url(self) -> str:
        return f"{BASE_URL}/v1/download/app/{WULKANOWY_HASH}/build/{self.build_slug}/artifact/{self.artifact_slug}"

    def __str__(self) -> str:
        return self.download_url


class WulkanowyManagerException(Exception):
    pass


class WulkanowyManager:
    def __init__(self) -> None:
        self._http = aiohttp.ClientSession(base_url=BASE_URL)

    async def fetch_branch_build(self, branch: str) -> WulkanowyBuild:
        response = await self._http.get(f"/v1/build/app/{WULKANOWY_HASH}/branch/{branch}")
        response.raise_for_status()
        json = await response.json()
        if not json["success"]:
            raise WulkanowyManagerException(json["error"])
        return WulkanowyBuild(json["data"])

    async def close(self):
        await self._http.close()
