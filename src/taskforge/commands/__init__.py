# flake8: noqa

# Export the actual cli entrypoint
import taskforge.commands.list_cmd

# Import all the commands so they get registered
import taskforge.commands.next
from taskforge.commands.cli import cli
