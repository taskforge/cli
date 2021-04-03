from taskforge.client.base import ModelClient


class FilterClient(ModelClient):
    plural_name = "filters"
    reverse_mapping_key = "name"

    async def get_by_name(self, name):
        params = {"name": name}
        results = await self.list(params=params)
        if results:
            return results[0]

        return None
