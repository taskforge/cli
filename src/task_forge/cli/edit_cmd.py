"""
Usage: task edit [<ID>]

Edit the task indicated by ID as a yaml file. If no ID given opens the current
task.

Will use $EDITOR if set and if not will attempt to find an editor based on
platform.
"""

import os
import sys
from tempfile import NamedTemporaryFile
from subprocess import call

import yaml

from task_forge.cli.utils import config, get_client
from task_forge.sdk.types import Task
from task_forge.sdk.exceptions import NotFound


def get_editor_program():
    """Return editor based on operating system"""
    editor_prg = os.getenv("EDITOR", None)
    if editor_prg is not None:
        return editor

    if sys.platform == "win32":
        return "notepad.exe"

    return "vi"


def editor(filename):
    """Open filename in $EDITOR"""
    program = get_editor_program()
    call([program, filename], stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr)


@config
def run(args, cfg):
    """Open task by ID in $EDITOR. Update task based on result."""
    client = get_client(cfg)

    try:
        if args["<ID>"]:
            task = client.tasks.get(args["<ID>"])
        else:
            task = client.tasks.current()

        # This slightly awkward dance that looks like it could be solved by a context manager is
        # caused by a few issues. First NamedTemporaryFile if used as a context manager will auto
        # delete itself when the block exits. That means that if we use a context manager for it we
        # can't release the file handle without deleting the file. For Windows we have to release
        # the file handle to allow $EDITOR to open it (otherwise it will complain about the file
        # being busy). So what we have to do is open the file for writing, write to it explicitly
        # close the handle (so it doesn't delete itself), open it with the editor program, then
        # re-open it for reading ourselves. Finally we have to explicitly clean up the temp file.
        tmp = NamedTemporaryFile(mode="w+", suffix=".toml", delete=False)
        yaml.dump(task.to_dict(), tmp)
        tmp.close()

        editor(tmp.name)

        with open(tmp.name) as tmp:
            new_task = Task(**yaml.safe_load(tmp))

        client.tasks.update(new_task)
        os.remove(tmp.name)
    except NotFound:
        print("No task with that ID exists")
        sys.exit(1)
