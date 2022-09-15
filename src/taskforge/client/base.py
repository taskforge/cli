import logging
from functools import cache


class NameRetrivalMixin:
    def reverse_lookup(self, value):
        self.logger.debug("doing context reverse_lookup for %s", value)
        model = super().reverse_lookup(value)
        if model:
            self.logger.debug("%s was in the lookup table", value)
            return model

        self.logger.debug(
            "doing reverse lookup for %s %s from API", self.plural_name, value
        )
        return self.get_by_name(value)

    @cache
    def get_by_name(self, name):
        params = {"name": name}
        results = self.list(params=params)
        if results:
            return results[0]

        return None


class ModelClient:
    plural_name = ""
    reverse_mapping_key = ""

    def __init__(self, client):
        self.client = client
        self.logger = logging.getLogger(self.__class__.__name__)
        self.reverse_map = dict()

    def reverse_lookup(self, value):
        return self.reverse_map.get(value, None)

    def create(self, model, **kwargs):
        self.logger.debug("creating %s with %s", self.plural_name, model)
        return self.client.post(
            f"/v1/{self.plural_name}",
            json=model,
            **kwargs,
        )

    @cache
    def get(self, id, **kwargs):
        self.logger.debug("retrieving a %s with ID: %s", self.plural_name, id)
        response = self.client.get(f"/v1/{self.plural_name}/{id}", **kwargs)
        if self.reverse_mapping_key:
            reverse_key = response[self.reverse_mapping_key]
            self.reverse_map[reverse_key] = response

        return response

    def list(self, limit=-1, **kwargs):
        self.logger.debug("getting all %s", self.plural_name)
        endpoint = f"/v1/{self.plural_name}"
        page = self.client.get(endpoint, **kwargs)
        results = page["results"]
        page_number = 1
        while page.get("next"):
            self.logger.debug("next page found, retrieving more %s", self.plural_name)
            if limit > 0 and len(results) >= limit:
                break

            page_number += 1
            if "params" in kwargs:
                kwargs["params"]["page"] = page_number
            else:
                kwargs["params"] = {"page": page_number}
            page = self.client.get(endpoint, **kwargs)
            results.extend(page["results"])

        return results

    def update(self, model, **kwargs):
        self.logger.debug("updated %s with ID: %s", self.plural_name, model["id"])
        return self.client.put(
            f"/v1/{self.plural_name}/{model['id']}",
            json=model,
            **kwargs,
        )

    def delete(self, id, **kwargs):
        self.logger.debug("deleted %s with ID: %s", self.plural_name, id)
        return self.client.delete(f"/v1/{self.plural_name}/{id}", **kwargs)
