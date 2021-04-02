import asyncio

import click

from taskforge.commands.cli import cli
from taskforge.commands.utils import coro, inject_client, spinner
from taskforge.state import State


@cli.command(aliases=["c", "done", "d"])
@click.argument("task-ids", nargs=-1)
@coro
@inject_client
async def complete(
    task_ids,
    client,
):
    """
    Mark tasks as complete.
    """
    with spinner("Completing tasks..."):
        if not task_ids:
            top = await client.tasks.next(State.current_context)
            task_ids = [top["id"]]

        await asyncio.gather(
            *map(
                client.tasks.complete,
                task_ids,
            )
        )

    click.echo("DONE!")
