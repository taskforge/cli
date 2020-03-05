import unittest
from multiprocessing import Process
from tempfile import NamedTemporaryFile

from task_forge.lists.sqlite import List as SQLiteList
from task_forge.lists.task_server_client import List
from task_forge.server.server import Server

from ..list_utils import ListTests


class TaskforgeServerListTests(unittest.TestCase, ListTests):
    def setUp(self):
        self.tmpfile = NamedTemporaryFile()
        tmp = NamedTemporaryFile(suffix=".sock")
        self.addr = tmp.name
        tmp.close()
        self.server = Server(
            SQLiteList(file_name=self.tmpfile.name, create_tables=True),
            unix_socket=self.addr,
        )
        self.proc = Process(target=self.server.run)
        self.proc.start()
        self.list = List(unix_socket=self.addr)

    def tearDown(self):
        self.tmpfile.close()
        self.proc.terminate()
        self.list.client.stop()
