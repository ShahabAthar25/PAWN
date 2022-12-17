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
    ast = parser.expr()

    return ast, ast.error

def get_current_date():
    return datetime.date.today().strftime("%B %d, %Y") + " " + datetime.datetime.now().strftime("%H:%M:%S")

try:
    filename = sys.argv[1]
except IndexError:
    filename = None

ask_debug = True
dev = False

if ask_debug:
    while True:
        debug = input("Do you want to begin this session as a debug session [y/n] ")
        if debug == "y":
            dev = True
            break
        elif debug == "n":
            dev = False
            break
        else:
            print(f"The expected input was not y or n please try again.")

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
    text = ["1*1", "1*1", "1%1", "1^1", "1*1/1", "1/1*1", "1^1/1*2"]

    print("Warning: Debug mode is on!!!")
    for i in range(len(text)):
        print(f"Running statement '{text[i]}'\n")

        result, error = pawn(text[i])

        if error: print(error.as_string())
        else: print(result)
        print("--------------------------\n")