from taskforge.client.base import ModelClient


class TaskClient(ModelClient):
    plural_name = "tasks"

    def __init__(self, client):
        self.client = client

    def next(self, context: str = ""):
        params = {"context": context} if context else None
        return self.client.get("/api/v1/tasks/next", params=params)

    def search(self, query: str):
        params = {"q": query}
        return self.list(params=params)
