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
            return Number(self.value + other.value)

    def subtraction(self, other):
        if isinstance(other, Number):
            return Number(self.value - other.value)

    def multiplication(self, other):
        if isinstance(other, Number):
            return Number(self.value * other.value)

    def division(self, other):
        if isinstance(other, Number):
            return Number(self.value / other.value)

    def modulus(self, other):
        if isinstance(other, Number):
            return Number(self.value % other.value)

    def power(self, other):
        if isinstance(other, Number):
            result = self.value ** other.value
            if result == int(result):
                result = int(result)
            return Number(result)

    def __repr__(self) -> str:
        return f"{self.value}"