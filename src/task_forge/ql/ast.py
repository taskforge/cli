"""AST and Expression classes for the Taskforge query language."""

from typing import Dict, Any, Optional
from datetime import datetime

from task_forge.ql.tokens import Token, Type


class Expression:
    """An expression is a statement that yields a value."""

    date_formats = [
        # Variations of 12 hour clock with AM/PM
        "%Y-%m-%d %I:%M %p",
        "%Y-%m-%d %I:%M%p",
        "%Y-%m-%d %I:%M:%S %p",
        "%Y-%m-%d %I:%M:%S%p",
        # 24 hour formats
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M",
        # Day only
        "%Y-%m-%d",
    ]

    def __init__(
        self,
        token: Token,
        left: Optional["Expression"] = None,
        right: Optional["Expression"] = None,
        value: Optional[Any] = None,
    ):
        """
        Build an Expression from token.

        If token is an operator left and right will be used to build
        an infix expression.

        Otherwise a literal will be returned parsing value from
        token.literal.
        """
        self.token = token

        self.value = None
        self.operator = None
        self.left = None
        self.right = None

        if value is not None:
            self.value = value
        elif token.token_type == Type.STRING:
            self.value = token.literal
        elif token.token_type == Type.NUMBER:
            self.value = float(token.literal)
        elif token.token_type == Type.BOOLEAN:
            self.value = token.literal.lower() == "true"
        elif token.token_type == Type.DATE:
            self.value = Expression.parse_date(token.literal)
        else:
            self.operator = token
            self.left = left
            self.right = right

    def to_dict(self) -> Dict[str, Any]:
        """Return a JSON serializable Dictionary representation of this AST."""
        if self.is_infix():
            assert self.left is not None
            assert self.right is not None
            assert self.operator is not None

            return {
                "left": self.left.to_dict(),
                "right": self.right.to_dict(),
                "operator": self.operator.to_dict(),
            }

        return {"token": self.token.to_dict(), "value": self.value}

    @classmethod
    def from_dict(cls, dictionary: Dict[str, Any]) -> "Expression":
        """Deserialize from a dictionary."""
        if "operator" in dictionary:
            return Expression(
                Token.from_dict(dictionary["operator"]),
                left=Expression.from_dict(dictionary["left"]),
                right=Expression.from_dict(dictionary["right"]),
            )

        return Expression(
            Token.from_dict(dictionary["token"]), value=dictionary["value"]
        )

    def __repr__(self) -> str:
        """Return a string representation of this expression."""
        if self.is_infix() and self.token.token_type in [Type.AND, Type.OR]:
            return f"({self.left} {self.operator.literal} {self.right})"  # type: ignore

        if self.is_infix():
            left_repr = self.left.value if self.left is not None else self.left
            return f"({left_repr} {self.operator.literal} {self.right})"  # type: ignore

        # Quote strings which have spaces in them
        if isinstance(self.value, str) and " " in self.value:
            return f"'{self.value}'"  # type: ignore

        return f"{self.value}"  # type: ignore

    def __eq__(self, other: object) -> Any:
        """Return True if other is the same kind of expression with the same values."""
        if not isinstance(other, Expression):
            return False

        if self.is_infix():
            return (
                other.is_infix()  # type: ignore
                and self.left == other.left  # type: ignore
                and self.operator == other.operator  # type: ignore
                and self.right == other.right  # type: ignore
            )

        return self.value == other.value and self.token == other.token  # type: ignore

    @staticmethod
    def parse_date(date_string: str) -> datetime:
        """Parse a date_string using the first valid format."""
        for date_format in Expression.date_formats:
            try:
                return datetime.strptime(date_string, date_format)
            except ValueError:
                continue

        raise ValueError("date string did not match any known formats")

    def is_infix(self) -> bool:
        """Indicate whether this expression is an infix expression."""
        return self.operator is not None

    def is_literal(self) -> bool:
        """Indicate whether this expression is a literal value."""
        return self.value is not None

    def is_logical_infix(self) -> bool:
        """Indicate if this is a logical AND/OR expression."""
        return self.is_and_infix() or self.is_or_infix()

    def is_and_infix(self) -> bool:
        """Indicate if this is a logical AND expression."""
        assert self.operator is not None
        return self.is_infix() and self.operator.token_type == Type.AND

    def is_or_infix(self) -> bool:
        """Indicate if this is a logical OR expression."""
        assert self.operator is not None
        return self.is_infix() and self.operator.token_type == Type.OR

    def is_str_literal(self) -> bool:
        """Indicate whether this expression is a string value."""
        return self.is_literal() and self.token.token_type == Type.STRING

    def is_date_literal(self) -> bool:
        """Indicate whether this expression is a date value."""
        return self.is_literal() and self.token.token_type == Type.DATE

    def is_number_literal(self) -> bool:
        """Indicate whether this expression is a number value."""
        return self.is_literal() and self.token.token_type == Type.NUMBER

    def is_boolean_literal(self) -> bool:
        """Indicate whether this expression is a boolean value."""
        return self.is_literal() and self.token.token_type == Type.BOOLEAN


class AST:
    """Abstract syntax tree for the Taskforge query language."""

    def __init__(self, expression: Expression):
        """Build an AST from expression."""
        self.expression = expression

    def to_dict(self) -> Dict[str, Any]:
        """Return a JSON serializable Dictionary representation of this AST."""
        return {"expression": self.expression.to_dict()}

    @classmethod
    def from_dict(cls, dictionary: Dict[str, Any]) -> "AST":
        """Deserialize an AST from a Dictionary representation."""
        return cls(expression=Expression.from_dict(dictionary["expression"]))

    def __eq__(self, other: object) -> bool:
        """Return True if other has the same expression."""
        if self.expression == getattr(other, "expression", None):
            return True
        return False

    def __repr__(self) -> str:
        """
        Return a string representation of this AST.

        The resulting string is parsable by a Parser.
        """
        return self.expression.__repr__()
