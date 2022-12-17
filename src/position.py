class Position:
    def __init__(self, pos, col, line, filename, filetext):
        self.pos = pos
        self.col = col
        self.line = line
        self.filename = filename
        self.filetext = filetext

    def advance(self, current_char=None):
        self.pos += 1
        self.col += 1

        if current_char == "\n":
            self.line += 1
            self.col = 0

        return self

    def copy(self):
        return Position(self.pos, self.col, self.line, self.filename, self.filetext)