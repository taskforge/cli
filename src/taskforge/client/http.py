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

    def __init__(self, msg, status_code=-1):
        self.msg = msg
        self.status_code = status_code


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

    async def handle_error(self, response, data):
        if "detail" in data:
            msg = data["detail"]
        elif response.status == 400:
            msg = "\n".join(
                [
                    "Invalid data for field {field}: {problem}".format(
                        field=field,
                        problem=problem[0],
                    )
                    for field, problem in data.items()
                ]
            )
        else:
            msg = "[{status}] ({method}) {url}: {data}".format(
                status=response.status,
                method=response.method,
                url=response.url,
                data=data,
            )

        raise ClientException(msg, status_code=response.status)

    async def request(self, method, url, **kwargs):
        try:
            response = await self.session.request(method, url, **kwargs)
            data = await response.json()
            if not response.ok:
                await self.handle_error(response, data)
                return
            return data
        except aiohttp.client_exceptions.ClientError as exc:
            msg = "unexpected response from server ([{method}] {url}): {msg}".format(
                method=method,
                url=url,
                msg=str(exc),
            )
            logger.error(msg)
            raise ClientException(msg, status_code=500) from exc

    async def get(self, endpoint, **kwargs):
        return await self.request("GET", self.url(endpoint), **kwargs)

    async def delete(self, endpoint, **kwargs):
        return await self.request("DELETE", self.url(endpoint), **kwargs)

    async def put(self, endpoint, **kwargs):
        return await self.request("PUT", self.url(endpoint), **kwargs)

    async def post(self, endpoint, **kwargs):
        return await self.request("POST", self.url(endpoint), **kwargs)
