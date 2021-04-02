import click

from taskforge.commands.cli import cli
from taskforge.commands.utils import coro, inject_client


@cli.command(aliases=["a"])
@click.option("-t", "--top", is_flag=True)
@click.option("-c", "--context", "context", default=None, type=str)
@click.option("-p", "--priority", "priority", default=1, type=int)
@click.argument("title", nargs=-1, required=True, type=str)
@coro
@inject_client
async def add(
    title,
    top,
    context,
    priority,
    client,
):
    """
    Add a task to Taskforge
    """
    task = {
        "title": " ".join(title),
        "priority": priority,
    }

    if context:
        ctx = await client.contexts.get_by_name(context)
        task["context"] = ctx["id"]

    if top:
        current = await client.tasks.next(context=context)
        task["priority"] = current["priority"] + 1

    created = await client.tasks.create(task)
    msg = "Created: {} {}".format(
        created["id"],
        created["title"],
    )
    click.echo(msg)
