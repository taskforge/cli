class ModelClient:
    plural_name = ""

    def __init__(self, client):
        self.client = client

    async def create(self, model, **kwargs):
        return await self.client.post(
            f"/api/v1/{self.plural_name}/{id}",
            json=model,
            **kwargs,
        )

    async def get(self, id, **kwargs):
        return await self.client.get(f"/api/v1/{self.plural_name}/{id}", **kwargs)

    async def list(self, limit=-1, **kwargs):
        page = await self.client.get(f"/api/v1/{self.plural_name}", **kwargs)
        results = page["results"]
        while page.get("next"):
            if limit > 0 and len(results) >= limit:
                break

            page = await self.client.get(page["next"], **kwargs)
            results.extend(page["results"])

        return results

    async def update(self, model, **kwargs):
        return await self.client.put(
            f"/api/v1/{self.plural_name}/{model['id']}",
            **kwargs,
        )

    async def delete(self, id, **kwargs):
        return await self.client.delete(f"/api/v1/{self.plural_name}/{id}", **kwargs)
