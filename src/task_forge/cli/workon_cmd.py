"""
Usage: task workon <ID>

Find task with ID and make it so the priority of the task is 0.1
higher than that of the current highest priority task. Effectively
making it the "current" task in Taskforge terms.
"""

import sys
from typing import Any

from task_forge.cli.utils import config, get_client
from task_forge.cli.config import Config
from task_forge.sdk.exceptions import NotFound


def top_priority(client) -> int:
    """Return a priority that is 0.1 more than the current highest priority."""
    try:
        task = client.tasks.current()
        return task.priority + 1
    except NotFound:
        return 2


@config
def run(args: Any, cfg: Config) -> None:
    """Make the given task the new current task"""
    client = get_client(cfg)
    try:
        new_current = client.tasks.get(args["<ID>"])
    except NotFound:
        print("no task with id: {} exists".format(args["<ID>"]))
        sys.exit(1)

    new_current.priority = top_priority(client)
    client.tasks.update(new_current)
