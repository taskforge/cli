import click

from taskforge.commands.cli import cli
from taskforge.commands.utils import coro, inject_client
from taskforge.printing import print_table


@cli.command(aliases=["l", "query", "q", "list"])
@click.argument("query", nargs=-1)
@coro
@inject_client
async def search(query, client):
    if query:
        tasks = await client.tasks.search(" ".join(query))
    else:
        tasks = await client.tasks.list()

    await print_table(client, tasks)
