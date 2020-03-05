import os
import unittest
import socket
import requests
import subprocess
import pytest

from contextlib import closing
from tempfile import NamedTemporaryFile

from task_forge.daemon import Daemon
from task_forge.lists.sqlite import List as SQLiteList
from task_forge.lists.taskforged import List

from ..list_utils import ListTests


def find_free_port():
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(("localhost", 0))
        return s.getsockname()[1]


class TaskforgeDaemonListTests(unittest.TestCase, ListTests):
    def setUp(self):
        self.tmpfile = NamedTemporaryFile()
        os.remove(self.tmpfile.name)
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
        try:
            self.proc.communicate(timeout=2)
        except subprocess.TimeoutExpired:
            pass

        self.list = List(port=port)

    def tearDown(self):
        self.tmpfile.close()
        self.proc.terminate()
