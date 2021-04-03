import click

from taskforge.commands.filters.filters import filters
from taskforge.commands.utils import coro, inject_client, spinner


@filters.command()
@click.option(
    "--name",
    "-n",
    type=str,
    nargs=1,
    required=True,
)
@click.argument("query", nargs=-1)
@coro
@inject_client
async def save(name, query, client):
    """
    Create a new filter.

    The filter will be saved given the name, the rest of the arguments will be used as
    the query for the filter.
    """
    with spinner("Saving filter..."):
        q = " ".join(query)
        new_filter = {
            "name": name,
            "query": q,
            "columns": [],
        }
        await client.filters.create(new_filter)

    click.echo("Filter saved.")
