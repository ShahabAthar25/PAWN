# The NumberNode class represents a number token in the AST.
class NumberNode:
    def __init__(self, tok):
        self.tok = tok # Reference to the token object.

        self.pos_start = self.tok.pos_start
        self.pos_end = self.tok.pos_end

    def __repr__(self):
        return f'{self.tok}'


# Class representing a node for a unary operation (e.g. -2)
class UnaryOpNode:
    def __init__(self, op, tok):
        self.op = op  # The operator for the unary operation
        self.tok = tok  # The token representing the number

        self.pos_start = self.op.pos_start
        self.pos_end = self.tok.pos_end

    def __repr__(self):
        return f'({self.op}, {self.tok})'


# Class representing a node for a binary operation (e.g. 2 + 3)
class BinOpNode:
    def __init__(self, left_node, op, right_node):
        self.left_node = left_node  # The left operand of the binary operation
        self.op = op  # The operator for the binary operation
        self.right_node = right_node  # The right operand of the binary operation

        self.pos_start = self.left_node.pos_start
        self.pos_end = self.right_node.pos_end

    def __repr__(self):
        return f'({self.left_node}, {self.op}, {self.right_node})'

class VarAccessNode:
    def __init__(self, var_name_tok):
        self.var_name_tok = var_name_tok

        self.pos_start = self.var_name_tok.pos_start
        self.pos_end = self.var_name_tok.pos_end

class VarAssignNode:
    def __init__(self, var_name_tok, value_node):
        self.var_name_tok = var_name_tok
        self.value_node = value_node

        self.pos_start = self.var_name_tok.pos_start
        self.pos_end = self.value_node.pos_end

class IfNode:
    def __init__(self, cases, else_case):
        self.cases = cases
        self.else_case = else_case

        self.pos_start = self.cases[0][0].pos_start
        self.pos_end = (self.else_case or self.cases[len(self.cases) - 1][0]).pos_end

class WhileNode:
    def __init__(self, condition, expr):
        self.condition = condition
        self.expr = expr

        self.pos_start = self.condition.pos_start
        self.pos_end = self.expr.pos_end