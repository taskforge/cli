"""A Github issues backed list implementation."""

import os
import re

from appdirs import user_data_dir

from github import Github, GithubObject
from task_forge.lists import TaskList as IList
from task_forge.lists.sqlite import TaskList as SQLiteList
from task_forge.models import Note, Task

PRIORITY_LABEL = re.compile("^P[0-9]{1,}$")
DEFAULT_CACHE_FILE = os.path.join(user_data_dir(), "taskforge", "github_cache.sqlite")


class TaskList(IList):
    """A list which aggregates Github issues."""

    __create_task_id_mapping_table = r"""
CREATE TABLE IF NOT EXISTS github_task_id_mapping(
    id text PRIMARY KEY,
    github_id text UNIQUE
)"""

    __create_note_id_mapping_table = r"""
CREATE TABLE IF NOT EXISTS github_note_id_mapping(
    id text PRIMARY KEY,
    github_id integer UNIQUE
)"""

    __create_task_id_mapping = r"""
INSERT INTO github_task_id_mapping
(
    id,
    github_id
)
VALUES (?, ?)
"""

    __create_note_id_mapping = r"""
INSERT INTO github_note_id_mapping
(
    id,
    github_id
)
VALUES (?, ?)
"""

    def __init__(
        self,
        base_url="https://api.github.com",
        sqlite_cache_file=DEFAULT_CACHE_FILE,
        sqlite_create_tables=False,
        create_repo=None,
        query_repo=None,
        self_assign_on_create=False,
        use_metadata_labels=False,
        username=None,
        password=None,
        access_token=None,
    ):
        self._cache_invalid = False
        self.create_repo = create_repo
        self.query_repo = query_repo
        self.self_assign_on_create = self_assign_on_create
        self.use_metadata_labels = use_metadata_labels
        self.client = Github(
            login_or_token=access_token if access_token is not None else username,
            password=password,
            base_url=base_url,
        )
        self.sqlite_cache = SQLiteList(
            file_name=sqlite_cache_file, create_tables=sqlite_create_tables
        )
        if sqlite_create_tables:
            self.sqlite_cache.conn.execute(self.__create_task_id_mapping_table)
            self.sqlite_cache.conn.execute(self.__create_note_id_mapping_table)

    def _github_issue_to_task(self, issue):
        """Convert a PyGithub issue object to a Task object."""
        priority = 1
        for label in issue.labels:
            if PRIORITY_LABEL.match(label.name):
                priority = int(label.name[1:])

        return Task(
            title=issue.title,
            id=f"{issue.repository.full_name}/{issue.number}",
            context=issue.repository.full_name,
            priority=priority,
            notes=[
                Note(comment.body, id=self._get_note_id(comment.id))
                for comment in issue.get_comments()
            ],
            created_date=issue.created_at,
            completed_date=issue.closed_at,
            body=issue.body,
        )

    def _invalidate_cache(self):
        self._cache_invalid = True

    def _get_issues(self):
        if self.query_repo is not None:
            issues = self.client.get_repo(self.query_repo).get_issues()
        else:
            issues = self.client.get_user().get_user_issues()
        return [self._github_issue_to_task(issue) for issue in issues]

    def _get_issue_by_task_id(self, task_id):
        split = task_id.split("/")
        repo = "/".join(split[:-1])
        number = int(split[-1])
        return self.client.get_repo(repo).get_issue(number)

    def _get_note_id(self, note_id):
        taskforge_id = self.sqlite_cache.conn.execute(
            "SELECT id FROM github_note_id_mapping WHERE github_id = ?", (note_id,)
        ).fetchone()
        if taskforge_id is None:
            return None
        return taskforge_id[0]

    def _get_task_id(self, task_id):
        github_id = self.sqlite_cache.conn.execute(
            "SELECT github_id FROM github_task_id_mapping WHERE id = ?", (task_id,)
        ).fetchone()
        if github_id is None:
            return task_id
        return github_id[0]

    def _cache(self):
        """Cache issues from github into SQLite."""
        if not self._cache_invalid and self.sqlite_cache.list():
            return
        self.sqlite_cache.add_multiple(self._get_issues())
        self._cache_invalid = False

    def search(self, ast):
        """Evaluate the AST and return a TaskList of matching results."""
        self._cache()
        return self.sqlite_cache.search(ast)

    def add(self, task):
        """Add a task to the TaskList."""
        kwargs = {"title": task.title}
        if self.self_assign_on_create:
            kwargs["assignee"] = self.client.get_user(self.client.get_user().login)

        if task.body:
            kwargs["body"] = task.body

        if self.use_metadata_labels:
            kwargs["labels"] = [f"P{task.priority}"]

        issue = self.client.get_repo(self.create_repo).create_issue(**kwargs)
        new_id = f"{issue.repository.full_name}/{issue.number}"
        # Create an id mapping, this is only used if a task object is
        # used in a subsequent list call without being a task
        # retrieved from this list.
        #
        # No need to commit changes since the add call to the SQLite
        # list will do that for us.
        self.sqlite_cache.conn.execute(self.__create_task_id_mapping, (task.id, new_id))
        task.id = new_id
        self.sqlite_cache.add(task)

    def add_multiple(self, tasks):
        """Add multiple tasks to the TaskList.

        Ideally should be more efficient resource utilization.
        """
        for task in tasks:
            self.add(task)

    def list(self):
        """Return a python list of the Task in this TaskList."""
        return self._get_issues()

    def find_by_id(self, task_id):
        """Find a task by id."""
        return self._github_issue_to_task(
            self._get_issue_by_task_id(self._get_task_id(task_id))
        )

    def current(self):
        """Return the current task.

        The current task is defined as the oldest uncompleted
        task in the TaskList.
        """
        self._cache()
        return self.sqlite_cache.current()

    def complete(self, task_id):
        """Complete a task by id."""
        self._cache()
        task_id = self._get_task_id(task_id)
        self.sqlite_cache.complete(task_id)
        issue = self._get_issue_by_task_id(task_id)
        issue.edit(state="closed")

    def update(self, task):
        """Update a task in the list.

        The original is retrieved using the id of the given task.
        """
        self._cache()
        self.sqlite_cache.update(task)
        task_id = self._get_task_id(task.id)
        issue = self._get_issue_by_task_id(task_id)
        if self.use_metadata_labels:
            new_labels = [
                label for label in issue.labels if not PRIORITY_LABEL.match(label.name)
            ]
            new_labels.append(f"P{task.priority}")
        else:
            new_labels = issue.labels

        issue.edit(
            title=task.title,
            body=task.body if task.body is not None else GithubObject.NotSet,
            labels=new_labels,
        )

    def add_note(self, task_id, note):
        """Add note to a task by id."""
        task_id = self._get_task_id(task_id)
        issue = self._get_issue_by_task_id(task_id)
        comment = issue.create_comment(note.body)
        self.sqlite_cache.conn.execute(
            self.__create_note_id_mapping, (note.id, comment.id)
        )
        self._invalidate_cache()
