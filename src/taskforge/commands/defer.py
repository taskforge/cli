import asyncio

import click

from taskforge.commands.cli import cli
from taskforge.commands.utils import coro, inject_client, spinner
from taskforge.state import State


@cli.command()
@click.argument("task-ids", nargs=-1)
@coro
@inject_client
async def defer(
    task_ids,
    client,
):
    """
    Defer the current task by reducing it's priority.
    """
    with spinner("Updating tasks..."):
        if not task_ids:
            top = await client.tasks.next(State.current_context)
            task_ids = [top["id"]]

        tasks = await asyncio.gather(
            *map(
                client.tasks.get,
                task_ids,
            )
        )

        async def __defer(task):
            task["priority"] -= 1
            return await client.tasks.update(task)

        await asyncio.gather(
            *map(
                __defer,
                tasks,
            )
        )

    click.echo("DONE!")
