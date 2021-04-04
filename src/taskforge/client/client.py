from taskforge.client.context import ContextClient
from taskforge.client.filter import FilterClient
from taskforge.client.http import Client as HttpClient
from taskforge.client.source import SourceClient
from taskforge.client.tasks import TaskClient
from taskforge.client.user import UserClient


class Client:
    def __init__(self, base_url="", token=""):
        self.http = HttpClient(base_url=base_url, token=token)
        self.tasks = TaskClient(self.http)
        self.sources = SourceClient(self.http)
        self.contexts = ContextClient(self.http)
        self.users = UserClient(self.http)
        self.filters = FilterClient(self.http)

    def close(self):
        self.http.session.close()
