"""Provides a TaskList implementation for talking to a Taskforge server."""

from typing import Any, Dict, List, Union, cast

import requests

from task_forge.lists import InvalidConfigError, NotFoundError
from task_forge.lists import TaskList as IList
from task_forge.models import Note, Task
from task_forge.ql.ast import AST


class TaskList(IList):
    """An base class that all list implementations must derive from."""

    def __init__(self, host: str = "localhost", port: int = 8000):
        self.addr = "http://{host}:{port}".format(host=host, port=port)
        self.session = requests.Session()
        self.session.headers.update(
            {"content-type": "application/json", "accepts": "application/json"}
        )

    def __request(
        self,
        endpoint: str,
        method: str = "GET",
        json: Union[Dict[str, Any], List[Dict[str, Any]]] = None,
        params: Dict[str, Any] = None,
    ) -> Union[Task, List[Task], None]:
        """Send msg to server, handle the errors if any returned."""
        if params is None:
            params = {}

        req = requests.Request(
            method, "{}{}".format(self.addr, endpoint), json=json, params=params,
        )
        res = self.session.send(self.session.prepare_request(req))
        if res.status_code == 404:
            raise NotFoundError
        elif res.status_code != 200:
            raise Exception(res.text)
        else:
            jsn = res.json()
            if isinstance(jsn, list):
                return [Task.from_dict(j) for j in jsn]
            elif jsn.get("message") == "success":
                return None
            else:
                return Task.from_dict(jsn)

    def add(self, task: Task) -> Any:
        """Add a task to the TaskList."""
        return self.__request("/tasks", method="POST", json=task.to_json())

    def add_multiple(self, tasks: List[Task]) -> Any:
        """Add multiple tasks to the TaskList.

        Ideally should be more efficient resource utilization.
        """
        return self.__request(
            "/tasks", method="POST", json=[task.to_json() for task in tasks]
        )

    def list(self) -> Any:
        """Return a python list of the Task in this TaskList."""
        return self.__request("/tasks")

    def find_by_id(self, task_id: str) -> Task:
        """Find a task by id."""
        return cast(Task, self.__request("/tasks/{}".format(task_id)))

    def current(self) -> Task:
        """Return the current task.

        The current task is defined as the oldest uncompleted
        task in the TaskList.
        """
        return cast(Task, self.__request("/tasks/current"))

    def complete(self, task_id: str) -> Any:
        """Complete a task by id."""
        return self.__request("/tasks/{}/complete".format(task_id), method="PUT")

    def update(self, task: Task) -> Any:
        """Update a task in the list.

        The original is retrieved using the id of the given task.
        """
        return self.__request("/tasks", method="PUT", json=task.to_json())

    def add_note(self, task_id: str, note: Note) -> Any:
        """Add note to a task by id."""
        return self.__request(
            "/tasks/{}/note".format(task_id), method="POST", json=note.to_json()
        )

    def search(self, ast: AST) -> List[Task]:
        """Evaluate the AST and return a List of matching results."""
        return cast(List[Task], self.__request("/tasks", params={"query": str(ast)}))
