import requests

from task_forge.sdk.client.base import HTTPClient
from task_forge.sdk.types import Task, Comment, Source, Context, Profile, User


class V1TaskClient(HTTPClient):
    cls = Task
    version = "v1"
    object_name = "tasks"


class V1ContextClient(HTTPClient):
    cls = Context
    version = "v1"
    object_name = "contexts"


class V1SourceClient(HTTPClient):
    cls = Source
    version = "v1"
    object_name = "sources"


class V1CommentClient(HTTPClient):
    cls = Comment
    version = "v1"
    object_name = "comments"


class V1UserClient(HTTPClient):
    cls = User
    version = "v1"
    object_name = "users"

    def create(self, *args, **kwargs):
        self.client.headers.update({"Authorization": None})
        return super().create(*args, **kwargs)

    def login(self, username, password):
        """
        Login and return the tokens
        """
        return self.request(
            "POST",
            "/api/token",
            json={"username": username, "password": password},
            retry=False,
        )


class API:
    def __init__(
        self, server_hostname, *args, **kwargs,
    ):
        if "session" not in kwargs or not kwargs["session"]:
            kwargs["session"] = requests.Session()

        self.users = V1UserClient(server_hostname, *args, **kwargs)
        self.tasks = V1TaskClient(server_hostname, *args, **kwargs)
        self.comments = V1CommentClient(server_hostname, *args, **kwargs)
        self.sources = V1SourceClient(server_hostname, *args, **kwargs)
        self.contexts = V1ContextClient(server_hostname, *args, **kwargs)

    def set_token(self, access, refresh):
        self.users.set_token(access, refresh)
        self.tasks.set_token(access, refresh)
        self.comments.set_token(access, refresh)
        self.sources.set_token(access, refresh)
        self.contexts.set_token(access, refresh)
        return self

    def login(self, username, password):
        tokens = self.users.login(username, password)
        self.set_token(tokens["access"], tokens["refresh"])
        return tokens
