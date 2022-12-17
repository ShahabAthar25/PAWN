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
        res = ParseResult()
        tok = self.current_tok

        if tok.type in (TT_INT, TT_FLOAT):
            res.register(self.advance())
            return res.success(NumberNode(tok))

        elif tok.type in (TT_ADD, TT_SUB):
            res.register(self.advance())
            right_node = self.factor()
            return res.success(UninaryOpNode(tok, right_node))

        elif tok.type == TT_LPAREN:
            res.register(self.advance())
            expr = res.register(self.expr())
            if self.current_tok.type == TT_RPAREN:
                res.register(self.advance())
                return res.success(expr)
            else:
                return res.failure(InvalidSyntaxError(
                    "Expected ')'",
                    tok.pos_start, self.current_tok.pos_end
                ))

        return res.failure(InvalidSyntaxError(
            "Expected a int or float",
            tok.pos_start, tok.pos_end
        ))
    def power(self):
        return self.bin_op(self.factor, (TT_POW, ))

    def term(self):
        return self.bin_op(self.power, (TT_MUL, TT_DIV, TT_MOD))

    def expr(self):
        return self.bin_op(self.term, (TT_ADD, TT_SUB))

    def bin_op(self, func, operands):
        res = ParseResult()

        left_factor = res.register(func())
        if res.error: return res

        while self.current_tok.type in operands:
            op = self.current_tok
            self.advance()
            right_factor = res.register(func())
            if res.error: return res
            left_factor = BinOpNode(left_factor, op, right_factor)

        return res.success(left_factor)