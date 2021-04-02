import asyncio

import click

from taskforge.commands.cli import cli
from taskforge.commands.utils import coro, inject_client, spinner


@cli.command(aliases=["w", "workon"])
@click.argument("task-id")
@coro
@inject_client
async def work_on(
    task_id,
    client,
):
    """
    Make a task the top priority.
    """
    with spinner("Updating task..."):
        top, task = await asyncio.gather(
            client.tasks.next(),
            client.tasks.get(task_id),
        )
        already_top = top["id"] == task["id"]
        if not already_top:
            task["priority"] = top["priority"] + 1
            await client.tasks.update(task)

    if already_top:
        print("That task was already the top priority!")
    else:
        print(f"'{task['title']}' is now the top priority.")
