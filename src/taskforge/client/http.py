import logging

import aiohttp

logger = logging.getLogger(__name__)


class NoToken(Exception):
    """
    No token was set for this client
    """


class ClientException(Exception):
    """
    Generic client exception, usually the result of an HTTP failure.
    """


class Client:
    def __init__(self, base_url="", token=""):
        self.base_url = base_url
        self.token = token
        if not self.token:
            raise NoToken()

        self.session = aiohttp.ClientSession()
        self.session.get
        self.session.headers["Authorization"] = f"Bearer {self.token}"
        self.session.headers["Accept"] = "application/json"

    def url(self, endpoint: str) -> str:
        return f"{self.base_url}{endpoint}"

    async def handle_error(self, response, exc):
        if response.headers["content-type"] == "application/json":
            data = await response.json()
        else:
            data = await response.text()

        msg = "bad response from server ([{method}] {url}): {data}".format(
            method=response.method,
            url=response.url,
            data=data,
        )

        logger.error(msg)
        raise ClientException(msg) from exc

    async def request(self, method, url, **kwargs):
        try:
            response = await self.session.request(method, url, **kwargs)
            if not response.ok:
                await self.handle_error(response)
            return await response.json()
        except aiohttp.client_exceptions.ClientError as exc:
            msg = "unexpected response from server ([{method}] {url})".format(
                method=method,
                url=url,
            )
            logger.error(msg)
            raise ClientException(msg) from exc

    async def get(self, endpoint, **kwargs):
        return await self.request("GET", self.url(endpoint), **kwargs)

    async def delete(self, endpoint, **kwargs):
        return await self.request("DELETE", self.url(endpoint), **kwargs)

    async def put(self, endpoint, **kwargs):
        return await self.request("PUT", self.url(endpoint), **kwargs)

    async def post(self, endpoint, **kwargs):
        return await self.request("POST", self.url(endpoint), **kwargs)
