"""API clients for the v1 API."""

from typing import List

import requests

from task_forge.sdk.types import Task, User, Source, Comment, Context
from task_forge.sdk.client.base import HTTPClient


class TaskClient(HTTPClient):
    """Backend client for interacting with Task objects."""

    cls = Task
    version = "v1"
    object_name = "tasks"

    def complete_by_id(self, id) -> None:
        """Complete the task with ID id."""
        self.request("PUT", f"/api/v1/tasks/{id}/complete")

    def current(self) -> Task:
        """Return the current Task for the current user."""
        data = self.request("GET", "/api/v1/tasks/current")
        return self.cls(**data)

    def search(self, query) -> List[Task]:
        """Run the query against the backend, return matching Tasks."""
        data = self.paginate("/api/v1/tasks/query", json={"query": query})
        return [self.cls(**d) for d in data]


class ContextClient(HTTPClient):
    """Backend client for interacting with Context objects."""

    cls = Context
    version = "v1"
    object_name = "contexts"

    def get_by_name(self, name: str) -> Context:
        """Retrieve a Context object by it's name."""
        data = self.request("GET", f"/api/v1/contexts/by-name/{name}")
        return self.cls(**data)


class SourceClient(HTTPClient):
    """Backend client for interacting with Source objects."""

    cls = Source
    version = "v1"
    object_name = "sources"


class CommentClient(HTTPClient):
    """Backend client for interacting with Comment objects."""

    cls = Comment
    version = "v1"
    object_name = "comments"


class UserClient(HTTPClient):
    """Backend client for interacting with User objects."""

    cls = User
    version = "v1"
    object_name = "users"

    def create(self, *args, **kwargs):
        """
        Remove Authorization headers before calling create.

        When creating a user sending a token can cause unexpected errors and is not how that API is
        expecting to be called.
        """
        self.client.headers.update({"Authorization": None})
        return super().create(*args, **kwargs)


class API:
    """Backend client for interacting with the v1 API."""

    refresh_hook = None

    def __init__(
        self, server_hostname, *args, **kwargs,
    ):
        if "session" not in kwargs or not kwargs["session"]:
            kwargs["session"] = requests.Session()

        clients = [
            ("users", UserClient),
            ("tasks", TaskClient),
            ("comments", CommentClient),
            ("sources", SourceClient),
            ("contexts", ContextClient),
        ]

        for attr, client in clients:
            obj = client(server_hostname, *args, **kwargs)
            obj.refresh_hook = self.proxy_refresh_hook
            setattr(self, attr, obj)

    def set_token(self, access, refresh):
        """Authenticate this client and sub-clients."""
        self.users.set_token(access, refresh)
        self.tasks.set_token(access, refresh)
        self.comments.set_token(access, refresh)
        self.sources.set_token(access, refresh)
        self.contexts.set_token(access, refresh)
        return self

    def set_credentials(self, username, password):
        """Authenticate this client and sub-clients."""
        self.users.set_credentials(username, password)
        self.tasks.set_credentials(username, password)
        self.comments.set_credentials(username, password)
        self.sources.set_credentials(username, password)
        self.contexts.set_credentials(username, password)
        return self

    def login(self, username, password):
        """Attempt to login with the given username and password."""
        tokens = self.users.login(username, password)
        self.set_credentials(username, password)
        self.set_token(tokens["access"], tokens["refresh"])
        return tokens

    def proxy_refresh_hook(self, access, refresh):
        """If any refresh hook is triggered propagate it."""
        if self.refresh_hook is not None and callable(self.refresh_hook):
            self.refresh_hook(access, refresh)
        self.set_token(access, refresh)
