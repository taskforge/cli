from typing import Optional
from dataclasses import dataclass, field
from uuid import UUID
from datetime import datetime


@dataclass
class Task:
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
    id: UUID
    object_id: UUID
    author: UUID
    body: str


@dataclass
class Source:
    id: UUID
    name: str


@dataclass
class Context:
    id: UUID
    name: str
    owner: UUID


@dataclass
class Profile:
    avatar: str


@dataclass
class User:
    username: str
    email: str
    id: Optional[int] = field(default=None)
    password: Optional[str] = field(default=None)
    profile: Optional[Profile] = field(default=None)
