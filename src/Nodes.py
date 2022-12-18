class NumberNode:
    def __init__(self, tok):
        self.tok = tok

    def __repr__(self):
        return f'{self.tok}'

class UnaryOpNode:
    def __init__(self, op, tok):
        self.op = op
        self.tok = tok

    def __repr__(self):
        return f'({self.op}, {self.tok})'

class BinOpNode:
    def __init__(self, left_node, op, right_node):
        self.left_node = left_node
        self.op = op
        self.right_node = right_node

    def __repr__(self):
        return f'({self.left_node}, {self.op}, {self.right_node})'
