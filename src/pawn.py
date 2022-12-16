import datetime
import platform
import sys
from lexer import Lexer

dev = False

def get_current_date():
    return datetime.date.today().strftime("%B %d, %Y") + " " + datetime.datetime.now().strftime("%H:%M:%S")

try:
    filename = sys.argv[1]
except IndexError:
    filename = None

if not dev:
    print(f"PAWN 0.0.1 (main, ALPHA) on {platform.system()} {platform.release()}, shell session started at {get_current_date()}")
    print(f"Type 'help()' for help")
    try:
        while True:
            text = input(">>>")

            lexer = Lexer(text, "<stdin>")
            tokens = lexer.make_tokens()

            print(tokens)
    except KeyboardInterrupt:
        print(f"\nSession ended on {get_current_date()}")
        exit()