from parseResult import ParseResult
from errors.syntax import InvalidSyntaxError
from tokens import *
from Nodes import *


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = -1
        self.current_tok = None
        self.power_ran = False

        self.advance()

    def advance(self):
        self.pos += 1

        # Setting self.current_char to next char if exists or to None if it does not
        if self.pos < len(self.tokens):
            self.current_tok = self.tokens[self.pos]

    def factor(self):
        tok = self.current_tok

        if tok in (TT_INT, TT_FLOAT):
            self.advance()
            return NumberNode(tok)

    def term(self):
        left_factor = self.factor()

        while self.current_tok.type in (TT_POW, TT_MUL, TT_DIV, TT_MOD):
            op = self.current_tok
            self.advance()
            right_factor = self.factor()
            left_factor = BinOpNode(left_factor, op, right_factor)

        return left_factor