from taskforge.client.base import ModelClient


class ContextClient(ModelClient):
    plural_name = "contexts"

    async def get_by_name(self, name):
        params = {"name": name}
        results = await self.list(params=params)
        return results[0]
