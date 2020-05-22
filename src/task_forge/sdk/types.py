from typing import Optional
from dataclasses import dataclass, field
from uuid import UUID
from datetime import datetime


@dataclass
class Task:
    id: UUID

    owner: UUID
    context: UUID
    source: UUID

    title: str
    body: str
    priority: int

    created_date: datetime
    completed_date: datetime


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
