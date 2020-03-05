"""Provides a List implementation for talking to a Taskforge server."""

from task_forge.lists import InvalidConfigError
from task_forge.lists import List as IList
from task_forge.lists import NotFoundError
from task_forge.models import Task

import requests


class List(IList):
    """An base class that all list implementations must derive from."""

    def __init__(self, host="localhost", port=8000):
        self.addr = "http://{host}:{port}".format(host=host, port=port)
        self.session = requests.Session()
        self.session.headers.update(
            {"content-type": "application/json", "accepts": "application/json"}
        )

    def __request(self, endpoint, method="GET", json=None, params=None):
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

    def add(self, task):
        """Add a task to the List."""
        return self.__request("/tasks", method="POST", json=task.to_json())

    def add_multiple(self, tasks):
        """Add multiple tasks to the List.

        Ideally should be more efficient resource utilization.
        """
        return self.__request(
            "/tasks", method="POST", json=[task.to_json() for task in tasks]
        )

    def list(self):
        """Return a python list of the Task in this List."""
        return self.__request("/tasks")

    def find_by_id(self, task_id):
        """Find a task by id."""
        return self.__request("/tasks/{}".format(task_id))

    def current(self):
        """Return the current task.

        The current task is defined as the oldest uncompleted
        task in the List.
        """
        return self.__request("/tasks/current")

    def complete(self, task_id):
        """Complete a task by id."""
        return self.__request("/tasks/{}/complete".format(task_id), method="PUT")

    def update(self, task):
        """Update a task in the list.

        The original is retrieved using the id of the given task.
        """
        return self.__request("/tasks", method="PUT", json=task.to_json())

    def add_note(self, task_id, note):
        """Add note to a task by id."""
        return self.__request(
            "/tasks/{}/note".format(task_id), method="POST", json=note.to_json()
        )

    def search(self, ast):
        """Evaluate the AST and return a List of matching results."""
        return self.__request("/tasks", params={"query": str(ast)})
