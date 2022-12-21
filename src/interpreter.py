from error_handlers.RTResult import RTResult
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
        return RTResult().success(
            Number(node.tok.value).set_pos(node.pos_start, node.pos_end)
        )

    def visit_BinOpNode(self, node):
        res = RTResult()

        left = res.register(self.visit(node.left_node))
        if res.error: return res

        right = res.register(self.visit(node.right_node))
        if res.error: return res

        if node.op.type == TT_ADD:
            result, error = left.addition(right)
        elif node.op.type == TT_SUB:
            result, error = left.substraction(right)
        elif node.op.type == TT_MUL:
            result, error = left.multiplication(right)
        elif node.op.type == TT_DIV:
            result, error = left.division(right)
        elif node.op.type == TT_MOD:
            result, error = left.modulus(right)
        elif node.op.type == TT_POW:
            result, error = left.power(right)

        if error:
            return res.failure(error)
        else:
            return res.success(result.set_pos(node.pos_start, node.pos_end))

    def visit_UnaryOpNode(self, node):
        res = RTResult()

        number = res.register(self.visit(node.tok))
        if res.error: return res

        number, error = number.multiplication(Number(-1))

        if error:
            return res.failure(error)
        else:
            return res.success(number.set_pos(node.pos_start, node.pos_end))