from tests.utils import CLITestCase
from task_forge.sdk.types import Task
from task_forge.cli.complete_cmd import run


class TestComplete(CLITestCase):
    def test_complete_cmd(self):
        task = Task(id="test", title="test", priority=1)
        args = self.args()
        args["<ID>"] = [task.id]
        run(args)
        self.client.tasks.complete_by_id.assert_called_with(task.id)

    def test_completes_current_with_no_ids(self):
        task = Task(id="test", title="test", priority=1)
        self.client.tasks.current.return_value = task
        args = self.args()
        run(args)
        self.client.tasks.complete_by_id.assert_called_with(task.id)
