import click

from taskforge.commands.cli import cli
from taskforge.commands.utils import inject_client, spinner


@cli.command(aliases=["w", "workon"])
@click.argument("task-id")
@inject_client
async def work_on(
    task_id,
    client,
):
    """
    Make a task the top priority.
    """
    with spinner("Updating task..."):
        top, task = (
            client.tasks.next(),
            client.tasks.get(task_id),
        )

        already_top = top["id"] == task["id"]
        if not already_top:
            task["priority"] = top["priority"] + 1
            client.tasks.update(task)

    if already_top:
        click.echo("That task was already the top priority!")
    else:
        click.echo(f"'{task['title']}' is now the top priority.")
