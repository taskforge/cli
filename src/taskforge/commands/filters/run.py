import click

from taskforge.commands.filters.filters import filters
from taskforge.commands.utils import coro, inject_client, spinner
from taskforge.printing import FORMATS, print_tasks


@filters.command()
@click.option(
    "-f",
    "--format",
    default="table",
    type=FORMATS,
)
@click.argument("name", nargs=1)
@coro
@inject_client
async def run(name, format, client):
    """
    Run the given filter.

    The tasks can be displayed in one of four ways:

    --format=table

    The default format is a simple human-readable ASCII table.

    --format=json

    Produces a raw JSON dump of the server response. This is useful for scripting.

    --format=csv

    Produces a CSV table containing the raw server response

    --format=csv-pretty

    Produces a CSV table containing user emails, context names, and source names instead
    of IDs
    """
    with spinner("Retrieving tasks"):
        filter = await client.filters.get_by_name(name)
        tasks = await client.tasks.search(filter["query"])

    await print_tasks(tasks, client, format)
