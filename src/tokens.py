# Define constants for token types
TT_INT 			= "INT"  # Integer token
TT_FLOAT		= "FLOAT"  # Float token
TT_IDENTIFIER	= "IDENTIFIER"  # Identifier token
TT_KEYWORD		= "KEYWORD"  # Keyword token
TT_POW 			= "POW"  # Power token
TT_DIV 			= "DIV"  # Division token
TT_MUL 			= "MUL"  # Multiplication token
TT_ADD 			= "ADD"  # Addition token
TT_SUB 			= "SUB"  # Subtraction token
TT_MOD 			= "MOD"  # Modulus token
TT_LPAREN 		= "LPAREN"  # Left parenthesis token
TT_RPAREN 		= "RPAREN"  # Right parenthesis token
TT_UNARY_FACTOR = "UNARY_FACTOR"  # Unary factor token
TT_EQ 			= "EQ"  # Equals token
TT_EE 			= "EE"  # Equals to token
TT_NE 			= "NE"  # Not equals to token
TT_LT 			= "LT"  # Less than token
TT_GT 			= "GT"  # Greater than token
TT_LTE 			= "LTE"  # Less than or equals to token
TT_GTE 			= "GTE"  # Greater than or equals to token
TT_EOF 			= "EOF"  # End-of-file token

KEYWORDS = [
	"let",
	"and",
	"or",
	"not",
	"if",
	"then",
	"else",
	"while"
]

# Define a class for tokens
class Token:
	def __init__(self, _type, value=None, pos_start=None, pos_end=None):
		# Set the token type and value
		self.type = _type
		self.value = value

		# If a starting position is provided, set it as the start and end position for the token
        # and advance the end position by one character
		if pos_start:
			self.pos_start = pos_start.copy()
			self.pos_end = pos_start.copy()
			self.pos_end.advance()

		# If an end position is provided, set it as the end position for the token
		if pos_end:
			self.pos_end = self.pos_end.copy()

	def matches(self, _type, value):
		return self.type == _type and self.value == value
	
	# Define a representation for the token
	def __repr__(self):
		# If the token has a value, return the type and value as a string
		if self.value:
			return f"{self.type}:{self.value}"
		# If the value is not provided then returning only type
		return f"{self.type}"