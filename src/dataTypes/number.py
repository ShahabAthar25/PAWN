from errors.RunTime import RTError

class Number:
    def __init__(self, value):
        self.value = value

        self.set_pos()
        self.set_context()

    def set_pos(self, pos_start=None, pos_end=None):
        self.pos_start = pos_start
        self.pos_end = pos_end

        return self

    def set_context(self, context=None):
        self.context = context
        return self

    def addition(self, other):
        if isinstance(other, Number):
            return Number(self.value + other.value).set_context(self.context), None

    def subtraction(self, other):
        if isinstance(other, Number):
            return Number(self.value - other.value).set_context(self.context), None

    def multiplication(self, other):
        if isinstance(other, Number):
            return Number(self.value * other.value).set_context(self.context), None

    def division(self, other):
        if isinstance(other, Number):
            if other.value == 0:
                return None, RTError(
                    "Division by zero",
                    other.pos_start, other.pos_end, self.context
                )
            return Number(self.value / other.value).set_context(self.context), None

    def modulus(self, other):
        if isinstance(other, Number):
            if other.value == 0:
                return None, RTError(
                    "Modulo by zero",
                    other.pos_start, other.pos_end, self.context
                )
            return Number(self.value % other.value).set_context(self.context), None

    def power(self, other):
        if isinstance(other, Number):
            result = self.value ** other.value
            if result == int(result):
                result = int(result)
            return Number(result).set_context(self.context), None

    def equals_to(self, other):
        if isinstance(other, Number):
            return Number(int(self.value == other.value)).set_context(self.context), None

    def not_equals_to(self, other):
        if isinstance(other, Number):
            return Number(int(self.value != other.value)).set_context(self.context), None

    def less_than(self, other):
        if isinstance(other, Number):
            return Number(int(self.value < other.value)).set_context(self.context), None

    def less_than_equals_to(self, other):
        if isinstance(other, Number):
            return Number(int(self.value <= other.value)).set_context(self.context), None

    def greater_than(self, other):
        if isinstance(other, Number):
            return Number(int(self.value > other.value)).set_context(self.context), None

    def greater_than_equals_to(self, other):
        if isinstance(other, Number):
            return Number(int(self.value >= other.value)).set_context(self.context), None

    def and_operation(self, other):
        if isinstance(other, Number):
            return Number(int(self.value and other.value)).set_context(self.context), None

    def or_operation(self, other):
        if isinstance(other, Number):
            return Number(int(self.value or other.value)).set_context(self.context), None

    def not_operation(self):
        return Number(1 if self.value == 0 else 0).set_context(self.context), None

    def __repr__(self):
        return f"{self.value}"