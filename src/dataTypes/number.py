from errors.RunTime import RTError

class Number:
    def __init__(self, value):
        self.value = value

        self.set_pos()

    def set_pos(self, pos_start=None, pos_end=None):
        self.pos_start = pos_start
        self.pos_end = pos_end

        return self

    def addition(self, other):
        if isinstance(other, Number):
            return Number(self.value + other.value), None

    def subtraction(self, other):
        if isinstance(other, Number):
            return Number(self.value - other.value), None

    def multiplication(self, other):
        if isinstance(other, Number):
            return Number(self.value * other.value), None

    def division(self, other):
        if isinstance(other, Number):
            if other.value == 0:
                return None, RTError(
                    "Division by zero",
                    other.pos_start, other.pos_end
                )
            return Number(self.value / other.value), None

    def modulus(self, other):
        if isinstance(other, Number):
            if other.value == 0:
                return None, RTError(
                    "Modulo by zero",
                    other.pos_start, other.pos_end
                )
            return Number(self.value % other.value), None

    def power(self, other):
        if isinstance(other, Number):
            result = self.value ** other.value
            if result == int(result):
                result = int(result)
            return Number(result), None

    def __repr__(self):
        return f"{self.value}"