import click

from taskforge.commands.cli import cli
from taskforge.commands.utils import coro, inject_client, spinner
from taskforge.printing import FORMATS, print_tasks


@cli.command(aliases=["td"])
@click.option(
    "-f",
    "--format",
    default="table",
    type=FORMATS,
)
@coro
@inject_client
async def todo(format, client):
    """
    Show incomplete tasks.

    The tasks can be displayed in one of four ways:

    --format=table

    The default format is a simple human-readable ASCII table.

    --format=json

    Produces a raw JSON dump of the server response. This is useful for scripting.

    --format=csv

    Produces a CSV table containing the raw server response

    --format=csv-pretty

    Produces a CSV table containing user emails, context names, and source names instead
    of IDs.
    """
    with spinner("Retrieving tasks"):
        tasks = await client.tasks.search("completed = false")

    await print_tasks(tasks, client, format)
