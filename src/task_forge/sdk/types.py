"""
Concrete types for interacting with the Taskforge server.

The SDK handles serialization and deserialization of server responses. All callers of the SDK should
be using these concrete types.
"""

from uuid import UUID
from typing import Optional
from datetime import datetime
from dataclasses import field, dataclass


@dataclass
class Task:
    """
    Basic task unit in Taskforge.

    This represents a unit of work a User needs to do.
    """

    title: str

    id: UUID = field(default=None)

    owner: UUID = field(default=None)
    context: UUID = field(default=None)
    source: UUID = field(default=None)

    body: str = field(default=None)
    priority: int = field(default=None)

    created_date: datetime = field(default=None)
    completed_date: datetime = field(default=None)


@dataclass
class Comment:
    """Comment type, usually tied to a Task."""

    id: UUID
    object_id: UUID
    author: UUID
    body: str


@dataclass
class Source:
    """
    A Task Source.

    This indicates where a Task came from, for example Github, JIRA, etc. The default is Taskforge.
    """

    id: UUID
    name: str


@dataclass
class Context:
    """
    A Task Context.

    This is usually analogous to "Projects" in other task manage applications. This is a
    user-defined container for grouping tasks. The default is "default"
    """

    id: UUID
    name: str
    owner: UUID


@dataclass
class Profile:
    """Profile information for a user, contains their settings."""

    avatar: str


@dataclass
class User:
    """A Taskforge User."""

    username: str
    email: str
    id: Optional[int] = field(default=None)
    password: Optional[str] = field(default=None)
    profile: Optional[Profile] = field(default=None)
