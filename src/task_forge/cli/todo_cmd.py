"""
Usage: task todo [options]

A convenience command for listing tasks which are incomplete.

Options:
    -o <format>, --output <format>  How to display the tasks which match the
                                    query. Available formats are: json, csv,
                                    table, text. See 'task list --help' for
                                    more information on how each format is
                                    displayed. [default: table]

For more information on available output formats see 'man task-query'
"""

from typing import Any

from task_forge.cli.query_cmd import print_tasks
from task_forge.cli.config import Config
from task_forge.cli.utils import config, get_client
from task_forge.sdk.exceptions import NotFound


@config
def run(args: Any, cfg: Config) -> None:
    """Print the current task in task_list."""
    client = get_client(cfg)
    query = "completed = false"
    try:
        tasks = client.tasks.search(query)
        print_tasks(tasks, output=args["--output"])
    except NotFound:
        print("No incomplete tasks!")
