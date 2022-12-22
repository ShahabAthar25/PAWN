from error_handlers.parseResult import ParseResult
from errors.syntax import InvalidSyntaxError
from tokens import *
from nodes import *

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = -1
        self.current_tok = None

        self.advance()

    def advance(self):
        self.pos += 1

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
    
    def if_expr(self):
        res = ParseResult()
        cases = []
        else_case = None

        res.register(self.advance())

        condition = res.register(self.condition())
        if res.error: return res

        if not self.current_tok.matches(TT_KEYWORD, 'then'):
            return res.failure(InvalidSyntaxError(
                "Expected 'then'",
                self.current_tok.pos_start, self.current_tok.pos_end
            ))

        res.register(self.advance())
        
        expr = res.register(self.expr())
        if res.error: return res
        cases.append((condition, expr))

        while self.current_tok.matches(TT_KEYWORD, "else"):
            res.register(self.advance())

            if self.current_tok.matches(TT_KEYWORD, "if"):
                res.register(self.advance())

                condition = res.register(self.condition())
                if res.error: return res

                if not self.current_tok.matches(TT_KEYWORD, "then"):
                    return res.failure(InvalidSyntaxError(
                        "Expected 'then'",
                        self.current_tok.pos_start, self.current_tok.pos_end
                    ))
                
                res.register(self.advance())

                expr = res.register(self.expr())
                if res.error: return res

                cases.append((condition, expr))

            else:
                else_case = res.register(self.expr())
                if res.error: return res

        return res.success(IfNode(cases, else_case))
    
    def while_loop(self):
        res = ParseResult()

        res.register(self.advance())

        condition = res.register(self.condition())
        if res.error: return res

        if not self.current_tok.matches(TT_KEYWORD, 'then'):
            return res.failure(InvalidSyntaxError(
                "Expected 'then'",
                self.current_tok.pos_start, self.current_tok.pos_end
            ))
        
        res.register(self.advance())

        expr = res.register(self.expr())
        if res.error: return res

        return res.success(WhileNode(condition, expr))

    def factor(self):
        res = ParseResult()
        tok = self.current_tok

        if tok.type in (TT_INT, TT_FLOAT):
            res.register(self.advance())
            return res.success(NumberNode(tok))
        
        elif tok.type == TT_IDENTIFIER:
            res.register(self.advance())
            return res.success(VarAccessNode(tok))
        
        elif tok.type == TT_LPAREN:
            res.register(self.advance())
            expr = res.register(self.expr())
            if res.error: return res

            if self.current_tok.type == TT_RPAREN:
                res.register(self.advance())
                return res.success(expr)
            else:
                return res.failure(InvalidSyntaxError(
                    "Expected ')'",
                    self.current_tok.pos_start, self.current_tok.pos_end
                ))

        elif tok.type in (TT_ADD, TT_SUB):
            res.register(self.advance())

            right = res.register(self.factor())
            if res.error: return res

            return res.success(UnaryOpNode(tok, right))

        elif tok.matches(TT_KEYWORD, "if"):
            if_expr = res.register(self.if_expr())
            if res.error: return res
            return res.success(if_expr)

        elif tok.matches(TT_KEYWORD, "while"):
            while_loop = res.register(self.while_loop())
            if res.error: return res
            return res.success(while_loop)

        return res.failure(InvalidSyntaxError(
            "Expected Float, Int or a parenthesis expression",
            self.current_tok.pos_start, self.current_tok.pos_end
        ))

    def power(self):
        return self.bin_op(self.factor, (TT_POW, ))

    def term(self):
        return self.bin_op(self.power, (TT_MUL, TT_DIV, TT_MOD))

    def arith_expr(self):
        return self.bin_op(self.term, (TT_ADD, TT_SUB))

    def comp_expr(self):
        res = ParseResult()

        if self.current_tok.matches(TT_KEYWORD, 'not'):
            tok = self.current_tok
            res.register(self.advance())
            right = res.register(self.comp_expr())
            return res.success(UnaryOpNode(tok, right))

        return self.bin_op(self.arith_expr, (TT_EE, TT_NE, TT_LT, TT_LTE, TT_GT, TT_GTE))

    def condition(self):
        return self.bin_op(self.comp_expr, ((TT_KEYWORD, 'and'), (TT_KEYWORD, 'or')))

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
        
        return self.condition()

    def bin_op(self, func, operands):
        res = ParseResult()

        left = res.register(func())
        if res.error: return res

        while self.current_tok.type in operands or (self.current_tok.type, self.current_tok.value) in operands:
            op = self.current_tok
            res.register(self.advance())
            right = res.register(func())
            if res.error: return res
            left = BinOpNode(left, op, right)

        return res.success(left)
