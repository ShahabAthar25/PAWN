from pawn.lexer import Lexer

code = '// let a = "Hello World"\n55+55=110'

lexer = Lexer(code, "main.pawn")
tokens = list(lexer.tokenize())

print(tokens)
