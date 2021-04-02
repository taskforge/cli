import logging

from taskforge.client.base import ModelClient

logger = logging.getLogger(__name__)


class ContextClient(ModelClient):
    plural_name = "contexts"
    reverse_mapping_key = "name"

    async def reverse_lookup(self, value):
        logger.debug("doing context reverse_lookup for %s", value)
        context = await super().reverse_lookup(value)
        if context:
            logger.debug("%s was in the lookup table", value)
            return context

        logger.debug("doing reverse lookup for context %s from API", value)
        return await self.get_by_name(value)

    async def get_by_name(self, name):
        async with self.cache_locks[name]:
            if name in self.cache:
                return self.cache[name]

            params = {"name": name}
            results = await self.list(params=params)
            # TODO: this is a work around because the contexts API doesn't support name
            # filtering yet.
            for result in results:
                if result["name"] == name:
                    self.cache[name] = result
                    return result

            return None
