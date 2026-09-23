from dataclasses import dataclass


@dataclass(slots=True)
class Position:
    """Tracks token coordinates in source code for precise error highlighting."""

    pos: int
    col: int
    line: int
    filename: str
    filetext: str

    def advance(self, current_char: str | None = None) -> "Position":
        self.pos += 1
        self.col += 1

        if current_char == "\n":
            self.line += 1
            self.col = 0

        return self

    def copy(self) -> "Position":
        return Position(self.pos, self.col, self.line, self.filename, self.filetext)
