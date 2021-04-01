import asyncio
import shutil
import textwrap

from tabulate import tabulate


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
