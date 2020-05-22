"""
API Client code for the Taskforge backend
"""

import sys
from json import JSONDecodeError, dumps

import requests

from uuid import UUID
from pprint import pprint
from functools import wraps
from dataclasses import asdict

from task_forge.sdk.exceptions import Unauthorized, NotFound


class HTTPClient:
    """
    API Client for the Taskforge backend
    """

    cls = callable
    version = None
    object_name = None

    def __init__(
        self, server_hostname, session=None, access_token=None, refresh_token=None
    ):
        self.hostname = server_hostname
        self.refresh_token = refresh_token
        if session is not None:
            self.client = requests.Session()
        else:
            self.client = session

        self.client.headers.update({"Content-Type": "application/json"})
        if access_token is not None and refresh_token is not None:
            self.set_token(access_token, refresh_token)

    def set_token(self, access_token, refresh_token):
        self.client.headers.update({"Authorization": f"Bearer {access_token}"})
        self.refresh_token = refresh_token

    def full_url(self, endpoint):
        # Already expanded
        if self.hostname in endpoint:
            return endpoint
        return f"{self.hostname}{endpoint}"

    def request(self, method, endpoint, retry=True, **kwargs):
        try:
            resp = self.client.request(method, self.full_url(endpoint), **kwargs)
            resp.raise_for_status()
            return resp.json()
        except Exception as err:
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
            elif response.status_code == 401:
                raise Unauthorized("Not authorized or logged in")
            elif response.status_code == 404:
                raise NotFound()
            elif response.status_code == 400:
                raise BadRequest(message)
            else:
                raise Exception(message)

    def token_refresh(self):
        if not self.refresh_token:
            raise Unauthorized("Refresh token not set")

        data = self.request(
            "POST",
            "/api/token/refresh",
            json={"refresh": self.refresh_token},
            retry=False,
        )
        self.set_token(data["access"], self.refresh_token)

    def get(self, id: UUID):
        data = self.request("GET", f"/api/{self.version}/{self.object_name}/{id}")
        return self.cls(**data)

    def list(self):
        results = []
        url = f"/api/{self.version}/{self.object_name}"
        while True:
            data = self.request("GET", url)
            results.extend(data["results"])
            if data["next"]:
                url = data["next"]
            else:
                break
        return [self.cls(**result) for result in results]

    def create(self, instance):
        data = {
            key: value for key, value in asdict(instance).items() if value is not None
        }
        created = self.request(
            "POST", f"/api/{self.version}/{self.object_name}", json=data
        )
        return self.cls(**created)

    def update(self, instance):
        data = asdict(instance)
        updated = self.request(
            "PUT", f"/api/{self.version}/{self.object_name}/{instance.id}", json=data
        )
        return self.cls(**updated)

    def delete(self, instance):
        data = asdict(instance)
        self.request(
            "DELETE", f"/api/{self.version}/{self.object_name}/{instance.id}", json=data
        )
        return None
