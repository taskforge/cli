"""Provides a List implementation for talking to a Taskforge server."""

from task_forge.lists import InvalidConfigError
from task_forge.lists import List as IList
from task_forge.lists import NotFoundError
from task_forge.server.client import Client
from task_forge.server.server import STATUS_FAILURE
from task_forge.task import Task


class List(IList):
    """An base class that all list implementations must derive from."""

    def __init__(self,
                 unix_socket=None,
                 host=None,
                 port=None,
                 secret_file=None):
        if unix_socket is not None:
            self.addr = unix_socket
        elif host is not None and port is not None:
            self.addr = f'{host}:{port}'
        else:
            raise InvalidConfigError(
                'must provide a unix_socket or host port combination')

        self.secret_file = secret_file
        self.client = Client(self.addr)
        self.client.start()

    def __send(self, msg):
        """Send msg to server, handle the errors if any returned."""
        self.client.send_message(msg)

        response = self.client.recv_message()
        if response['status'] == STATUS_FAILURE and 'no task' in response[
                'message']:
            raise NotFoundError(response['message'])

        if response['status'] == STATUS_FAILURE:
            raise Exception(response['message'])

        payload = response.get('payload')
        if isinstance(payload, dict):
            return Task.from_dict(payload)

        if isinstance(payload, list):
            return [Task.from_dict(task) for task in payload]

        return None

    def add(self, task):
        """Add a task to the List."""
        return self.__send({'method': 'add', 'payload': task.to_json()})

    def add_multiple(self, tasks):
        """Add multiple tasks to the List.

        Ideally should be more efficient resource utilization.
        """
        return self.__send({
            'method': 'add_multiple',
            'payload': [task.to_json() for task in tasks]
        })

    def list(self):
        """Return a python list of the Task in this List."""
        return self.__send({'method': 'list'})

    def find_by_id(self, task_id):
        """Find a task by id."""
        return self.__send({
            'method': 'find_by_id',
            'payload': {
                'task_id': task_id
            }
        })

    def current(self):
        """Return the current task.

        The current task is defined as the oldest uncompleted
        task in the List.
        """
        return self.__send({'method': 'current'})

    def complete(self, task_id):
        """Complete a task by id."""
        return self.__send({
            'method': 'complete',
            'payload': {
                'task_id': task_id
            }
        })

    def update(self, task):
        """Update a task in the list.

        The original is retrieved using the id of the given task.
        """
        return self.__send({'method': 'update', 'payload': task.to_json()})

    def add_note(self, task_id, note):
        """Add note to a task by id."""
        return self.__send({
            'method': 'add_note',
            'payload': {
                'task_id': task_id,
                'note': note.to_json()
            }
        })

    def search(self, ast):
        """Evaluate the AST and return a List of matching results."""
        return self.__send({'method': 'search', 'payload': ast.to_dict()})
