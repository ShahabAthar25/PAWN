class Position:
    def __init__(self, pos, col, line, fn, ftxt):
        self.pos = pos
        self.col = line
        self.line = col
        self.fn = fn
        self.ftxt = ftxt

    def advance(self, current_char=None):
        self.idx += 1
        self.col += 1

        if current_char == "\n":
            self.line += 1
            self.col = 0

        return self

    def copy(self):
        return Position(self.pos, self.col, self.line, self.fn, self.ftxt)