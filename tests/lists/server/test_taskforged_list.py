import os
import unittest
import socket
import requests
import subprocess
import pytest

from contextlib import closing
from tempfile import NamedTemporaryFile

from task_forge.daemon import Daemon
from task_forge.lists.sqlite import TaskList as SQLiteList
from task_forge.lists.taskforged import TaskList

from ..list_utils import TaskListTests


def find_free_port():
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(("localhost", 0))
        return s.getsockname()[1]


class TaskforgeDaemonListTests(unittest.TestCase, TaskListTests):
    def setUp(self):
        self.tmpfile = NamedTemporaryFile()

        # Have to remove the file that NamedTemporaryFile creates so
        # the sqlite list created by taskforged will run create_tables
        os.remove(self.tmpfile.name)

        # Can't used NamedTemporaryFile here because for some reason
        # os.path.isfile (used in config.py for loading) returns False
        # for them even after we create it below by writing to it.
        self.cfgfile = "/tmp/taskforged_test_config.toml"

        port = find_free_port()

        with open(self.cfgfile, "w") as cfgfile:
            cfgfile.write(
                """[list]
name = 'sqlite'

[list.config]
file_name = '{sqlite_file}'

[server]
host = 'localhost'
port = {free_port}
""".format(
                    sqlite_file=self.tmpfile.name, free_port=port
                )
            )

        self.proc = subprocess.Popen(
            ["taskforged", "--config-file={}".format(self.cfgfile)]
        )

        # Give the server time to start, if we don't do this some
        # weird GIL-ness (I'm guessing) causes the process to never
        # get to the point of accepting connections before we try
        # connecting.
        try:
            self.proc.communicate(timeout=2)
        except subprocess.TimeoutExpired:
            pass

        self.list = TaskList(port=port)

    def tearDown(self):
        self.tmpfile.close()
        self.proc.terminate()
