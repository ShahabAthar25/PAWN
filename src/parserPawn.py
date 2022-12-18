from parseResult import ParseResult
from errors.syntax import InvalidSyntaxError
from tokens import *
from Nodes import *

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = -1
        self.current_tok = None

        self.advance()

    def advance(self):
        self.pos += 1

        # Setting self.current_char to next char if exists or to None if it does not
        if self.pos < len(self.tokens):
            self.current_tok = self.tokens[self.pos]

    def atom(self):
        res = ParseResult()
        tok = self.current_tok

        if tok.type in (TT_INT, TT_FLOAT):
            res.register(self.advance())
            return res.success(NumberNode(tok))
        
        elif tok.type == TT_LPAREN:
            res.register(self.advance())
            expr = res.register(self.expr())
            if res.error: return res

            if self.current_tok.type == TT_RPAREN:
                self.advance()
                return expr
            else:
                return res.failure(InvalidSyntaxError(
                    "Expected a ')'",
                    self.current_tok.pos_start, self.current_tok.pos_end
                ))

        return res.failure(InvalidSyntaxError(
            "Expected int, flaot or a parentheses operation",
            self.current_tok.pos_start, self.current_tok.pos_end
        ))


    def power(self):
        return self.bin_op(self.atom, (TT_POW, ), self.factor)
    
    def factor(self):
        res = ParseResult()
        tok = self.current_tok

        if tok.type in (TT_ADD, TT_SUB):
            op = self.current_tok
            res.register(self.advance())
            right = res.register(self.term())
            return res.success(UnaryOpNode(op, right))
        
        return self.power()

    def term(self):
        return self.bin_op(self.factor, (TT_MUL, TT_DIV))

    def expr(self):
        return self.bin_op(self.term, (TT_ADD, TT_SUB))

    def bin_op(self, func_a, operands, func_b=None):
        if func_b == None:
            func_b = func_a

        res = ParseResult()

        left = res.register(func_a())
        if res.error: return res

        while self.current_tok.type in operands:
            op = self.current_tok
            self.advance()
            right = res.register(func_b())
            left = BinOpNode(left, op, right)

        return res.success(left)