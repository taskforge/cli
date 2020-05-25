import os
from copy import copy
from tempfile import TemporaryDirectory
from unittest import TestCase
from collections import defaultdict
from unittest.mock import Mock, patch

from task_forge.sdk.client import v1


class CLITestCase(TestCase):
    command_mod = None

    def setUp(self):
        self.cfgdir = TemporaryDirectory()
        dummy_config = os.path.join(self.cfgdir.name, "config.toml")
        with open(dummy_config, "w") as f:
            f.write("")

        find_file_patcher = patch(
            "task_forge.cli.config.find_config_file", return_value=dummy_config
        )
        find_file_patcher.start()
        self.addCleanup(find_file_patcher.stop)

        save_patcher = patch(
            "task_forge.cli.config.Config.save", return_value=dummy_config
        )
        self.save_mock = save_patcher.start()
        self.addCleanup(save_patcher.stop)

        self.client = Mock()
        self.client.tasks = Mock(spec=v1.TaskClient)
        self.client.comments = Mock(spec=v1.CommentClient)
        self.client.users = Mock(spec=v1.UserClient)
        self.client.sources = Mock(spec=v1.SourceClient)
        self.client.contexts = Mock(spec=v1.ContextClient)
        self.client.login = lambda *args: {
            "access": "test",
            "refresh": "test",
        }
        self.client.set_token = lambda *args: self.client

        if self.command_mod is None:
            command_name = self.__class__.__name__[len("Test") :].lower()
            self.command_mod = f"{command_name}_cmd"

        patcher = patch(
            f"task_forge.cli.{self.command_mod}.get_client", return_value=self.client
        )
        self.get_client_patch = patcher.start()
        self.addCleanup(patcher.stop)
        self.empty_args = defaultdict(lambda: None)

    def args(self):
        return copy(self.empty_args)

    def tearDown(self):
        self.save_mock.assert_called()
        self.get_client_patch.stop()
        self.cfgdir.cleanup()
