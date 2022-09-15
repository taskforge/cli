import click

from taskforge.commands.cli import cli
from taskforge.commands.utils import inject_client, spinner
from taskforge.printing import FORMATS, print_tasks


@cli.command(aliases=["s", "list", "query", "q"])
@click.option(
    "-f",
    "--format",
    default="table",
    type=FORMATS,
)
@click.argument("query", nargs=-1)
@inject_client
def search(query, format, client):
    """
    Search for tasks using TQL. If no query given lists all tasks.

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
    with spinner("Retrieving tasks", disabled=format in ("csv", "json", "csv-pretty")):
        if query:
            tasks = client.tasks.search(" ".join(query))
        else:
            tasks = client.tasks.list()

    print_tasks(tasks, client, format)
