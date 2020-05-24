"""
Error types returned by objects in the SDK.

These types are meant to make error handling more expressive without exposing low-level details of
interacting with the server.
"""


class Unauthorized(Exception):
    """The current users is not allowed to perform the action or is not logged in."""


class NotFound(Exception):
    """Object was not found, either ID is incorrect or no objects exist."""


class BadRequest(Exception):
    """Something went horribly wrong, this should indicate a bug in the SDK."""
