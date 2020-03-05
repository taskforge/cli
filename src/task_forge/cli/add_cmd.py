"""
Usage: task add [options] [<title>...]

Add or import tasks into the list.

Options:
   -p <priority>, --priority <priority>  Create the task with the indicated
                                         priority, this can be an integer or
                                         float [default: 1.0]
   -b <body>, --body <body>              The body or "description" of the task
   -c <context>, --context <context>     The context in which to create the task
   -t, --top                             Make this task the top priority

Import Options:
   -f <file>, --from-file <file>  Import tasks from the indicated JSON file

If an import option is provided all other options are ignored.
"""

import sys
from typing import Any

from task_forge.cli.utils import inject_list
from task_forge.cli.workon_cmd import top_priority
from task_forge.lists import TaskList
from task_forge.models import Task


def import_file(filename: str, task_list: TaskList) -> None:
    """Import tasks from filename into the configured task list"""
    import json

    with open(filename) as tasks_file:
        task = json.load(tasks_file)
        if isinstance(task, list):
            tasks = [Task.from_dict(t) for t in task]
            task_list.add_multiple(tasks)
        else:
            task_list.add(task)


@inject_list
def run(args: Any, task_list: TaskList) -> None:
    """Parse the docopt args and call add_task."""
    if args["--from-file"]:
        import_file(args["--from-file"], task_list)
        return

    if not args["<title>"]:
        print("when not importing tasks title is required")
        sys.exit(1)

    title = " ".join(args["<title>"])
    priority = int(args["--priority"]) if args["--priority"] else 1
    context = args["--context"] if args["--context"] else "default"
    body = args["--body"] if args["--body"] else ""

    if args["--top"]:
        priority = top_priority(task_list)

    task_list.add(Task(title, body=body, context=context, priority=priority))
