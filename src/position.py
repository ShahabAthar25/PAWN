# Initializing a position class to keep track of the line, col and index
# in lexer to give detail to error messages
class Position:
    def __init__(self, pos, col, line, filename, filetext):
        # Initialize the position, column, line, filename, and file text with the provided values
        self.pos = pos
        self.col = col
        self.line = line
        self.filename = filename
        self.filetext = filetext

    def advance(self, current_char=None):
        # Increase the position by 1
        self.pos += 1
        # Increase the column by 1
        self.col += 1

        # If the current character is a newline, increase the line number by 1 and reset the column to 0
        if current_char == "\n":
            self.line += 1
            self.col = 0

        # Return the modified position
        return self

    def copy(self):
        # Return a copy of the current position
        return Position(self.pos, self.col, self.line, self.filename, self.filetext)