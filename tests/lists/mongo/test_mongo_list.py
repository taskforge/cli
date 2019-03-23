# pylint: disable=missing-docstring

import unittest
from uuid import uuid1

import pytest

from task_forge.lists import InvalidConfigError
from task_forge.lists.mongo import List

from ..list_utils import ListBenchmarks, ListTests

@pytest.mark.slow
class MongoDBListConstructorTests(unittest.TestCase):
    def test_conn_url_with_username_and_password(self):
        try:
            mongo_list = List(username='test')
            self.assertEqual(True, False)
        except InvalidConfigError:
            pass

        mongo_list = List(username='test', password='pass123')
        self.assertEqual(mongo_list.conn_url,
                         'mongodb://test:pass123@localhost:27017')


@pytest.mark.slow
class MongoDBListTests(unittest.TestCase, ListTests):
    def setUp(self):
        self.list = List(db=uuid1().hex)

    def teardown(self):
        self.list._client.close()  # pylint: disable=protected-access


@pytest.mark.benchmark(group='MongoDB')
class TestMongoDBListPerformance(ListBenchmarks):
    @pytest.fixture
    def task_list(self):
        mongo = List(db=uuid1().hex)
        yield mongo
        mongo._client.close()  # pylint: disable=protected-access
