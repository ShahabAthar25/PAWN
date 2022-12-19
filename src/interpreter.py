from dataTypes.number import Number
from tokens import *

class Interpreter:
    def visit(self, node):
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.no_visit_method)
        return method(node)

    def no_visit_method(self, node):
        raise Exception(f'No visit_{type(node).__name__} method defined')

    def visit_NumberNode(self, node):
        return Number(node.tok.value).set_pos(node.pos_start, node.pos_end)

    def visit_BinOpNode(self, node):
        left = self.visit(node.left_node)
        right = self.visit(node.right_node)

        if node.op.type == TT_ADD:
            result = left.addition(right)
        elif node.op.type == TT_SUB:
            result = left.substraction(right)
        elif node.op.type == TT_MUL:
            result = left.multiplication(right)
        elif node.op.type == TT_DIV:
            result = left.division(right)
        elif node.op.type == TT_MOD:
            result = left.modulus(right)
        elif node.op.type == TT_POW:
            result = left.power(right)
        
        return result.set_pos(node.pos_start, node.pos_end)

    def visit_UnaryOpNode(self, node):
        number = self.visit(node.tok)

        return number.multiplication(Number(-1))