"""API Client code for the Taskforge backend."""

from abc import ABC
from json import JSONDecodeError, dumps
from uuid import UUID
from dataclasses import asdict

import requests
from requests.exceptions import RequestException

from task_forge.sdk.exceptions import NotFound, BadRequest, Unauthorized


class HTTPClient(ABC):
    """
    An Abstract API Client for the Taskforge backend.

    This is meant to be subclassed per object to create an Object-oriented API client.
    """

    cls = callable
    version: str = "v0"
    object_name: str = "widgets"
    refresh_hook = None

    def __init__(
        self,
        server_hostname,
        session=None,
        access_token=None,
        refresh_token=None,
        credentials=None,
    ):
        self.hostname = server_hostname
        self.refresh_token = refresh_token
        if session is not None:
            self.client = requests.Session()
        else:
            self.client = session

        self.client.headers.update({"Content-Type": "application/json"})
        self.refresh_token = None
        self.credentials = credentials
        if access_token is not None and refresh_token is not None:
            self.set_token(access_token, refresh_token)

    def set_token(self, access_token: str, refresh_token: str):
        """Set the authentication headers for access and refresh tokens."""
        self.client.headers.update({"Authorization": f"Bearer {access_token}"})
        self.refresh_token = refresh_token

    def set_credentials(self, username, password):
        """
        Set the credentials for this client.

        These are only used if the refresh token is expired.
        """
        self.credentials = {
            "username": username,
            "password": password,
        }

    def full_url(self, endpoint: str):
        """Expand partial url endpoint to include the full protocol and hostname."""
        # Already expanded
        if self.hostname in endpoint:
            return endpoint
        return f"{self.hostname}{endpoint}"

    def request(self, method: str, endpoint: str, retry: bool = True, **kwargs):
        """
        Make a request to the Taskforge API.

        This handles error conversion and retry logic.
        """
        try:
            resp = self.client.request(method, self.full_url(endpoint), **kwargs)
            resp.raise_for_status()
            return resp.json()
        except RequestException as err:
            if getattr(err, "response", None) is None:
                raise err

            message = f"Unknown error: {resp.text}"
            try:
                obj = resp.json()
                if "detail" in obj:
                    print(obj["detail"])
                else:
                    obj = dumps(obj)
            except JSONDecodeError:
                pass

            response = err.response
            if response.status_code == 401 and retry:
                self.token_refresh()
                return self.request(method, endpoint, retry=False, **kwargs)
            else:
                self.convert_error(err, response, message)
                return None

    def convert_error(self, err, response, message):
        """Convert the response status code to an SDK error type."""
        if response.status_code == 401:
            raise Unauthorized("Not authorized or logged in")
        elif response.status_code == 404:
            raise NotFound()
        elif response.status_code == 400:
            raise BadRequest(message)
        else:
            raise Exception(message)

    def login(self, username, password):
        """Login and return the tokens."""
        self.client.headers.update({"Authorization": None})
        tokens = self.request(
            "POST",
            "/api/token",
            json={"username": username, "password": password},
            retry=False,
        )
        self.set_token(tokens["access"], tokens["refresh"])
        self.set_credentials(username, password)
        return tokens

    def token_refresh(self):
        """Reresh the access token."""
        if not self.refresh_token:
            raise Unauthorized("Refresh token not set")

        try:
            data = self.request(
                "POST",
                "/api/token/refresh",
                json={"refresh": self.refresh_token},
                retry=False,
            )
            self.set_token(data["access"], self.refresh_token)
        except Unauthorized as exc:
            if self.credentials:
                tokens = self.login(
                    self.credentials["username"], self.credentials["password"]
                )
                if self.refresh_hook is not None and callable(self.refresh_hook):
                    self.refresh_hook(
                        access=tokens["access"], refresh=tokens["refresh"]
                    )
            else:
                raise exc

    def get(self, id: UUID):
        """Get a single object by ID."""
        data = self.request("GET", f"/api/{self.version}/{self.object_name}/{id}")
        return self.cls(**data)

    def paginate(self, url, **kwargs):
        """Consume a paginated response from the API."""
        results = []
        while True:
            data = self.request("GET", url, **kwargs)
            results.extend(data["results"])
            if data["next"]:
                url = data["next"]
            else:
                break
        return results

    def list(self):
        """Return a list of objects."""
        results = self.paginate(f"/api/{self.version}/{self.object_name}")
        return [self.cls(**result) for result in results]

    def create(self, instance):
        """Send a create request for instance."""
        data = {
            key: value for key, value in asdict(instance).items() if value is not None
        }
        created = self.request(
            "POST", f"/api/{self.version}/{self.object_name}", json=data
        )
        return self.cls(**created)

    def update(self, instance):
        """Send an update request for instance."""
        data = asdict(instance)
        updated = self.request(
            "PUT", f"/api/{self.version}/{self.object_name}/{instance.id}", json=data
        )
        return self.cls(**updated)

    def delete(self, instance):
        """Delete instance in the backend."""
        data = asdict(instance)
        self.request(
            "DELETE", f"/api/{self.version}/{self.object_name}/{instance.id}", json=data
        )
        return None
