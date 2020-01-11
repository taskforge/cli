import pytest

from task_forge.ql.ast import AST, Expression
from task_forge.ql.parser import Parser
from task_forge.ql.tokens import Token


@pytest.mark.parametrize(
    "query,ast",
    [
        (
            "milk and cookies",
            AST(
                Expression(
                    Token("and"),
                    left=Expression(Token("milk")),
                    right=Expression(Token("cookies")),
                )
            ),
        ),
        (
            "completed = false",
            AST(
                Expression(
                    Token("="),
                    left=Expression(Token("completed")),
                    right=Expression(Token("false")),
                )
            ),
        ),
        ("milk -and cookies", AST(Expression(Token("milk and cookies")))),
        (
            "(priority > 5 and title ^ 'take out the trash') or "
            '(context = "work" and (priority >= 2 or ("my little pony")))',
            AST(
                Expression(
                    Token("or"),
                    right=Expression(
                        Token("and"),
                        left=Expression(
                            Token("="),
                            left=Expression(Token("context")),
                            right=Expression(Token("work")),
                        ),
                        right=Expression(
                            Token("or"),
                            left=Expression(
                                Token(">="),
                                left=Expression(Token("priority")),
                                right=Expression(Token("2")),
                            ),
                            right=Expression(Token("my little pony")),
                        ),
                    ),
                    left=Expression(
                        Token("and"),
                        right=Expression(
                            Token("~"),
                            right=Expression(Token("take out the trash")),
                            left=Expression(Token("title")),
                        ),
                        left=Expression(
                            Token(">"),
                            left=Expression(Token("priority")),
                            right=Expression(Token("5")),
                        ),
                    ),
                )
            ),
        ),
        (
            "completed = false",
            AST(
                Expression(
                    Token("="),
                    left=Expression(Token("completed")),
                    right=Expression(Token("false")),
                )
            ),
        ),
    ],
)
def test_parser(query, ast):
    parser = Parser(query)
    assert parser.parse() == ast


def test_parser_no_prefix_fun_raises_parse_error():
    parser = Parser("'unclosed string")
    try:
        parser.parse()
    except ParseError as e:
        assert str(e) == "no prefix function for: Type.UNEXPECTED"


def test_parser_empty_query_raises_stopiteration():
    try:
        parser = Parser("")
        assert False
    except StopIteration:
        pass


def test_parser_left_side_comparison_not_valid_raises_parse_error():
    try:
        parser = Parser("(0) = 1")
        parser.parse()
        assert False
    except ParseError as e:
        assert (
            str(e)
            == "left side of an infix expression must be a string literal got: Type.NUMBER"
        )


def test_parser_left_side_logical_not_valid_raises_parse_error():
    try:
        parser = Parser("(0) and 1")
        parser.parse()
        assert False
    except ParseError as e:
        assert (
            str(e)
            == "left side of a logical expression must be an infix expression or string literal got: Type.NUMBER"
        )


def test_parser_throws_on_unclosed_group():
    try:
        parser = Parser("(milk and cookies")
        parser.parse()
        assert False
    except ParseError as e:
        assert str(e) == "unclosed group expression @ 17"


def test_parser_cant_concat_non_string():
    try:
        parser = Parser("0 mat")
        parser.parse()
        assert False
    except ParseError as e:
        assert str(e) == "can only concat string literals got: 0.0"

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
def test_parser_performance(query, benchmark):
    """Benchmark the performance of various queries."""

    @benchmark
    def parse_query():
        """Benchmark query parsing"""
        parser = Parser(query)
        parser.parse()
