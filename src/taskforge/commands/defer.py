import click

from taskforge.commands.cli import cli
from taskforge.commands.utils import inject_client, spinner
from taskforge.state import State


@cli.command()
@click.argument("task-ids", nargs=-1)
@inject_client
def defer(
    task_ids,
    client,
):
    """
    Defer the current task by reducing it's priority.
    """
    with spinner("Updating tasks..."):
        if not task_ids:
            top = client.tasks.next(State.current_context)
            task_ids = [top["id"]]

        for task_id in task_ids:
            task = client.tasks.get(task_id)
            task["priority"] -= 1
            client.tasks.update(task)

    click.echo("Tasks deferred.")
