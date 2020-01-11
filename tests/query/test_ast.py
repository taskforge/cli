import unittest
from datetime import datetime

from task_forge.ql.ast import AST, Expression
from task_forge.ql.parser import Parser
from task_forge.ql.tokens import Token


class ASTTests(unittest.TestCase):
    def test_to_and_from_dict(self):
        literal = Expression(Token("milk"))
        a = AST(literal)
        d = a.to_dict()
        self.assertEqual(
            d,
            {
                "expression": {
                    "token": {"token_type": "STRING", "literal": "milk"},
                    "value": "milk",
                }
            },
        )
        self.assertEqual(a, AST.from_dict(d))
        infix = Expression(
            Token("="), left=Expression(Token("foo")), right=Expression(Token("bar")),
        )
        a = AST(infix)
        d = a.to_dict()
        self.assertEqual(
            d,
            {
                "expression": {
                    "operator": {"token_type": "EQ", "literal": "="},
                    "left": {
                        "token": {"token_type": "STRING", "literal": "foo"},
                        "value": "foo",
                    },
                    "right": {
                        "token": {"token_type": "STRING", "literal": "bar"},
                        "value": "bar",
                    },
                }
            },
        )
        self.assertEqual(a, AST.from_dict(d))

    def test_repr(self):
        test_cases = [
            # Note the single quotes here
            ("'milk and cookies'", AST(Expression(Token("milk and cookies")))),
            (
                "(milk and cookies)",
                AST(
                    Expression(
                        Token("and"),
                        left=Expression(Token("milk")),
                        right=Expression(Token("cookies")),
                    )
                ),
            ),
            (
                "(foo = bar)",
                AST(
                    Expression(
                        Token("="),
                        left=Expression(Token("foo")),
                        right=Expression(Token("bar")),
                    )
                ),
            ),
        ]

        for query, obj in test_cases:
            self.assertEqual(repr(obj), query)
            # Test that the repr is re-parsable to get the same AST
            self.assertEqual(Parser(query).parse(), obj)

    def test_unparsable_date_raises_valueerror(self):
        try:
            Expression.parse_date("foo")
        except ValueError as e:
            self.assertEqual(str(e), "date string did not match any known formats")


class ExpressionTests(unittest.TestCase):
    def test_expression_values_literals(self):
        literals = [
            {"literal": "1.0", "value": 1.0},
            {"literal": "hello world", "value": "hello world"},
            {"literal": "2018-01-01", "value": datetime(year=2018, month=1, day=1)},
            {"literal": "True", "value": True},
            {"literal": "true", "value": True},
            {"literal": "False", "value": False},
            {"literal": "false", "value": False},
        ]

        for literal in literals:
            with self.subTest(**literal):
                exp = Expression(Token(literal["literal"]))
                self.assertEqual(type(exp.value), type(literal["value"]))
                self.assertEqual(exp.value, literal["value"])

    def test_is_infix(self):
        infix = Expression(Token("="), left=Token("title"), right=Token("right"))
        self.assertTrue(infix.is_infix())

    def test_is_literal(self):
        literal = Expression(Token("milk"))
        self.assertTrue(literal.is_literal())

    def test_is_logical_infix(self):
        logical_and = Expression(
            Token("and"), left=Expression(Token("foo")), right=Expression(Token("bar")),
        )
        self.assertEqual(logical_and.is_logical_infix(), True)

        logical_or = Expression(
            Token("and"), left=Expression(Token("foo")), right=Expression(Token("bar")),
        )
        self.assertEqual(logical_or.is_logical_infix(), True)

        illogical = Expression(
            Token("="), left=Expression(Token("foo")), right=Expression(Token("bar")),
        )
        self.assertEqual(illogical.is_logical_infix(), False)

    def test_is_literal_types(self):
        literal = Expression(Token("foo"))
        self.assertEqual(literal.is_str_literal(), True)
        self.assertEqual(literal.is_date_literal(), False)
        self.assertEqual(literal.is_number_literal(), False)
        self.assertEqual(literal.is_boolean_literal(), False)

        literal = Expression(Token("true"))
        self.assertEqual(literal.is_str_literal(), False)
        self.assertEqual(literal.is_date_literal(), False)
        self.assertEqual(literal.is_number_literal(), False)
        self.assertEqual(literal.is_boolean_literal(), True)

        literal = Expression(Token("0"))
        self.assertEqual(literal.is_str_literal(), False)
        self.assertEqual(literal.is_date_literal(), False)
        self.assertEqual(literal.is_number_literal(), True)
        self.assertEqual(literal.is_boolean_literal(), False)

        literal = Expression(Token("2019-01-01"))
        self.assertEqual(literal.is_str_literal(), False)
        self.assertEqual(literal.is_date_literal(), True)
        self.assertEqual(literal.is_number_literal(), False)
        self.assertEqual(literal.is_boolean_literal(), False)

    def test_date_formats(self):
        date_strings = [
            {
                "date_string": "2018-01-01",
                "expected": datetime(year=2018, month=1, day=1),
            },
            {
                "date_string": "2018-01-01 01:01",
                "expected": datetime(year=2018, month=1, day=1, hour=1, minute=1),
            },
            {
                "date_string": "2018-01-01 01:01:10",
                "expected": datetime(
                    year=2018, month=1, day=1, hour=1, minute=1, second=10
                ),
            },
            {
                "date_string": "2018-01-01 01:01:10 PM",
                "expected": datetime(
                    year=2018, month=1, day=1, hour=13, minute=1, second=10
                ),
            },
            {
                "date_string": "2018-01-01 01:01:10PM",
                "expected": datetime(
                    year=2018, month=1, day=1, hour=13, minute=1, second=10
                ),
            },
            {
                "date_string": "2018-01-01 01:01 PM",
                "expected": datetime(year=2018, month=1, day=1, hour=13, minute=1),
            },
            {
                "date_string": "2018-01-01 01:01PM",
                "expected": datetime(year=2018, month=1, day=1, hour=13, minute=1),
            },
        ]

        for date in date_strings:
            with self.subTest(**date):
                result = Expression.parse_date(date["date_string"])
                self.assertEqual(result, date["expected"])
