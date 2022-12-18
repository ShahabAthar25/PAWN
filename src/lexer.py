from errors.syntax import IllegalCharError
from position import Position
from tokens import *

DIGITS = '1234567890'
WHITESPACES = ' \t'

class Lexer:
    def __init__(self, text, filename):
        self.text = text
        self.filename = filename
        self.pos = Position(-1, -1, 0, filename, text)
        self.current_char = None

        self.advance()

    def advance(self):
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.pos] if self.pos.pos < len(self.text) else None

    def make_tokens(self):
        tokens = []

        while self.current_char != None:
            if self.current_char in WHITESPACES:
                self.advance()
            elif self.current_char in DIGITS:
                tokens.append(self.make_number())
            elif self.current_char == "+":
                tokens.append(Token(TT_ADD, pos_start=self.pos))
                self.advance()
            elif self.current_char == "-":
                tokens.append(Token(TT_SUB, pos_start=self.pos))
                self.advance()
            elif self.current_char == "*":
                tokens.append(Token(TT_MUL, pos_start=self.pos))
                self.advance()
            elif self.current_char == "/":
                tokens.append(Token(TT_DIV, pos_start=self.pos))
                self.advance()
            elif self.current_char == "^":
                tokens.append(Token(TT_POW, pos_start=self.pos))
                self.advance()
            elif self.current_char == "%":
                tokens.append(Token(TT_MOD, pos_start=self.pos))
                self.advance()
            elif self.current_char == "(":
                tokens.append(Token(TT_LPAREN, pos_start=self.pos))
                self.advance()
            elif self.current_char == ")":
                tokens.append(Token(TT_RPAREN, pos_start=self.pos))
                self.advance()
            else:
                pos_start = self.pos.copy()
                char = self.current_char
                self.advance()
                return [], IllegalCharError(f"'{char}'", pos_start, self.pos.copy())

        tokens.append(Token(TT_EOF, pos_start=self.pos))

        return tokens, None

    def make_number(self):
        num_str = ''
        dot_count = 0

        while self.current_char != None and self.current_char in DIGITS + ".":
            if self.current_char == ".":
                if dot_count > 1: break
                dot_count += 1
            num_str += self.current_char
            self.advance()

        if dot_count != 1:
            return Token(TT_INT, int(num_str), pos_start=self.pos)
        else:
            return Token(TT_FLOAT, float(num_str), pos_start=self.pos)

    def peek(self):
        # Get the position of the next character
        pos = self.pos.pos + 1
        # Try to get the character at that position
        # If the position is out of bounds, return None
        try:
            return self.text[pos]
        except IndexError:
            return None
