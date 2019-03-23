# pylint: disable=missing-docstring

import unittest
import os
from tempfile import NamedTemporaryFile

import pytest

from task_forge.lists.github import List

from ..list_utils import ListBenchmarks, ListTests


INTEGRATION_TESTING_REPO = 'taskforge/github-issues-list-integration-tester'


@pytest.mark.slow
@unittest.skipIf(os.getenv('TASKFORGE_GITHUB_TEST_TOKEN') is None,
                 '$TASKFORGE_GITHUB_TEST_TOKEN not set, skipping github list tests')
class GithubListTests(unittest.TestCase, ListTests):
    def setUp(self):
        token = os.getenv('TASKFORGE_GITHUB_TEST_TOKEN')
        self.tmpfile = NamedTemporaryFile()
        self.list = List(
            sqlite_cache_file=self.tmpfile.name,
            sqlite_create_tables=True,
            create_repo=INTEGRATION_TESTING_REPO,
            query_repo=INTEGRATION_TESTING_REPO,
            self_assign_on_create=True,
            use_metadata_labels=True,
            access_token=token,
        )

    def tearDown(self):
        self.tmpfile.close()
        for issue in self.list.client.get_repo(INTEGRATION_TESTING_REPO).get_issues():
            issue.edit(state='closed')


@pytest.mark.benchmark(group='Github')
@unittest.skipIf(os.getenv('TASKFORGE_GITHUB_TEST_TOKEN') is None,
                 '$TASKFORGE_GITHUB_TEST_TOKEN not set, skipping github list tests')
@unittest.skipIf(os.getenv('TASKFORGE_GITHUB_RUN_BENCHMARKS') != "1",
                 '$TASKFORGE_GITHUB_RUN_BENCHMARKS is not set to 1')
class TestGithubListPerformance(ListBenchmarks):
    @pytest.fixture
    def task_list(self, tmpdir):  # pylint: disable=arguments-differ
        token = os.getenv('TASKFORGE_GITHUB_TEST_TOKEN')
        tmpfile = NamedTemporaryFile()
        return List(
            sqlite_cache_file=tmpfile.name,
            sqlite_create_tables=True,
            create_repo='taskforge/github-issues-list-integration-tester',
            query_repo='taskforge/github-issues-list-integration-tester',
            self_assign_on_create=True,
            use_metadata_labels=True,
            access_token=token,
        )
