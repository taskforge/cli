import sys

import click

from taskforge.commands.filters.filters import filters
from taskforge.commands.utils import inject_client, spinner


@filters.command()
@click.option(
    "--name",
    "-n",
    type=str,
    nargs=1,
    required=True,
)
@click.argument("query", nargs=-1)
@inject_client
def update(name, query, client):
    """
    Update the query for a filter.
    """
    with spinner("Updating filter..."):
        existing = client.filters.get_by_name(name)
        if existing:
            existing["query"] = " ".join(query)
            client.filters.update(existing)

    if existing:
        click.echo("Filter saved.")
    else:
        click.echo("No filter with that name exists!")
        sys.exit(1)
