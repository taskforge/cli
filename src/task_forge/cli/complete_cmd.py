"""
Usage: task complete [<ID>...]

Complete tasks by ID. If no IDs are provided then the current task indicated by
'task next' is completed.
"""

import sys
from typing import Any, List

from task_forge.cli.utils import config, get_client
from task_forge.cli.config import Config


@config
def complete_tasks(tasks: List[str], cfg: Config) -> None:
    """
    Complete tasks by the ids in tasks.

    If no tasks are provided then complete the current task.
    """
    client = get_client(cfg)
    if not tasks:
        try:
            current = client.tasks.current()
            tasks = [current.id]
        except Exception:
            print("no IDs given and no current task found")
            sys.exit(0)

    for task in tasks:
        client.tasks.complete_by_id(task)


def run(args: Any) -> None:
    """Add the next command to parser."""
    tasks = args["<ID>"]
    complete_tasks(tasks)  # pylint: disable=no-value-for-parameter
