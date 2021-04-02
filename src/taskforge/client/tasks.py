from taskforge.client.base import ModelClient


class TaskClient(ModelClient):
    plural_name = "tasks"

    async def next(self, context: str = ""):
        params = {"context": context} if context else None
        self.logger.debug("getting next Task in context: %s", context)
        return await self.client.get("/api/v1/tasks/next", params=params)

    async def search(self, query: str):
        params = {"q": query}
        self.logger.debug("searching for %s with query: %s", self.plural_name, query)
        return await self.list(params=params)

    async def complete(self, id: str):
        self.logger.debug("completing task: %s", id)
        return await self.client.put(f"/api/v1/tasks/{id}/complete")
