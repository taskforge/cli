import unittest
from tempfile import NamedTemporaryFile

import pytest

from task_forge.lists.sqlite import TaskList

from ..list_utils import TaskListBenchmarks, TaskListTests


class SQLiteTaskListTests(unittest.TestCase, TaskListTests):
    def setUp(self):
        self.tmpfile = NamedTemporaryFile()
        self.list = TaskList(file_name=self.tmpfile.name, create_tables=True)

    def tearDown(self):
        self.tmpfile.close()


@pytest.mark.benchmark(group="SQLite")
class TestSQLiteTaskListPerformance(TaskListBenchmarks):
    @pytest.fixture
    def task_list(self, tmpdir):  # pylint: disable=arguments-differ
        tmpfile = tmpdir.join("tasks.sqlite3")
        return TaskList(file_name=str(tmpfile), create_tables=True)
