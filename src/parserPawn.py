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

        return self

    def parse(self):
        res = self.atom()
        if res.error and self.current_tok.type != TT_EOF:
            return res.failure(InvalidSyntaxError(
                "Expected '+', '-', '*' or '/'",
                self.current_tok.pos_start, self.current_tok.pos_end
            ))
        return res

    def factor(self):
        res = ParseResult()
        tok = self.current_tok

        # checking if tok type is int or float
        if tok.type in (TT_INT, TT_FLOAT):
            # advancing since we found a int or float number
            res.register(self.advance())
            # returning number node
            return res.success(NumberNode(tok))

        # checking if tok type is Left Parenthesis
        elif tok.type == TT_LPAREN:
            res.register(self.advance())
            expr = res.register(self.atom())
            if res.error: return res
            if self.current_tok.type == TT_RPAREN:
                res.register(self.advance())
                # returning expr
                return res.success(expr)
            else:
                res.failure(InvalidSyntaxError(
                    "Expected '('",
                    tok.pos_start, tok.pos_end
                ))

        return res.failure(InvalidSyntaxError(
            "Expected int, float, '+', '-' or '('",
            tok.pos_start, tok.pos_end
        ))

    def power(self):
        return self.bin_op(self.factor, TT_POW, self.quark)


    def quark(self):
        res = ParseResult()
        # getting current token to return after advancing to next token
        tok = self.current_tok

        # checking if token type is add or sub
        if tok.type in (TT_ADD, TT_SUB):
            res.register(self.advance())
            # getting right node of unary op
            right_node = res.register(self.factor())
            if res.error: return res
            # returning uninary op
            return res.success(UninaryOpNode(tok, right_node))

        return self.power()

    def electron(self):
        return self.bin_op(self.quark, TT_DIV)

    def proton(self):
        return self.bin_op(self.electron, TT_MUL)

    def neutron(self):
        return self.bin_op(self.proton, TT_ADD)

    def atom(self):
        return self.bin_op(self.neutron, TT_SUB)

    def bin_op(self, left_func, operand, right_func=None):
        if right_func == None:
            right_func = left_func

        res = ParseResult()

        # getting left node
        left_node = left_func()

        # checking if the current token is in operands
        while self.current_tok.type == operand:
            # getting the operator
            op = self.current_tok
            res.register(self.advance())
            # getting right node
            right_node = res.register(right_func())
            if res.error: return res
            # returning a BinOpNode since the token after left_node was in the operand
            left_node = BinOpNode(left_node, op, right_node)

        # returning the left node since token after the left node was not in the operand i.e returning a term, number etc
        return res.success(left_node)