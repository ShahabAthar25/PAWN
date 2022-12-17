TT_INT		=		"INT"
TT_FLOAT	=		"FLOAT"
TT_POW		=		"POW"
TT_DIV		=		"DIV"
TT_MUL		=		"MUL"
TT_ADD		=		"ADD"
TT_SUB		=		"SUB"
TT_MOD		=		"MOD"
TT_LPAREN	=		"LPAREN"
TT_RPAREN	=		"RPAREN"
TT_EOF		=		"EOF"

class Token:
	def __init__(self, _type, value=None, pos_start=None, pos_end=None):
		self.type = _type
		self.value = value

		if pos_start:
			self.pos_start = pos_start.copy()
			self.pos_end = pos_start.copy()
			self.pos_end.advance()

		if pos_end:
			self.pos_end = self.pos_end.copy()
	
	def __repr__(self):
		if self.value:
			return f"{self.type}:{self.value}"
		return f"{self.type}"