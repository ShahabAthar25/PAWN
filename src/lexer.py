# Import the IllegalCharError class from the errors.syntax module
# and the Position and Token classes from the position and tokens modules, respectively
from errors.syntax import IllegalCharError
from position import Position
from tokens import *
import string

# String of digits to use for recognizing numbers in the input text
DIGITS = '1234567890'
# String of letters to use for recognizing identifiers in the input text
LETTERS = string.ascii_letters

# String of whitespace characters to ignore in the input text
WHITESPACES = ' \t'

class Lexer:
    def __init__(self, text, filename):
        # Initialize the lexer with the input text and filename, and set the current
        # position to the start of the text
        self.text = text
        self.filename = filename
        self.pos = Position(-1, -1, 0, filename, text)

        # Set the current character to None and the token index to 0
        self.current_char = None
        self.tok_idx = 0

        # Advance to the first character in the input text
        self.advance()

    def advance(self):
        # Advance the current position by one character and set the current character
        # to the character at the new position
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.pos] if self.pos.pos < len(self.text) else None

    def make_tokens(self):
        # Initialize an empty list to store the generated tokens
        tokens = []

        # Loop through the characters in the input text
        while self.current_char != None:
            # If the current character is a whitespace character, ignore it and move on
            if self.current_char in WHITESPACES:
                self.advance()
            # If the current character is a digit, create a number token
            elif self.current_char in DIGITS:
                tokens.append(self.make_number())
            # If the current character is a letter, create a identifier token
            elif self.current_char in DIGITS:
                tokens.append(self.make_identifier())
            # If the current character is "+", create an ADD token
            elif self.current_char == "+":
                tokens.append(Token(TT_ADD, pos_start=self.pos))
                self.advance()
            # If the current character is "-", create either a SUB or UNARY_FACTOR token
            # depending on whether the next character is a digit
            elif self.current_char == "-":
                # Check if the next character is a digit
                if self.peek() != None and self.peek() in DIGITS:
                    # If the previous token is a number, add an ADD token
                    try:
                        if tokens[-1].type in (TT_INT, TT_FLOAT):
                            tokens.append(Token(TT_ADD, pos_start=self.pos))
                    except IndexError:
                        pass
                    # If it is, create a UNARY_FACTOR token
                    tokens.append(Token(TT_UNARY_FACTOR, pos_start=self.pos))
                else:
                    # If it is not, create a SUB token
                    tokens.append(Token(TT_SUB, pos_start=self.pos))
                self.advance()
            # If the current character is "*", create a MUL token
            elif self.current_char == "*":
                # Create a MUL token with the current position as the starting position
                tokens.append(Token(TT_MUL, pos_start=self.pos))
                # Advance to the next character
                self.advance()
            # If the current character is "/", create a DIV token
            elif self.current_char == "/":
                # Create a DIV token with the current position as the starting position
                tokens.append(Token(TT_DIV, pos_start=self.pos))
                # Advance to the next character
                self.advance()
            # If the current character is "^", create a POW token
            elif self.current_char == "^":
                # Create a POW token with the current position as the starting position
                tokens.append(Token(TT_POW, pos_start=self.pos))
                # Advance to the next character
                self.advance()
            # If the current character is "%", create a MOD token
            elif self.current_char == "%":
                # Create a MOD token with the current position as the starting position
                tokens.append(Token(TT_MOD, pos_start=self.pos))
                # Advance to the next character
                self.advance()
            # If the current character is "="", create a equals token
            elif self.current_char == "=":
                # Create a EQUAL token with the current position as the starting position
                tokens.append(Token(TT_EQ, pos_start=self.pos))
                # Advance to the next character
                self.advance()
            # If the current character is "(", create a LPAREN token
            elif self.current_char == "(":
                # Create a LPAREN token with the current position as the starting position
                tokens.append(Token(TT_LPAREN, pos_start=self.pos))
                # Advance to the next character
                self.advance()
            # If the current character is ")", create a RPAREN token
            elif self.current_char == ")":
                # Create a RPAREN token with the current position as the starting position
                tokens.append(Token(TT_RPAREN, pos_start=self.pos))
                # Advance to the next character
                self.advance()
            # If the current character is none of these, return an error indicating that
            # an illegal character was encountered
            else:
                # Save the current position as the starting position of the error
                pos_start = self.pos.copy()
                # Save the current character as the character that caused the error
                char = self.current_char
                # Advance to the next character
                self.advance()
                # Return an empty list of tokens and an IllegalCharError instance
                return [], IllegalCharError(f"'{char}'", pos_start, self.pos.copy())

        # Add a EOF (End of File) token to the end of the program so that
        # the parser can make sure that it has reached the end of the program
        tokens.append(Token(TT_EOF, pos_start=self.pos))

        # Return tokens and None as the error
        return tokens, None

    def make_number(self):
        # Initialize an empty string to store the digits of the number
        num_str = ''
        # Initialize a counter for the number of decimal points encountered
        dot_count = 0

        # Loop through the characters in the input text as long as they are digits
        # or a single decimal point
        while self.current_char != None and self.current_char in DIGITS + ".":
            # If the current character is a decimal point, increment the dot count
            # and exit the loop if more than one decimal point has been encountered
            if self.current_char == ".":
                if dot_count > 1: break
                dot_count += 1
            # Add the current character to the number string
            num_str += self.current_char
            # Advance to the next character
            self.advance()

        # If exactly one decimal point was encountered, create a FLOAT token
        # with the value of the number string converted to a float
        if dot_count == 1:
            return Token(TT_FLOAT, float(num_str), pos_start=self.pos)
        # If no decimal points or more than one was encountered, create an INT token
        # with the value of the number string converted to an integer
        else:
            return Token(TT_INT, int(num_str), pos_start=self.pos)

    def make_identifier(self):
        id_str = ''
        pos_start = self.pos.copy()

        while self.current_char != None and self.current_char in LETTERS + DIGITS + "_-":
            id_str += self.current_char
            self.advance()
        
        tok_type = TT_KEYWORD if id_str in KEYWORDS else TT_IDENTIFIER
        return Token(tok_type, id_str, pos_start, self.pos)

    def peek(self, back=False):
        # Determine the position to peek at based on the value of the back argument
        if back:
            pos = self.pos.pos - 1
        else:
            pos = self.pos.pos + 1

        # Try to return the character at the specified position in the input text
        # and return None if the position is out of bounds
        try:
            return self.text[pos]
        except IndexError:
            return None
