from taskforge.client.base import ModelClient, NameRetrivalMixin


class FilterClient(ModelClient, NameRetrivalMixin):
    plural_name = "filters"
    reverse_mapping_key = "name"
