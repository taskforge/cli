# flake8: noqa
"""
We have to import all the commands so they get registered here.

We then export the CLI entrypoint for use in the console_scripts
"""

import taskforge.commands.add
import taskforge.commands.complete
import taskforge.commands.login
import taskforge.commands.next
import taskforge.commands.register
import taskforge.commands.search
import taskforge.commands.switch_context
import taskforge.commands.todo

# Export the actual cli entrypoint
from taskforge.commands.cli import cli
