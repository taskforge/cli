from taskforge.client.base import ModelClient, NameRetrivalMixin


class SourceClient(ModelClient, NameRetrivalMixin):
    plural_name = "sources"
    reverse_mapping_key = "name"
