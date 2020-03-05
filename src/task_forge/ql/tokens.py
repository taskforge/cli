"""Contains the Token and Type classes."""

import re
from enum import Enum
from typing import Optional, Dict

DATE_REGEX = re.compile(
    "^[0-9]{4}-[0-9]{2}-[0-9]{2}( [0-9]{2}:[0-9]{2})? ?(AM|PM|pm|am)?"
)
NUMBER_REGEX = re.compile("^[0-9]{1,}")


class Type(Enum):
    """Represents the various token types."""

    GT = "GT"
    LT = "LT"
    GTE = "GTE"
    LTE = "LTE"
    EQ = "EQ"
    NE = "NE"
    LIKE = "LIKE"
    NLIKE = "NLIKE"

    AND = "AND"
    OR = "OR"

    LPAREN = "LPAREN"
    RPAREN = "RPAREN"

    EOF = "EOF"
    STRING = "STRING"
    NUMBER = "NUMBER"
    DATE = "DATE"
    BOOLEAN = "BOOLEAN"

    UNEXPECTED = "UNEXPECTED"


LITERAL_TYPES = {
    "or": Type.OR,
    "OR": Type.OR,
    "and": Type.AND,
    "AND": Type.AND,
    "false": Type.BOOLEAN,
    "False": Type.BOOLEAN,
    "true": Type.BOOLEAN,
    "True": Type.BOOLEAN,
    ">": Type.GT,
    "<": Type.LT,
    ">=": Type.GTE,
    "<=": Type.LTE,
    "=": Type.EQ,
    "!=": Type.NE,
    "^=": Type.NE,
    "^": Type.LIKE,
    "~": Type.LIKE,
    "^^": Type.NLIKE,
    "!~": Type.NLIKE,
    "(": Type.LPAREN,
    ")": Type.RPAREN,
}


class Token:
    """A query language lexical Token."""

    def __init__(self, literal: str, token_type: Optional[Type] = None):
        """
        Return a token for literal.

        If token_type is None will be determined from literal.
        """
        self.literal = literal
        if token_type is not None:
            self.token_type = token_type
            return

        if LITERAL_TYPES.get(literal):
            self.token_type = LITERAL_TYPES[literal]
        elif DATE_REGEX.match(literal):
            self.token_type = Type.DATE
        elif NUMBER_REGEX.match(literal):
            self.token_type = Type.NUMBER
        else:
            self.token_type = Type.STRING

    def to_dict(self) -> Dict[str, str]:
        """Return a JSON serializable Dictionary represenation of this AST."""
        return {"token_type": self.token_type.value, "literal": self.literal}

    @classmethod
    def from_dict(cls, dictionary: Dict[str, str]) -> "Token":
        """Deserialize from a Dictionary."""
        return Token(literal=dictionary["literal"])

    def __repr__(self) -> str:
        """Return a string representation of this token."""
        return f"Token({self.token_type}, {self.literal})"

    def __eq__(self, other: object) -> bool:
        """Return equal if other's literal and token_type are the same."""
        literal = getattr(other, "literal", None)
        token_type = getattr(other, "token_type", Type.EOF)
        if self.literal == literal and self.token_type == token_type:
            return True
        return False
