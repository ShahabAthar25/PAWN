from error_handlers.parseResult import ParseResult
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

    def parse(self):
        res = self.expr()
        if not res.error and self.current_tok.type != TT_EOF:
            return res.failure(InvalidSyntaxError(
                "Expected '(', '+', '-', '*', '/' or '^'",
                self.current_tok.pos_start, self.current_tok.pos_end
            ))
        return res

    def factor(self):
        # Parse a number or parenthesized expression
        res = ParseResult()
        tok = self.current_tok

        if tok.type in (TT_INT, TT_FLOAT):
            # If the current token is an integer or float, return a NumberNode object
            res.register(self.advance())
            return res.success(NumberNode(tok))
        
        elif tok.type == TT_IDENTIFIER:
            res.register(self.advance())
            return res.success(VarAccessNode(tok))
        
        elif tok.type == TT_LPAREN:
            # If the current token is a left parenthesis, parse the expression inside the parentheses
            res.register(self.advance())
            expr = res.register(self.expr())
            if res.error: return res

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

        elif tok.type in (TT_ADD, TT_SUB):
            # If the current token is a unary factor (e.g., "-"), parse the factor that follows it
            res.register(self.advance())

            # Getting the right node
            right = res.register(self.factor())
            # If there is an error then returning the error
            if res.error: return res

            # Returning the unary operator node
            return res.success(UnaryOpNode(tok, right))

        # If none of the above conditions are met, return an error
        return res.failure(InvalidSyntaxError(
            "Expected Float, Int or a parenthesis expression",
            self.current_tok.pos_start, self.current_tok.pos_end
        ))

    def power(self):
        # Parse a power expression (e.g., 2 ^ 3)
        return self.bin_op(self.factor, (TT_POW, ))

    def term(self):
        # Parse a multiplicative expression (e.g., 2 * 3)
        return self.bin_op(self.power, (TT_MUL, TT_DIV, TT_MOD))

    def expr(self):
        res = ParseResult()

        if self.current_tok.matches(TT_KEYWORD, 'let'):
            res.register(self.advance())

            if self.current_tok.type != TT_IDENTIFIER:
                return res.failure(InvalidSyntaxError(
                    "Expected identifier",
                    self.current_tok.pos_start, self.current_tok.pos_end
                ))
            
            var_name = self.current_tok
            res.register(self.advance())

            if self.current_tok.type != TT_EQ:
                return res.failure(InvalidSyntaxError(
                    "Expected '='",
                    self.current_tok.pos_start, self.current_tok.pos_end
                ))

            res.register(self.advance())
            expr = res.register(self.expr())

            return res.success(VarAssignNode(var_name, expr))

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
            if res.error: return res
            left = BinOpNode(left, op, right)

        # Return the left operand as the result of the function
        return res.success(left)
