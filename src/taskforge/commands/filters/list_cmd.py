import click

from taskforge.commands.filters.filters import filters
from taskforge.commands.utils import coro, inject_client


@filters.command()
@coro
@inject_client
async def list(client):
    """
    List saved filters.
    """
    for filter in await client.filters.list():
        click.echo(filter["name"])
