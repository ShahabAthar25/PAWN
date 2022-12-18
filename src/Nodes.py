# The NumberNode class represents a number token in the AST.
class NumberNode:
    def __init__(self, tok):
        self.tok = tok # Reference to the token object.

    def __repr__(self):
        return f'{self.tok}'


# Class representing a node for a unary operation (e.g. -2)
class UnaryOpNode:
    def __init__(self, op, tok):
        self.op = op  # The operator for the unary operation
        self.tok = tok  # The token representing the number

    def __repr__(self):
        return f'({self.op}, {self.tok})'


# Class representing a node for a binary operation (e.g. 2 + 3)
class BinOpNode:
    def __init__(self, left_node, op, right_node):
        self.left_node = left_node  # The left operand of the binary operation
        self.op = op  # The operator for the binary operation
        self.right_node = right_node  # The right operand of the binary operation

    def __repr__(self):
        return f'({self.left_node}, {self.op}, {self.right_node})'
