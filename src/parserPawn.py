from parseResult import ParseResult
from errors.syntax import InvalidSyntaxError
from tokens import *
from nodes import *

class Parser:
    def __init__(self, tokens):
        # Initialize the parser with the token stream and set the current token to None
        self.tokens = tokens
        self.pos = -1
        self.current_tok = None

        self.advance()

    def advance(self):
        # Advance the token stream by one and set the current token to the next token
        self.pos += 1

        # Setting self.current_char to next char if exists or to None if it does not
        if self.pos < len(self.tokens):
            self.current_tok = self.tokens[self.pos]

        return self

    def factor(self):
        # Parse a number or parenthesized expression
        res = ParseResult()
        tok = self.current_tok

        if tok.type in (TT_INT, TT_FLOAT):
            # If the current token is an integer or float, return a NumberNode object
            res.register(self.advance())
            return res.success(NumberNode(tok))
        
        elif tok.type == TT_LPAREN:
            # If the current token is a left parenthesis, parse the expression inside the parentheses
            res.register(self.advance())
            expr = res.register(self.expr())
            if res.error: return res
            print(expr, self.current_tok)

            if self.current_tok.type == TT_RPAREN:
                # If the current token is a right parenthesis, return the parsed expression
                res.register(self.advance())
                return res.success(expr)
            else:
                # If the current token is not a right parenthesis, return an error
                return res.failure(InvalidSyntaxError(
                    "Expected ')'",
                    self.current_tok.pos_start, self.current_tok.pos_end
                ))

        elif tok.type == TT_UNARY_FACTOR:
            # If the current token is a unary factor (e.g., "-"), parse the factor that follows it
            res.register(self.advance())

            # Getting the right node
            right = res.register(self.factor())
            # If there is an error then returning the error
            if res.error: return res
            # If there was no error telling parse result the operation was succesful
            res.success(right)

            # Returning the unary operator nod
            return res.success(UnaryOpNode(tok, right))

        # If none of the above conditions are met, return an error
        return res.failure(InvalidSyntaxError(
            "Expected Float, Int or a parenthesis expression",
            self.current_tok.pos_start, self.current_tok.pos_end
        ))

    def power(self):
        # Parse a power expression (e.g., 2 ** 3)
        return self.bin_op(self.factor, (TT_POW, ), self.factor)

    def term(self):
        # Parse a multiplicative expression (e.g., 2 * 3)
        return self.bin_op(self.power, (TT_MUL, TT_DIV, TT_MOD))

    def expr(self):
        # Parse an additive expression (e.g., 2 + 3)
        return self.bin_op(self.term, (TT_ADD, TT_SUB))

    def bin_op(self, func_a, operands, func_b=None):
        # Utility function for parsing binary operations
        if func_b == None:
            # If func_b is not provided, set it to func_a
            func_b = func_a

        res = ParseResult()

        # Parse the left operand using func_a
        left = res.register(func_a())
        if res.error: return res

        while self.current_tok.type in operands:
            # While the current token is one of the operands, parse the right operand using func_b
            op = self.current_tok
            res.register(self.advance())
            right = res.register(func_b())
            left = BinOpNode(left, op, right)

        # Return the left operand as the result of the function
        return res.success(left)
