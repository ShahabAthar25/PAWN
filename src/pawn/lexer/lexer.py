import string
from typing import List

from errors.syntax import IllegalCharError
from position import Position
from tokens import *

DIGITS = "1234567890"
LETTERS = string.ascii_letters

WHITESPACES = " \t"


class Lexer:
    def __init__(self, text: str, filename: str):
        self.text = text
        self.filename = filename
        self.pos = Position(-1, -1, 0, filename, text)

        self.tokens: List[Token] = []

        self.advance()

    def advance(self):
        self.pos.advance(self.current_char)
        self.current_char: str | None = (
            self.text[self.pos.pos] if self.pos.pos < len(self.text) else None
        )

    def _add_token(self, token) -> None:
        self.tokens.append(Token(token, pos_start=self.pos))
        self.advance()

    def make_tokens(self):
        tokens = []

        while self.current_char != None:
            if self.current_char in WHITESPACES:
                self.advance()
            elif self.current_char in DIGITS:
                tokens.append(self.make_number())
            elif self.current_char in LETTERS:
                tokens.append(self.make_identifier())
            elif self.current_char == ",":
                self._add_token(TT_COMMA)
            elif self.current_char == "+":
                self._add_token(TT_ADD)
            elif self.current_char == "-":
                self._add_token(TT_SUB)
            elif self.current_char == "*":
                self._add_token(TT_MUL)
            elif self.current_char == "/":
                self._add_token(TT_DIV)
            elif self.current_char == "^":
                self._add_token(TT_POW)
            elif self.current_char == "%":
                self._add_token(TT_MOD)
            elif self.current_char == "(":
                self._add_token(TT_LPAREN)
            elif self.current_char == ")":
                self._add_token(TT_RPAREN)
            elif self.current_char == "{":
                self._add_token(TT_LCURLY)
            elif self.current_char == "}":
                self._add_token(TT_RCURLY)
            elif self.current_char == "!":
                tokens.append(self.make_not_equals())
            elif self.current_char == "=":
                tokens.append(self.make_equals())
            elif self.current_char == "<":
                tokens.append(self.make_less_than())
            elif self.current_char == ">":
                tokens.append(self.make_greater_than())
            else:
                pos_start = self.pos.copy()
                char = self.current_char
                self.advance()
                return [], IllegalCharError(f"'{char}'", pos_start, self.pos.copy())

        tokens.append(Token(TT_EOF, pos_start=self.pos))

        return tokens, None

    def make_number(self) -> Token:
        num_str = ""
        dot_count = 0

        while self.current_char != None and self.current_char in DIGITS + ".":
            if self.current_char == ".":
                if dot_count > 1:
                    break
                dot_count += 1
            num_str += self.current_char
            self.advance()

        if dot_count == 1:
            return Token(TT_FLOAT, float(num_str), pos_start=self.pos)
        else:
            return Token(TT_INT, int(num_str), pos_start=self.pos)

    def make_identifier(self) -> Token:
        id_str = ""
        pos_start = self.pos.copy()

        while (
            self.current_char != None and self.current_char in LETTERS + DIGITS + "_-"
        ):
            id_str += self.current_char
            self.advance()

        tok_type = TT_KEYWORD if id_str in KEYWORDS else TT_IDENTIFIER
        return Token(tok_type, id_str, pos_start, self.pos)

    def make_not_equals(self) -> Token:
        pos_start = self.pos.copy()
        self.advance()

        if self.current_char == "=":
            self.advance()
            return Token(TT_NE, pos_start=pos_start, pos_end=self.pos)

        return Token(TT_KEYWORD, "not", pos_start=pos_start, pos_end=self.pos)

    def make_equals(self) -> Token:
        tok_type = TT_EQ
        pos_start = self.pos.copy()
        self.advance()

        if self.current_char == "=":
            self.advance()
            tok_type = TT_EE

        return Token(tok_type, pos_start=pos_start, pos_end=self.pos)

    def make_less_than(self) -> Token:
        tok_type = TT_LT
        pos_start = self.pos.copy()
        self.advance()

        if self.current_char == "=":
            self.advance()
            tok_type = TT_LTE

        return Token(tok_type, pos_start=pos_start, pos_end=self.pos)

    def make_greater_than(self) -> Token:
        tok_type = TT_GT
        pos_start = self.pos.copy()
        self.advance()

        if self.current_char == "=":
            self.advance()
            tok_type = TT_GTE

        return Token(tok_type, pos_start=pos_start, pos_end=self.pos)
