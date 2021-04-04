import logging
from json.decoder import JSONDecodeError

import requests

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

        self.session = requests.Session()
        self.session.get
        self.session.headers["Authorization"] = f"Bearer {self.token}"
        self.session.headers["Accept"] = "application/json"

    def url(self, endpoint: str) -> str:
        return f"{self.base_url}{endpoint}"

    def handle_error(self, response):
        try:
            data = response.json()
        except JSONDecodeError:
            data = response.text()

        if "detail" in data:
            msg = data["detail"]
        elif response.status_code == 400:
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
                status=response.status_code,
                method=response.method,
                url=response.url,
                data=data,
            )

        raise ClientException(msg, status_code=response.status_code)

    def request(self, method, url, **kwargs):
        response = self.session.request(method, url, **kwargs)
        if not response.ok:
            self.handle_error(response)

        if method != "DELETE":
            return response.json()

        return None

    def get(self, endpoint, **kwargs):
        return self.request("GET", self.url(endpoint), **kwargs)

    def delete(self, endpoint, **kwargs):
        return self.request("DELETE", self.url(endpoint), **kwargs)

    def put(self, endpoint, **kwargs):
        return self.request("PUT", self.url(endpoint), **kwargs)

    def post(self, endpoint, **kwargs):
        return self.request("POST", self.url(endpoint), **kwargs)
