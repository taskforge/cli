"""
Usage: task complete [<ID>...]

Complete tasks by ID. If no IDs are provided then the current task indicated by
'task next' is completed.
"""

import sys
from typing import Any, List

from task_forge.cli.utils import inject_list
from task_forge.lists import NotFoundError, TaskList


@inject_list
def complete_tasks(tasks: List[str], task_list: TaskList) -> None:
    """
    Complete tasks by the ids in tasks.

    If no tasks are provided then complete the current task.
    """
    try:
        current = task_list.current()
        tasks = [current.id]
    except NotFoundError:
        print("no ID given and no current task found")
        sys.exit(0)

    for task in tasks:
        task_list.complete(task)


def run(args: Any) -> None:
    """Add the next command to parser."""
    tasks = args["<ID>"]
    complete_tasks(tasks)  # pylint: disable=no-value-for-parameter
