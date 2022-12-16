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

        return self

    def factor(self):
        # getting current token to return after advancing to next token
        tok = self.current_tok

        # checking if tok type is int or float
        if tok.type in (TT_INT, TT_FLOAT):
            # advancing since we found a int or float number
            self.advance()
            # returning number node
            return NumberNode(tok)
    
    def electron(self):
        return self.bin_op(self.factor, TT_DIV)

    def proton(self):
        return self.bin_op(self.electron, TT_MUL)

    def neutron(self):
        return self.bin_op(self.proton, TT_ADD)

    def atom(self):
        return self.bin_op(self.neutron, TT_SUB)

    def bin_op(self, func, operand):
        # getting left node
        left_node = func()

        # checking if the current token is in operands
        while self.current_tok.type == operand:
            # getting the operator
            op = self.current_tok
            self.advance()
            # getting right node
            right_node = func()
            # returning a BinOpNode since the token after left_node was in the operand
            left_node = BinOpNode(left_node, op, right_node)

        # returning the left node since token after the left node was not in the operand i.e returning a term, number etc
        return left_node