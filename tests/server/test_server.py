"""Test server functions."""


from unittest.mock import Mock

import pytest

from task_forge.ql.ast import AST
from task_forge.ql.parser import Parser
from task_forge.server.server import dispatch
from task_forge.task import Task


@pytest.mark.parametrize(
    "message,called,called_with",
    [
        ({"method": "add", "payload": {"title": "a mock task"}}, "add", None),
        (
            {"method": "add_multiple", "payload": [{"title": "a mock task"}]},
            "add_multiple",
            None,
        ),
        ({"method": "list"}, "list", None),
        (
            {"method": "find_by_id", "payload": {"id": "testid"}},
            "find_by_id",
            {"id": "testid"},
        ),
        ({"method": "current"}, "current", None),
        (
            {"method": "complete", "payload": {"id": "testid"}},
            "complete",
            {"id": "testid"},
        ),
        (
            {"method": "update", "payload": {"id": "testid", "title": "updated"}},
            "update",
            Task(id="testid", title="updated"),
        ),
        (
            {
                "method": "add_note",
                "payload": {"task_id": "testid", "note": {"body": "a note"}},
            },
            "add_note",
            None,
        ),
        (
            {
                "method": "search",
                "payload": {
                    "expression": {
                        "left": {
                            "token": {"token_type": "STRING", "literal": "completed"},
                            "value": "completed",
                        },
                        "right": {
                            "token": {"token_type": "BOOLEAN", "literal": "false"},
                            "value": False,
                        },
                        "operator": {"token_type": "EQ", "literal": "="},
                    }
                },
            },
            "search",
            AST.from_dict(
                {
                    "expression": {
                        "left": {
                            "token": {"token_type": "STRING", "literal": "completed"},
                            "value": "completed",
                        },
                        "right": {
                            "token": {"token_type": "BOOLEAN", "literal": "false"},
                            "value": False,
                        },
                        "operator": {"token_type": "EQ", "literal": "="},
                    }
                }
            ),
        ),
        (
            {"method": "query", "payload": {"query": "completed = false"}},
            "search",
            Parser("completed = false").parse(),
        ),
    ],
)
def test_dispatch(message, called, called_with):
    """Test various dispatch methods."""
    mock = Mock()
    result = dispatch(mock, message)
    assert result["status"] == "success"

    attr = getattr(mock, called)
    assert attr
    attr.assert_called()
    if isinstance(called_with, dict):
        attr.assert_called_with(**called_with)
    elif called_with is not None:
        attr.assert_called_with(called_with)


def test_dispatch_ping():
    res = dispatch(None, {"method": "ping"})
    assert {"status": "success", "payload": {"message": "pong"}} == res
