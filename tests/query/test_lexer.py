# We're testing low-level Lexer methods here so need to use protected
# methods
# pylint: disable=protected-access
import pytest

from task_forge.ql.lexer import Lexer
from task_forge.ql.tokens import Token, Type


@pytest.mark.parametrize(
    "query,expected",
    [
        ("milk and cookies", [Token("milk"), Token("and"), Token("cookies")]),
        ("completed = false", [Token("completed"), Token("="), Token("false")]),
        ("completed ^= false", [Token("completed"), Token("^="), Token("false")]),
        ("completed != false", [Token("completed"), Token("!="), Token("false")]),
        (
            "foo = 'unclosed string",
            [
                Token("foo"),
                Token("="),
                Token("unexpected eof: no closing quote", token_type=Type.UNEXPECTED),
            ],
        ),
        ("completed ^^ false", [Token("completed"), Token("^^"), Token("false")]),
        (
            "(priority > 0)",
            [Token("("), Token("priority"), Token(">"), Token("0"), Token(")")],
        ),
        (
            "milk -and cookies",
            [Token("milk"), Token("and", token_type=Type.STRING), Token("cookies")],
        ),
        (
            '(priority > 5 and title ^ "take out the trash") or '
            '(context = "work" and (priority >= 2 or ("my little pony")))',
            [
                Token("("),
                Token("priority"),
                Token(">"),
                Token("5"),
                Token("and"),
                Token("title"),
                Token("^"),
                Token("take out the trash"),
                Token(")"),
                Token("or"),
                Token("("),
                Token("context"),
                Token("="),
                Token("work"),
                Token("and"),
                Token("("),
                Token("priority"),
                Token(">="),
                Token("2"),
                Token("or"),
                Token("("),
                Token("my little pony"),
                Token(")"),
                Token(")"),
                Token(")"),
            ],
        ),
    ],
)
def test_lexer(query, expected):
    lex = Lexer(query)
    tokens = list(lex)
    assert tokens == expected
    assert len(tokens) == len(expected)


def test_lexer_peek_over_end_is_safe():
    lex = Lexer("")
    assert lex._peek_char() == ""
    lex._read_char()
    assert lex._peek_char() == ""


@pytest.mark.slow
@pytest.mark.benchmark
@pytest.mark.parametrize(
    "query",
    [
        ("milk and cookies",),
        ("milk -and cookies",),
        ("completed = false",),
        (
            "(priority > 5 and title ^ 'take out the trash') or "
            '(context = "work" and (priority >= 2 or ("my little pony")))',
        ),
    ],
)
def test_lexer_performance(query, benchmark):
    """Benchmark the performance of various queries."""

    @benchmark
    def parse_query():  # pylint: disable=unused-variable
        """Benchmark query parsing"""
        lexer = Lexer(query)
        list(lexer)
