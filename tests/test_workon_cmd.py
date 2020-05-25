from tests.utils import CLITestCase
from task_forge.sdk.types import Task
from task_forge.cli.workon_cmd import run


class TestWorkon(CLITestCase):
    def test_workon_cmd(self):
        task = Task(id="test", title="test", priority=1)
        self.client.tasks.current.return_value = Task(title="test", priority=100)
        self.client.tasks.get.return_value = task
        args = self.args()
        args["<ID>"] = task.id
        run(args)
        self.client.tasks.get.assert_called_with(task.id)
        self.assertEqual(task.priority, 101)
