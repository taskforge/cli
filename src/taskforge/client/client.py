from taskforge.client.context import ContextClient
from taskforge.client.http import Client as HttpClient
from taskforge.client.source import SourceClient
from taskforge.client.tasks import TaskClient
from taskforge.client.user import UserClient


class Client:
    def __init__(self, base_url="", token=""):
        self.http = HttpClient(base_url=base_url, token=token)

    async def close(self):
        await self.http.session.close()

    @property
    def tasks(self) -> TaskClient:
        return TaskClient(self.http)

    @property
    def sources(self) -> SourceClient:
        return SourceClient(self.http)

    @property
    def contexts(self) -> ContextClient:
        return ContextClient(self.http)

    @property
    def users(self) -> UserClient:
        return UserClient(self.http)
