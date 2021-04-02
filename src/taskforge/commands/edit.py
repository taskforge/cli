import asyncio
import os
import subprocess
import tempfile

import click
import yaml

from taskforge.commands.cli import cli
from taskforge.commands.utils import coro, inject_client, spinner
from taskforge.printing import populate
from taskforge.state import State


def reverse_populate(client):
    async def wrapper(task):
        owner, source, context = await asyncio.gather(
            client.users.reverse_lookup(task["owner"]),
            client.sources.reverse_lookup(task["source"]),
            client.contexts.reverse_lookup(task["context"]),
        )
        task["owner"] = owner["id"]
        task["source"] = source["id"]
        task["context"] = context["id"]
        return task

    return wrapper


@cli.command(aliases=["e"])
@click.argument("task-ids", nargs=-1)
@coro
@inject_client
async def edit(
    task_ids,
    client,
):
    """
    Edit tasks as YAML files.
    """
    if not task_ids:
        top = await client.tasks.next(State.current_context)
        task_ids = [top["id"]]

    tasks = await asyncio.gather(
        *map(
            client.tasks.get,
            task_ids,
        )
    )

    tasks = await asyncio.gather(
        *map(
            populate(client),
            tasks,
        )
    )

    fh = tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".yaml",
        encoding="utf-8",
        delete=False,
    )
    yaml.dump(tasks, fh)
    fh.close()

    editor = os.getenv("EDITOR", "vi")
    subprocess.run([editor, fh.name])

    try:
        with open(fh.name) as edited:
            edited_tasks = yaml.safe_load(edited)

        with spinner("Updating tasks..."):
            edited_tasks = await asyncio.gather(
                *map(
                    reverse_populate(client),
                    edited_tasks,
                )
            )

            await asyncio.gather(
                *map(
                    client.tasks.update,
                    edited_tasks,
                )
            )
    finally:
        os.unlink(fh.name)

    click.echo("DONE!")
