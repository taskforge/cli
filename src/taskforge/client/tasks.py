from taskforge.client.base import ModelClient


class TaskClient(ModelClient):
    plural_name = "tasks"

    def next(self, context: str = ""):
        params = {"context": context} if context else None
        self.logger.debug("getting next Task in context: %s", context)
        return self.client.get("/api/v1/tasks/next", params=params)

    def search(self, query: str):
        params = {"q": query}
        self.logger.debug("searching for %s with query: %s", self.plural_name, query)
        return self.list(params=params)

    def complete(self, id: str):
        self.logger.debug("completing task: %s", id)
        return self.client.put(f"/api/v1/tasks/{id}/complete")
