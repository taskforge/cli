import click

from taskforge.commands.cli import cli
from taskforge.commands.utils import coro, inject_client
from taskforge.printing import print_json


@cli.command(aliases=["n"])
@click.option("-t", "--title-only", "title_only", is_flag=True, default=False)
@click.option("-i", "--id-only", "id_only", is_flag=True, default=False)
@click.option("-j", "--json", "as_json", is_flag=True, default=False)
@coro
@inject_client
async def next(
    title_only,
    id_only,
    as_json,
    client,
):
    task = await client.tasks.next()
    if title_only:
        print(task["title"])
    elif id_only:
        print(task["id"])
    elif as_json:
        print_json(task)
    else:
        print(task["id"], task["title"])