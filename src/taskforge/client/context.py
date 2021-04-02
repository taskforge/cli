from taskforge.client.base import ModelClient


class ContextClient(ModelClient):
    plural_name = "contexts"

    async def get_by_name(self, name):
        params = {"name": name}
        results = await self.list(params=params)
        # TODO: this is a work around because the contexts API doesn't support name
        # filtering yet.
        for result in results:
            if result["name"] == name:
                return result

        return None
