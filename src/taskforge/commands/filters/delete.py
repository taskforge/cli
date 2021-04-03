import click

from taskforge.commands.filters.filters import filters
from taskforge.commands.utils import coro, inject_client


@filters.command()
@click.option(
    "--name",
    "-n",
    type=str,
    nargs=1,
    required=True,
)
@coro
@inject_client
async def delete(name, client):
    """
    Delete a filter.
    """
    existing = await client.filters.get_by_name(name)
    await client.filters.delete(existing["id"])
