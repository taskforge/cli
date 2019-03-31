"""Test global list constructs like errors."""


import unittest

from task_forge.lists import NotFoundError


class TestNotFoundError(unittest.TestCase):
    def test_no_id(self):
        exc = NotFoundError()
        self.assertEqual(repr(exc), "no task that matched query found")

    def test_with_id(self):
        exc = NotFoundError(task_id="blah")
        self.assertEqual(repr(exc), "no task with id blah exists")
