import os

import aiohttp


class NoToken(Exception):
    """
    No token was set for this client
    """


class Client:
    def __init__(self, base_url="", token=""):
        self.base_url = base_url
        self.token = token
        if not self.token:
            raise NoToken()

        self.session = aiohttp.ClientSession()
        self.session.headers["Authorization"] = f"Bearer {self.token}"
        self.session.headers["Accept"] = "application/json"

    def url(self, endpoint: str) -> str:
        return f"{self.base_url}{endpoint}"

    async def get(self, endpoint, **kwargs):
        response = await self.session.get(self.url(endpoint), **kwargs)
        response.raise_for_status()
        return await response.json()

    async def delete(self, endpoint, **kwargs):
        response = await self.session.put(self.url(endpoint), **kwargs)
        response.raise_for_status()
        return await response.json()

    async def put(self, endpoint, **kwargs):
        response = await self.session.put(self.url(endpoint), **kwargs)
        response.raise_for_status()
        return await response.json()

    async def post(self, endpoint, **kwargs):
        response = await self.session.put(self.url(endpoint), **kwargs)
        response.raise_for_status()
        return await response.json()
