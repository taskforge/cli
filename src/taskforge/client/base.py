import logging


class ModelClient:
    plural_name = ""

    def __init__(self, client):
        self.client = client
        self.logger = logging.getLogger(self.__class__.__name__)

    async def create(self, model, **kwargs):
        self.logger.debug("creating %s with %s", self.plural_name, model)
        return await self.client.post(
            f"/api/v1/{self.plural_name}",
            json=model,
            **kwargs,
        )

    async def get(self, id, **kwargs):
        self.logger.debug("retrieving a %s with ID: %s", self.plural_name, id)
        return await self.client.get(f"/api/v1/{self.plural_name}/{id}", **kwargs)

    async def list(self, limit=-1, **kwargs):
        self.logger.debug("getting all %s", self.plural_name)
        page = await self.client.get(f"/api/v1/{self.plural_name}", **kwargs)
        results = page["results"]
        while page.get("next"):
            self.logger.debug("next page found, retrieving more %s", self.plural_name)
            if limit > 0 and len(results) >= limit:
                break

            page = await self.client.get(page["next"], **kwargs)
            results.extend(page["results"])

        return results

    async def update(self, model, **kwargs):
        self.logger.debug("updated %s with ID: %s", self.plural_name, model["id"])
        return await self.client.put(
            f"/api/v1/{self.plural_name}/{model['id']}",
            **kwargs,
        )

    async def delete(self, id, **kwargs):
        self.logger.debug("deleted %s with ID: %s", self.plural_name, id)
        return await self.client.delete(f"/api/v1/{self.plural_name}/{id}", **kwargs)
