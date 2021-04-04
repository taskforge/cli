import logging

from taskforge.client.base import ModelClient, NameRetrivalMixin

logger = logging.getLogger(__name__)


class ContextClient(ModelClient, NameRetrivalMixin):
    plural_name = "contexts"
    reverse_mapping_key = "name"
