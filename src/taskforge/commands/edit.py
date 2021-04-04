import os
import subprocess
import tempfile

import click
import yaml

from taskforge.commands.cli import cli
from taskforge.commands.utils import inject_client, spinner
from taskforge.printing import populate
from taskforge.state import State


def reverse_populate(client):
    def wrapper(task):
        owner, source, context = (
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
@inject_client
def edit(
    task_ids,
    client,
):
    """
    Edit tasks as YAML files.
    """
    if not task_ids:
        top = client.tasks.next(State.current_context)
        task_ids = [top["id"]]

    tasks = map(
        populate(client),
        map(
            client.tasks.get,
            task_ids,
        ),
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
            edited_tasks = map(
                reverse_populate(client),
                edited_tasks,
            )

            for task in edited_tasks:
                client.tasks.update(task)
    finally:
        os.unlink(fh.name)

    click.echo("DONE!")
