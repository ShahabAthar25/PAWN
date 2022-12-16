TT_INT		=		"INT"
TT_FLOAT	=		"FLOAT"
TT_MUL		=		"MUL"
TT_DIV		=		"DIV"
TT_ADD		=		"ADD"
TT_SUB		=		"SUB"
TT_LPAREN	=		"LPAREN"
TT_RPAREN	=		"RPAREN"

class Token:
	def __init__(self, _type, value):
		self.type = _type
		self.value = value
	
	def __repr__(self):
		if self.value:
			return f"{self.type}:{self.value}"
		return f"{self.value}"