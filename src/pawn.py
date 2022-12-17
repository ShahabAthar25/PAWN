from lexer import Lexer
from parserPawn import Parser

import datetime
import platform
import sys

def pawn(text):
    lexer = Lexer(text, "<stdin>")
    tokens, error = lexer.make_tokens()

    if error: return None, error
    
    parser = Parser(tokens)
    ast = parser.term()

    return ast.node, ast.error

def get_current_date():
    return datetime.date.today().strftime("%B %d, %Y") + " " + datetime.datetime.now().strftime("%H:%M:%S")

try:
    filename = sys.argv[1]
except IndexError:
    filename = None

dev = True

if not dev:
    print(f"PAWN 0.0.1 (main, ALPHA) on {platform.system()} {platform.release()}, shell session started at {get_current_date()}")
    print(f"Type 'help()' for help")
    try:
        while True:
            text = input(">>> ")

            result, error = pawn(text)

            if error: print(error.as_string())
            else: print(result)
    except KeyboardInterrupt:
        print(f"\nSession ended on {get_current_date()}")
        exit()
else:
    text = "1/1"

    print("Warning: Debug mode is on!!!")
    print(f"Running statement {text}\n\n")

    result, error = pawn(text)

    if error: print(error.as_string())
    else: print(result)