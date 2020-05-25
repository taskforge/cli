from tests.utils import CLITestCase
from task_forge.cli.add_cmd import run


class TestAdd(CLITestCase):
    def test_add_cmd(self):
        args = self.args()
        args["<title>"] = ["test", "task"]
        run(args)
        self.client.tasks.create.assert_called()
