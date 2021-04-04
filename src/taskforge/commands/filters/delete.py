import click

from taskforge.commands.filters.filters import filters
from taskforge.commands.utils import inject_client


@filters.command()
@click.option(
    "--name",
    "-n",
    type=str,
    nargs=1,
    required=True,
)
@inject_client
def delete(name, client):
    """
    Delete a filter.
    """
    existing = client.filters.get_by_name(name)
    client.filters.delete(existing["id"])
