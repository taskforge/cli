"""
API Client code for the Taskforge backend
"""

import sys
from json import JSONDecodeError

import requests

from uuid import UUID
from pprint import pprint
from functools import wraps
from dataclasses import asdict


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
            if (
                getattr(err, "response", None) is not None
                and err.response.status_code == 401
                and retry
            ):
                self.token_refresh()
                return self.request(method, endpoint, retry=False, **kwargs)
            try:
                json = resp.json()
                if "detail" in json:
                    print(json["detail"])
                else:
                    pprint(json)
            except JSONDecodeError:
                print("Unknown error:", resp.text)

            sys.exit(1)

    def token_refresh(self):
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
