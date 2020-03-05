"""
Usage: task workon <ID>

Find task with ID and make it so the priority of the task is 0.1
higher than that of the current highest priority task. Effectively
making it the "current" task in Taskforge terms.
"""

import sys
from typing import Any

from task_forge.cli.utils import inject_list
from task_forge.lists import NotFoundError, TaskList


def top_priority(task_list: TaskList) -> int:
    """Return a priority that is 0.1 more than the current highest priority."""
    try:
        task = task_list.current()
        current_priority = task.priority
    except NotFoundError:
        current_priority = 1

    return current_priority + 1


@inject_list
def run(args: Any, task_list: TaskList) -> None:
    """Print the current task in task_list."""
    try:
        new_current = task_list.find_by_id(args["<ID>"])
    except NotFoundError:
        print("no task with that id exists")
        sys.exit(1)

    new_current.priority = top_priority(task_list)
    try:
        task_list.update(new_current)
    except NotFoundError:
        print("something unexpected went wrong, unable to update task")
        sys.exit(1)
