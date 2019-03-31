"""
Usage: task [options] <command> [<args>...]

A task management CLI that integrates with external services.

Options:
  -h, --help      Print this help message
  --version       Print version and license information
  -v, --verbose   Print debug information, useful when submitting bug reports!

Commands:
   help                Print usage information about task commands
   add (new, a)        Add a new task to the list
   next (n)            Print the next or "current" task in the list
   todo                Print incomplete tasks in the list
   edit (e)            Edit task data as a toml file
   complete (done, d)  Complete tasks in the list.
   query (q, s, list)  Search or list tasks in the list
   workon              Move a task to the top of the list

See 'task help <command>' for more information on a specific command.
"""

import logging
import sys

from docopt import docopt

ALIASES = {
    "n": "next",
    "new": "add",
    "a": "add",
    "d": "complete",
    "done": "complete",
    "q": "query",
    "s": "query",
    "l": "query",
    "list": "query",
    "e": "edit",
}


def print_lists():
    """Print installed list implementations"""
    from ..lists.load import get_all_lists

    print("Available lists are:")
    try:
        lists = get_all_lists()
    except ImportError as import_err:
        print(f"unable to load lists: {import_err}")
        sys.exit(1)

    if not lists:
        print("no lists are installed")
        sys.exit(0)

    for name, _ in lists:
        print(f"  {name}")


def main():
    """CLI entrypoint, handles subcommand parsing"""
    args = docopt(__doc__, version="task version 0.3.0", options_first=True)
    if not args["<command>"]:
        print(__doc__)
        sys.exit(1)

    command = args["<command>"]
    if command == "help" or args["--help"]:
        topic = None
        if args["<args>"]:
            topic = args["<args>"][0]

        if topic == "lists":
            print_lists()
        elif topic is not None:
            try:
                from importlib import import_module

                command_mod = import_module(f"task_forge.cli.{topic}_cmd")
                print(command_mod.__doc__)
            except ImportError:
                print(f"{topic} is not a known task command")
                sys.exit(1)
        else:
            print(__doc__)

        sys.exit(0)

    if args["--verbose"]:
        logging.basicConfig(level=logging.DEBUG)

    command = ALIASES.get(command, command)
    if command == "add":
        import task_forge.cli.add_cmd as command_mod
    elif command == "next":
        import task_forge.cli.next_cmd as command_mod
    elif command == "todo":
        import task_forge.cli.todo_cmd as command_mod
    elif command == "edit":
        import task_forge.cli.edit_cmd as command_mod
    elif command == "complete":
        import task_forge.cli.complete_cmd as command_mod
    elif command == "query":
        import task_forge.cli.query_cmd as command_mod
    elif command == "workon":
        import task_forge.cli.workon_cmd as command_mod
    else:
        print(f"{command} is not a known task command")
        print(__doc__)
        sys.exit(1)

    argv = [command] + args["<args>"]
    command_mod.run(docopt(command_mod.__doc__, argv=argv))
    sys.exit(0)


if __name__ == "__main__":
    main()
