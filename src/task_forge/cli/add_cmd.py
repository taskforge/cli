"""
Usage: task add [options] [<title>...]

Add or import tasks into the list.

Options:
   -p <priority>, --priority <priority>  Create the task with the indicated
                                         priority, this can be an integer or
                                         float [default: 1]
   -b <body>, --body <body>              The body or "description" of the task
   -c <context>, --context <context>     The context in which to create the task
   -t, --top                             Make this task the top priority

Import Options:
   -f <file>, --from-file <file>  Import tasks from the indicated JSON file

If an import option is provided all other options are ignored.
"""

import sys
from typing import Any

from task_forge.cli.utils import config, get_client
from task_forge.sdk.types import Task
from task_forge.cli.config import Config
from task_forge.cli.workon_cmd import top_priority


def import_file(filename: str) -> None:
    """Import tasks from filename into the configured task list"""
    import json

    with open(filename) as tasks_file:
        task = json.load(tasks_file)
        if isinstance(task, list):
            tasks = [Task(**t) for t in task]
        else:
            tasks = [Task(**task)]

    return tasks


@config
def run(args: Any, cfg: Config) -> None:
    """Parse the docopt args and call add_task."""
    client = get_client(cfg)

    if args["--from-file"]:
        tasks = import_file(args["--from-file"])
        for task in tasks:
            client.tasks.create(task)
        return

    if not args["<title>"]:
        print("when not importing tasks title is required")
        sys.exit(1)

    title = " ".join(args["<title>"])
    priority = int(args["--priority"]) if args["--priority"] else None
    if args["--top"]:
        priority = top_priority(client)
    context = args["--context"] if args["--context"] else None
    if context:
        context_obj = client.contexts.get_by_name(context)
        if context_obj:
            context = context_obj.id
    body = args["--body"] if args["--body"] else None
    task = Task(title=title, priority=priority, body=body, context=context)
    client.tasks.create(task)
