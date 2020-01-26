"""Provides the Task and Note classes used throughout Taskforge."""

from typing import List, Union
from datetime import datetime

from bson.objectid import ObjectId

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def date_to_string(dateobj):
    """Format dateobj using the standard DATE_FORMAT."""
    return dateobj.strftime(DATE_FORMAT)


class Model:
    """Common base functionality for all Models in task forge."""

    id = None
    dict_blacklist = []
    transforms = {
        "created_date": date_to_string,
        "completed_date": date_to_string,
        "id": str,
    }

    def __init__(self, id: Union[str, ObjectId, None] = None):
        if id is None:
            id = ObjectId()
        elif isinstance(id, str):
            id = ObjectId(id)

        self.id = id

    def __repr__(self):
        """Return a simple string of Model subclass name and id."""
        return f"{self.__class__.__name__}({self.id})"

    def __eq__(self, other):
        """Return True if self and other have the same id."""
        if not hasattr(other, "id"):
            return False

        return str(self.id) == str(other.id)

    def to_json(self):
        """
        Convert this Model object into a dictionary with JSON incompatible types serialized.

        .. note:: For richer data types use :meth:`Note.to_dict` instead.
        """
        return {
            key: self.transforms.get(key, lambda x: x)(value)
            for key, value in self.__dict__.items()
            if not key.startswith("_") and key not in self.dict_blacklist
        }

    @classmethod
    def from_dict(cls, dictionary):
        """
        Create a Model instance from a dictionary.

        Handles JSON-deserialized types appropriately. i.e. datetime fields will
        be properly parsed if in string form.
        """
        return cls(**dictionary)

    def to_dict(self):
        """Transform this model into a dictionary for easy use to/from BSON."""
        return {
            key: value
            for key, value in self.__dict__.items()
            if not key.startswith("_") and key not in self.dict_blacklist
        }


# We only enable the User model when bcrypt is installed, it is only
# installed for task_forge[server]
try:
    import bcrypt

    class User(Model):
        """A Taskforge user"""

        def __init__(
            self,
            username: str,
            email: str,
            id: Union[str, ObjectId, None] = None,
            password: str = None,
        ):
            super().__init__(id=id)
            self.username = username
            self.email = email
            self.password = password

        @classmethod
        def new(cls, username: str, email: str, password: str) -> User:
            """Create a new user, secures password using bcrypt."""
            bcrypted_pass = bcrypt.hashpw(password, bcrypt.gensalt())
            user = cls(id=None, username=username, email=email, password=bcrypted_pass,)
            return user

        def update_password(self, password: str):
            """Update the password of this user hashing password with bcrypt."""
            bcrypted_pass = bcrypt.hashpw(password, bcrypt.gensalt())
            self.password = bcrypted_pass


except ImportError:
    pass


class Note(Model):
    """
    A note or 'comment' on a task.

    A basic note instantiation only requires the body field. All other fields
    are optional and id should not be set unless instantiating from an existing
    Note.

    :param body: The body of the note.
    :type body: str
    :param id: The unique id for this note. If None this will be generated using
               :func:`uuid.uuid4`. Should only be provided if deserializing an
               existing :class:`Note`.
    :type id: Optional[str].
    :param created_date: The created_date for this note. If None this
                will be generated using :meth:`datetime.datetime.now`.
                Should only be provided if deserializing an existing
               :class:`Note`.
    :type created_date: Optional[datetime.datetime].
    """

    def __init__(
        self,
        author: str,
        body: str,
        id: Union[str, ObjectId, None] = None,
        created_date: Union[datetime, None] = None,
    ):
        """Create a note with body."""
        if created_date is None:
            created_date = datetime.now()
        elif isinstance(created_date, str):
            created_date = datetime.strptime(created_date, DATE_FORMAT)

        super().__init__(id=id)
        self.author = author
        self.body = body
        self.created_date = created_date

    def to_dict(self):
        """Convert this note object into a dictionary."""
        return {
            "id": self.id,
            "author": self.author,
            "body": self.body,
            "created_date": self.created_date,
        }


class Task(Model):
    """
    Represents a task in a Task List.

    This class is the basic unit in Taskforge and is central to all
    functionality.

    The basic instantiation of a Task only requires a title and will fill out
    any required metadata with default values:

    >>> from task_forge.task import Task
    >>> Task('An example Task')
    Task(c659687d9ad54b308a258850a5a06af1)

    All fields available for a task and their defaults are:

    :param title: The title or 'summary' of a task.
    :type title: str
    :param id: The unique id for this task. If None this will be generated using
               :func:`uuid.uuid4`. Should only be provided if deserializing an
               existing :class:`Task`.
    :type id: Optional[str].
    :param created_date: A datetime object representing when this task was
                         created. If not provided defaults to
                         :meth:`datetime.now`. Should only be provided if
                         deserializing an existing :class:`Task`.
    :type created_date: Optional[datetime.datetime]
    :param body: **Default** ("") - The body or 'description' of a task.
    :type body: str
    :param context: **Default** ("default") - The 'list' this task belongs to.
                    Common values are work, personal etc.
    :type context: str
    :param priority: **Default** (1) - The priority of this task, this is the
                     primary sorting criteria for tasks.
    :type priority: int
    :param notes: **Default** (None) - A list of Note objects to for this task.
    :type notes: List[Note]
    :param completed_date: **Default** (None) - A datetime object representing
                           when this task was completed.
    :type completed_date: datetime.datetime
    """

    def __init__(
        self,
        owner: str,
        title: str,
        id: Union[str, ObjectId, None] = None,
        context: str = "default",
        priority: int = 1,
        notes: Union[List[Note], None] = None,
        created_date: Union[str, datetime, None] = None,
        completed_date: Union[str, datetime, None] = None,
        body: str = "",
    ):
        """
        Create a Task with the given fields, defaulting appropriate metadata.

        All other fields are optional and id should not be set unless
        instantiating from an existing task.
        """
        if created_date is None:
            created_date = datetime.now()
        elif isinstance(created_date, str):
            created_date = datetime.strptime(created_date, DATE_FORMAT)

        if isinstance(completed_date, str):
            completed_date = datetime.strptime(completed_date, DATE_FORMAT)

        if notes is None:
            notes = []

        super().__init__(id=id)
        self.title = title
        self.context = context
        self.priority = priority
        self.body = body
        self.created_date = created_date
        self.completed_date = completed_date
        self.notes = notes
        self.owner = owner

    def __lt__(self, other):
        """Sorts highest priority first then oldest first."""
        if self.priority > other.priority:
            return True

        if self.priority < other.priority:
            return False

        return self.created_date < other.created_date

    @classmethod
    def from_dict(cls, dictionary):
        """
        Create a Task from a dictionary representation.

        Handles JSON-deserialized types appropriately. i.e. datetime fields will
        be properly parsed if in string form.
        """
        dictionary["notes"] = [
            Note.from_dict(note) for note in dictionary.get("notes", [])
        ]

        return cls(**dictionary)

    def to_json(self):
        """
        Convert to a dictionary which has JSON incompatible types properly serialized.

        .. note:: For richer data types use :meth:`Task.to_dict` instead.
        """
        j = {
            "id": str(self.id),
            "title": self.title,
            "body": self.body,
            "context": self.context,
            "priority": self.priority,
            "owner": self.owner,
            "created_date": date_to_string(self.created_date),
            "notes": [n.to_json() for n in self.notes],
        }

        if self.completed_date:
            j["completed_date"] = date_to_string(self.completed_date)

        return j

    def to_dict(self):
        """Convert this task object into a dictionary."""
        return {
            "id": self.id,
            "title": self.title,
            "body": self.body,
            "context": self.context,
            "priority": self.priority,
            "owner": self.owner,
            "created_date": self.created_date,
            "completed_date": self.completed_date,
            "notes": [n.to_dict() for n in self.notes],
        }

    def complete(self):
        """
        Complete this task.

        Sets self.completed_date using :meth:`datetime.datetime.now`.
        """
        self.completed_date = datetime.now()
        return self

    def is_complete(self):
        """Indicate whether this task is completed or not."""
        return self.is_completed()

    def is_completed(self):
        """Indicate whether this task is completed or not."""
        return self.completed_date is not None
