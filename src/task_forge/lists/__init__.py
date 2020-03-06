"""Contains the TaskList abstract base class as well as error types."""

from abc import ABC, abstractmethod
from typing import Any, List, Optional

from task_forge.models import Note, Task
from task_forge.ql.ast import AST


class InvalidConfigError(Exception):
    """Indicate an invalid configuration was provided to the TaskList."""


class NotFoundError(Exception):
    """Indicate a task with the given id does not exist."""

    def __init__(self, task_id: Optional[str] = None):
        """Return a NotFoundError for id."""
        super().__init__()
        self.task_id = task_id

    def __repr__(self) -> str:
        """Return a human friendly error message."""
        if self.task_id is not None:
            return f"no task with id {self.task_id} exists"
        return "no task that matched query found"


class TaskList(ABC):
    """An base class that all list implementations must derive from."""

    @abstractmethod
    def search(self, ast: AST) -> List[Task]:
        """Evaluate the AST and return a List of matching results."""
        raise NotImplementedError

    @abstractmethod
    def add(self, task: Task) -> Any:
        """Add a task to the TaskList."""
        raise NotImplementedError

    @abstractmethod
    def add_multiple(self, tasks: List[Task]) -> Any:
        """Add multiple tasks to the TaskList.

        Ideally should be more efficient resource utilization.
        """
        raise NotImplementedError

    @abstractmethod
    def list(self) -> List[Task]:
        """Return a python list of the Task in this TaskList."""
        raise NotImplementedError

    @abstractmethod
    def find_by_id(self, task_id: str) -> Task:
        """Find a task by id."""
        raise NotImplementedError

    @abstractmethod
    def current(self) -> Task:
        """Return the current task.

        The current task is defined as the oldest uncompleted
        task in the TaskList.
        """
        raise NotImplementedError

    @abstractmethod
    def complete(self, task_id: str) -> Any:
        """Complete a task by id."""
        raise NotImplementedError

    @abstractmethod
    def update(self, task: Task) -> Any:
        """Update a task in the list.

        The original is retrived using the id of the given task.
        """
        raise NotImplementedError

    @abstractmethod
    def add_note(self, task_id: str, note: Note) -> Any:
        """Add note to a task by id."""
        raise NotImplementedError
