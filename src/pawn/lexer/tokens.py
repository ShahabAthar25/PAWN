from dataclasses import dataclass
from enum import StrEnum, auto
from typing import Any, Final

from pawn.lexer.position import Position


class TokenType(StrEnum):
    # Literal types
    INT = auto()
    FLOAT = auto()
    STRING = auto()
    IDENTIFIER = auto()
    KEYWORD = auto()

    # Operators
    POW = auto()
    DIV = auto()
    MUL = auto()
    ADD = auto()
    SUB = auto()
    MOD = auto()
    UNARY_FACTOR = auto()

    # Comparison / Assignment
    EQ = auto()
    EE = auto()
    NE = auto()
    LT = auto()
    GT = auto()
    LTE = auto()
    GTE = auto()

    # Delimiters & Control
    LPAREN = auto()
    RPAREN = auto()
    LCURLY = auto()
    RCURLY = auto()
    COMMA = auto()
    EOF = auto()


KEYWORDS: Final[set[str]] = {
    "let",
    "and",
    "or",
    "not",
    "if",
    "else",
    "while",
    "for",
    "func",
}


@dataclass(slots=True)
class Token:
    type: TokenType
    value: Any = None
    pos_start: Position | None = None
    pos_end: Position | None = None

    def __post_init__(self) -> None:
        if self.pos_start and self.pos_end is None:
            self.pos_end = self.pos_start.copy()
            self.pos_end.advance()

    def matches(self, type_: TokenType, value: Any) -> bool:
        return self.type == type_ and self.value == value

    def __repr__(self) -> str:
        if self.value is not None:
            return f"{self.type.value}:{self.value}"
        return f"{self.type.value}"
