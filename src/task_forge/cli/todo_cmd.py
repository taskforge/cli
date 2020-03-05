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

from task_forge.lists import NotFoundError, TaskList
from task_forge.ql.ast import AST, Expression
from task_forge.ql.tokens import Token
from task_forge.cli.query_cmd import print_tasks
from task_forge.cli.utils import inject_list


@inject_list
def run(args: Any, task_list: TaskList) -> None:
    """Print the current task in task_list."""
    ast = AST(
        Expression(
            Token("="),
            left=Expression(Token("completed")),
            right=Expression(Token("false")),
        )
    )

    try:
        tasks = task_list.search(ast)
        print_tasks(tasks, output=args["--output"])
    except NotFoundError:
        print("No incomplete tasks!")
