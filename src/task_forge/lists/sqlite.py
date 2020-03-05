"""Provides a SQLite 3 backed list implementation."""

import os
import sqlite3

from datetime import datetime
from typing import Any, Dict, List, Tuple
from uuid import uuid1

from task_forge.models import Note, Task
from task_forge.ql.ast import AST, Expression
from task_forge.ql.tokens import Type

from . import InvalidConfigError, NotFoundError
from . import TaskList as AList

QueryContext = Tuple[str, Dict[str, Any]]


class TaskList(AList):
    """A SQLite 3 backed list implementation."""

    __create_task_table = r"""
CREATE TABLE IF NOT EXISTS tasks(
    id text PRIMARY KEY,
    title text,
    body text,
    context text,
    priority integer,
    created_date integer,
    completed_date integer
)"""

    __create_note_table = r"""
CREATE TABLE IF NOT EXISTS notes(
    task_id text,
    id text,
    body text,
    created_date integer,
    FOREIGN KEY(task_id) REFERENCES tasks(task_id)
)"""

    __insert = r"""
INSERT INTO tasks
(
    id,
    title,
    body,
    context,
    priority,
    created_date,
    completed_date
)
VALUES (?,?,?,?,?,?,?)
"""

    __select = r"""
SELECT id, title, body, context, priority, created_date, completed_date
FROM tasks
"""

    def __init__(
        self, directory: str = "", file_name: str = "", create_tables: bool = False
    ):
        """Create a TaskList from the given configuration.

        Either directory or file_name should be provided. Raises
        InvalidConfigError if neither are provided. If both are
        provided then file_name is used.

        create_tables forces the table creation query to
        run. Otherwise will create tables if the resulting sqlite db
        file does not already exist.
        """
        if not file_name and not directory:
            raise InvalidConfigError("either directory or file_name must be provided")

        if not file_name:
            directory = directory.replace(
                "~", os.getenv("HOME", os.getenv("APPDATALOCAL", ""))
            )
            file_name = os.path.join(directory, "tasks.sqlite3")

        parent = os.path.dirname(file_name)
        if not os.path.isdir(parent):
            os.makedirs(parent)

        if not os.path.isfile(file_name):
            create_tables = True

        self.conn = sqlite3.connect(file_name)
        if create_tables:
            self.conn.execute(self.__create_task_table)
            self.conn.execute(self.__create_note_table)

    @staticmethod
    def note_from_row(row: Tuple[Any, Any, Any]) -> Note:
        """Convert a SQL row tuple back into a Note object."""
        return Note(id=row[0], body=row[1], created_date=datetime.fromtimestamp(row[2]))

    @staticmethod
    def task_to_row(task: Task) -> Tuple[str, str, str, str, int, float, float]:
        """Convert a task to a tuple with the correct column order."""
        return (
            task.id,
            task.title,
            task.body,
            task.context,
            task.priority,
            task.created_date.timestamp(),
            task.completed_date.timestamp() if task.completed_date else 0,
        )

    def task_from_row(self, row: Tuple[Any, Any, Any, Any, Any, Any, Any]) -> Task:
        """Convert a SQL row tuple back into a Task object.

        Raises a NotFoundError if row is None
        """
        if row is None:
            raise NotFoundError

        if len(row) != 7:
            raise NotFoundError

        return Task(
            id=row[0],
            title=row[1],
            body=row[2],
            context=row[3],
            priority=row[4],
            created_date=datetime.fromtimestamp(row[5]),
            completed_date=datetime.fromtimestamp(row[6]) if row[6] else None,
            notes=self.__get_notes(row[0]),
        )

    def __get_notes(  # pylint: disable=invalid-name
        self, id: str  # pylint: disable=redefined-builtin
    ) -> List[Note]:
        return [
            TaskList.note_from_row(row)
            for row in self.conn.execute(
                "SELECT id, body, created_date FROM notes WHERE task_id = ?", (id,)
            )
        ]

    def add(self, task: Task) -> None:
        """Add a task to the TaskList."""
        self.conn.execute(self.__insert, TaskList.task_to_row(task))
        self.conn.commit()

    def add_multiple(self, tasks: List[Task]) -> None:
        """Add multiple tasks to the TaskList."""
        self.conn.executemany(
            self.__insert, [TaskList.task_to_row(task) for task in tasks]
        )
        self.conn.commit()

    def list(self) -> List[Task]:
        """Return a python list of the Task in this TaskList."""
        return [self.task_from_row(row) for row in self.conn.execute(self.__select)]

    def find_by_id(self, task_id: str) -> Task:
        """Find a task by task_id."""
        cursor = self.conn.execute(self.__select + "WHERE id = ?", (task_id,))
        return self.task_from_row(cursor.fetchone())

    def current(self) -> Task:
        """Return the current task."""
        return self.task_from_row(
            self.conn.execute(
                self.__select
                + "WHERE completed_date = 0 "
                + "ORDER BY priority DESC, created_date ASC"
            ).fetchone()
        )

    def complete(self, task_id: str) -> None:
        """Complete a task by task_id."""
        self.conn.execute(
            "UPDATE tasks SET completed_date = ? WHERE id = ?",
            (datetime.now().timestamp(), task_id),
        )
        self.conn.commit()

    def update(self, task: Task) -> None:
        """Update a task in the list.

        The original is retrieved using the id of the given task.
        """
        task_row = TaskList.task_to_row(task)
        # move id to the end
        update_tuple = (
            task_row[1],
            task_row[2],
            task_row[3],
            task_row[4],
            task_row[5],
            task_row[6],
            task_row[0],
        )
        self.conn.execute(
            r"""
UPDATE tasks
SET
    title = ?,
    body = ?,
    context = ?,
    priority = ?,
    created_date = ?,
    completed_date = ?
WHERE id = ?
""",
            update_tuple,
        )
        self.conn.commit()

    def add_note(self, task_id: str, note: Note) -> None:
        """Add note to a task by task_id."""
        self.conn.execute(
            "INSERT INTO notes (task_id, id, body, created_date) VALUES (?, ?, ?, ?)",
            (task_id, note.id, note.body, note.created_date.timestamp()),
        )
        self.conn.commit()

    def search(self, ast: AST) -> List[Task]:
        """Evaluate the AST and return a List of matching results."""
        where, values = TaskList.__eval(ast.expression)
        return [
            self.task_from_row(task)
            for task in self.conn.execute(self.__select + "WHERE " + where, values)
        ]

    @staticmethod
    def __eval(expression: Expression) -> QueryContext:
        """Evaluate expression returning a where clause and a dictionary of values."""
        if expression.is_str_literal():
            return TaskList.__eval_str_literal(expression)

        if expression.is_infix():
            return TaskList.__eval_infix(expression)

        return ("", {})

    @staticmethod
    def __eval_str_literal(expression: Expression) -> QueryContext:
        """Evaluate a string literal query."""
        ident = uuid1().hex
        return (
            f"(title LIKE :{ident} OR body LIKE :{ident})",
            {ident: f"%{expression.value}%"},
        )

    @staticmethod
    def __eval_infix(expression: Expression) -> QueryContext:
        """Evaluate an infix expression."""
        assert expression.left is not None
        assert expression.right is not None
        assert expression.operator is not None

        if expression.is_logical_infix():
            left, left_values = TaskList.__eval(expression.left)
            right, right_values = TaskList.__eval(expression.right)
            return (
                f"({left}) {expression.operator.literal} ({right})",
                {**left_values, **right_values},
            )

        ident = uuid1().hex
        if (
            expression.left.value == "completed"
            and expression.right.is_boolean_literal()
        ):
            return (
                "completed_date != 0"
                if expression.right.value
                else "completed_date = 0",
                {},
            )

        if expression.operator.token_type == Type.LIKE:
            return (
                f"({expression.left.value} LIKE :{ident})",
                {ident: f"%{expression.right.value}%"},
            )

        # Type ignore because we know that if we got here the right value is valid.
        return (
            f"({expression.left.value} {expression.operator.literal} :{ident})",
            {ident: expression.right.value},  # type: ignore
        )
