# flake8: noqa
"""
We have to import all the commands so they get registered here.

We then export the CLI entrypoint for use in the console_scripts
"""

import taskforge.commands.list_cmd
import taskforge.commands.next
import taskforge.commands.switch_context

# Export the actual cli entrypoint
from taskforge.commands.cli import cli
