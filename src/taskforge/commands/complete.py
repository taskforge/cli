import click

from taskforge.commands.cli import cli
from taskforge.commands.utils import inject_client, spinner
from taskforge.state import State


@cli.command(aliases=["c", "done", "d"])
@click.argument("task-ids", nargs=-1)
@inject_client
def complete(
    task_ids,
    client,
):
    """
    Mark tasks as complete.
    """
    with spinner("Completing tasks..."):
        if not task_ids:
            top = client.tasks.next(State.current_context)
            task_ids = [top["id"]]

        for task in task_ids:
            client.tasks.complete(task)

    click.echo("DONE!")
