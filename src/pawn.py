from lexer import Lexer
from parserPawn import Parser
from interpreter import Interpreter
from context import Context

import datetime
import platform
import sys

from symbolTable.symbolTable import SymbolTable
from symbolTable.setGlobalSymbolTable import setGlobalSymbolTable

global_symbol_table = SymbolTable()
setGlobalSymbolTable(global_symbol_table)

def pawn(text):
    lexer = Lexer(text, "<stdin>")
    tokens, error = lexer.make_tokens()

    if error: return None, error

    parser = Parser(tokens)
    ast = parser.parse()

    if ast.error: return None, ast.error

    interpreter = Interpreter()
    context = Context('<program>')
    context.symbol_table = global_symbol_table
    result = interpreter.visit(ast.node, context)

    return result.value, result.error


def get_current_date():
    return datetime.date.today().strftime("%B %d, %Y") + " " + datetime.datetime.now().strftime("%H:%M:%S")

try:
    filename = sys.argv[1]
except IndexError:
    filename = None

ask_debug = False
dev = False

if ask_debug and not dev:
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
    tests = [
            "3 + 4 - 2",
            "8 / 4 * 2",
            "2^3 % 7",
            "(5 + 3) * (2 - 1)",
            "10 - 3 * 2 / 4",
            "8 + 2 * (5 - 3)",
            "3 * (5 + 1) - 2 / 4",
            "4 % 3 + 7 * (2 - 1)",
            "2^(3-1) + 10 / 5",
            "8 - 3 + 2 * (5 - 1)",
            "let a = 5",
            "a/5",
        ]
    test_ans = [
        "5",
        "4",
        "1",
        "8",
        "8.5",
        "12",
        "17.5",
        "8",
        "6",
        "13",
        "5",
        "1"
    ]

    print("Warning: Debug mode is on!!!") 
    test_passed = 0   
    test_failed = 0
    test_failed_pos = []
    test_failed_ans = []
    print(f"Running tests\n")
    for i in range(len(tests)):
        result, error = pawn(tests[i])
        if str(result) == test_ans[i] or str(result) == test_ans[i] + ".0":
            test_passed += 1
        else:
            test_failed += 1
            test_failed_pos.append(i)
            test_failed_ans.append(result)
    
    print(f"Test passed: {test_passed}")
    print(f"Test failed: {test_failed}")
    if test_failed != 0:
        try:
            while True:
                text = input("Do you want to see the failed tests[y/n]: ")
                if text == "y":
                    for i in range(len(test_failed_pos)):
                        print(f"{tests[test_failed_pos[i]]} = {test_failed_ans[i]} while expected {test_ans[test_failed_pos[i]]}")
                    break
                elif text == "n":
                    break
                else:
                    pass
        except KeyboardInterrupt:
            print("\nExiting")