from taskforge.client.base import ModelClient


class SourceClient(ModelClient):
    plural_name = "sources"
    reverse_mapping_key = "name"

    async def reverse_lookup(self, value):
        context = await super().reverse_lookup(value)
        if context:
            return context

        return await self.get_by_name(value)

    async def get_by_name(self, name):
        async with self.cache_locks[name]:
            if name in self.cache:
                return self.cache[name]

            params = {"name": name}
            results = await self.list(params=params)
            # TODO: this is a work around because the sources API doesn't support name
            # filtering yet.
            for result in results:
                if result["name"] == name:
                    self.cache[name] = result
                    return result

            return None
