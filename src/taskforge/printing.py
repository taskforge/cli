import asyncio
import json
import shutil
import sys
import textwrap
from csv import DictWriter

import click
from tabulate import tabulate

from taskforge.commands.utils import spinner

FORMATS = click.Choice(
    ["table", "json", "csv", "csv-pretty"],
    case_sensitive=False,
)


def populate(client):
    async def transform(task):
        user, source, context = await asyncio.gather(
            client.users.get(task["owner"]),
            client.sources.get(task["source"]),
            client.contexts.get(task["context"]),
        )

        task["owner"] = user["email"]
        task["context"] = context["name"]
        task["source"] = source["name"]
        return task

    return transform


def wordwrap(max_width, title_index):
    def wrapper(row):
        if row[0] == "ID":
            return row

        total_width = sum(len(v) + 2 for v in row)
        if total_width < max_width:
            return row

        available_width = max_width - (total_width - len(row[title_index]))
        if available_width <= 0:
            raise Exception("Not enough room to display tasks!")

        row[title_index] = textwrap.shorten(row[title_index], available_width)
        return row

    return wrapper


def to_row(task, small_term):
    if small_term:
        return [
            task["id"],
            task["title"],
            task["context"],
        ]
    else:
        return [
            task["id"],
            str(task["created_date"]),
            str(task["completed_date"]),
            str(task["priority"]),
            task["title"],
            task["context"],
            task["source"],
            task["owner"],
        ]


async def print_table(client, tasks, tablefmt="plain"):
    """Print an ASCII table of the tasks."""
    with spinner(text="Gathering task metadata..."):
        data = await asyncio.gather(*map(populate(client), tasks))

    terminal = shutil.get_terminal_size((80, 20))
    small_term = terminal.columns < 250
    if small_term:
        columns = [
            "ID",
            "Title",
            "Context",
        ]

    else:
        columns = [
            "ID",
            "Created Date",
            "Completed Date",
            "Priority",
            "Title",
            "Context",
            "Source",
            "Owner",
        ]

    rows = [columns]
    rows.extend(
        [to_row(task, small_term) for task in data],
    )

    print(
        tabulate(
            map(
                wordwrap(
                    max_width=terminal.columns,
                    title_index=1 if small_term else 4,
                ),
                rows,
            ),
            headers="firstrow",
            tablefmt=tablefmt,
        ),
    )


def print_json(task_or_tasks):
    data = json.dumps(task_or_tasks, indent=4)
    print(data)


async def print_csv(task_or_tasks, client=None, pretty=False):
    if isinstance(task_or_tasks, list):
        data = task_or_tasks
    else:
        data = [task_or_tasks]

    if not data:
        return

    fieldnames = list(data[0].keys())
    if pretty:
        data = await asyncio.gather(*map(populate(client), data))

    writer = DictWriter(sys.stdout, fieldnames=fieldnames)
    for row in data:
        writer.writerow(row)


async def print_tasks(tasks, client, format):
    format = format.lower()
    if format == "json":
        print_json(tasks)
    elif format == "csv":
        await print_csv(tasks)
    elif format == "csv-pretty":
        await print_csv(tasks, client=client, pretty=True)
    else:
        await print_table(client, tasks)
