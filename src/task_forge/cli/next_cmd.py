"""
Usage: task next [options]

Print the "next" or "current" task. This is calculated by the list as the
highest priority, oldest task in the list.

Default output format is:

$TASK_ID: $TASK_TITLE

You can modify the output with the options below.

Options:
    -i, --id-only     Print only the task ID
    -t, --title-only  Print only the task title
"""

from typing import Any

from task_forge.cli.utils import config, get_client
from task_forge.cli.config import Config
from task_forge.sdk.exceptions import NotFound


@config
def run(args: Any, cfg: Config) -> None:
    """Print the current task in task_list."""
    client = get_client(cfg)

    try:
        task = client.tasks.current()
    except NotFound:
        print("No next task, you're all done!")
        return

    if args["--title-only"]:
        print(task.title)
    elif args["--id-only"]:
        print(task.id)
    else:
        print(f"{task.id}: {task.title}")
