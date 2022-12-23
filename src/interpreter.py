from error_handlers.RTResult import RTResult
from dataTypes.number import Number
from errors.RunTime import RTError
from tokens import *

class Interpreter:
    def visit(self, node, context):
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.no_visit_method)
        return method(node, context)

    def no_visit_method(self, node, context):
        raise Exception(f'No visit_{type(node).__name__} method defined')

    def visit_NumberNode(self, node, context):
        return RTResult().success(
            Number(node.tok.value).set_context(context).set_pos(node.pos_start, node.pos_end)
        )

    def visit_VarAccessNode(self, node, context):
        res = RTResult()
        var_name = node.var_name_tok.value
        value = context.symbol_table.get(var_name)

        if not value:
            res.failure(RTError(
                f"'{var_name}' is not defined",
                node.pos_start, node.pos_end, context
            ))

        return res.success(value)
    
    def visit_VarAssignNode(self, node, context):
        res = RTResult()
        var_name = node.var_name_tok.value
        value = res.register(self.visit(node.value_node, context))
        if res.error: return res

        context.symbol_table.set(var_name, value)
        return res.success(value)

    def visit_BinOpNode(self, node, context):
        res = RTResult()

        left = res.register(self.visit(node.left_node, context))
        if res.error: return res

        right = res.register(self.visit(node.right_node, context))
        if res.error: return res

        if node.op.type == TT_ADD:
            result, error = left.addition(right)
        elif node.op.type == TT_SUB:
            result, error = left.subtraction(right)
        elif node.op.type == TT_MUL:
            result, error = left.multiplication(right)
        elif node.op.type == TT_DIV:
            result, error = left.division(right)
        elif node.op.type == TT_MOD:
            result, error = left.modulus(right)
        elif node.op.type == TT_POW:
            result, error = left.power(right)
        elif node.op.type == TT_EE:
            result, error = left.equals_to(right)
        elif node.op.type == TT_NE:
            result, error = left.not_equals_to(right)
        elif node.op.type == TT_LT:
            result, error = left.less_than(right)
        elif node.op.type == TT_LTE:
            result, error = left.less_than_equals_to(right)
        elif node.op.type == TT_GT:
            result, error = left.greater_than(right)
        elif node.op.type == TT_GTE:
            result, error = left.greater_than_equals_to(right)
        elif node.op.matches(TT_KEYWORD, 'and'):
            result, error = left.and_operation(right)
        elif node.op.matches(TT_KEYWORD, 'or'):
            result, error = left.or_operation(right)

        if error:
            return res.failure(error)
        else:
            return res.success(result.set_pos(node.pos_start, node.pos_end))

    def visit_UnaryOpNode(self, node, context):
        res = RTResult()

        number = res.register(self.visit(node.tok, context))
        if res.error: return res

        error = None
        if node.op.type == TT_SUB:
            number, error = number.multiplication(Number(-1))
        if node.op.matches(TT_KEYWORD, 'not'):
            number, error = number.not_operation()

        if error:
            return res.failure(error)
        else:
            return res.success(number.set_pos(node.pos_start, node.pos_end))
    
    def visit_IfNode(self, node, context):
        res = RTResult()

        for condition, expr in node.cases:
            condition_value = res.register(self.visit(condition, context))
            if res.error: return res

            if condition_value.value == 1:
                expr_value = res.register(self.visit(expr, context))
                if res.error: return res
                return res.success(expr_value)
        
        if node.else_case:
            expr = res.register(self.visit(node.else_case, context))
            if res.error: return res
            return res.success(expr)
        
        return res.success(None)

    def visit_WhileNode(self, node, context):
        res = RTResult()

        while True:
            condition = res.register(self.visit(node.condition, context))
            if res.error: return res

            if condition.value == 0: break

            res.register(self.visit(node.expr, context))
            if res.error: return res

        return res.success(None)

    def visit_ForNode(self, node, context):
        res = RTResult()

        starting_value = res.register(self.visit(node.starting_value, context))
        if res.error: return res

        ending_value = res.register(self.visit(node.ending_value, context))
        if res.error: return res

        if node.gaps:
            gaps = res.register(self.visit(node.gaps, context))
            if res.error: return res
        else:
            gaps = Number(1)

        for i in range(starting_value.value, ending_value.value, gaps.value):
            res.register(self.visit(node.expr, context))
            if res.error: return res
        
        return res.success(None)