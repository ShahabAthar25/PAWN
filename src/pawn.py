# Import the Lexer and Parser classes from the lexer and parserPawn modules
from lexer import Lexer
from parserPawn import Parser
from interpreter import Interpreter

# Import the datetime, platform, and sys modules for use in various functions
import datetime
import platform
import sys

# Define a function that takes an input string and returns the resulting AST
# and any error that occurred during parsing
def pawn(text):
    # Create a Lexer instance with the input text and a filename of "<stdin>"
    lexer = Lexer(text, "<stdin>")
    # Tokenize the input text and save the result and any error that occurred
    tokens, error = lexer.make_tokens()

    # If an error occurred during tokenization, return None for the AST and the error
    if error: return None, error
    
    # Create a Parser instance with the resulting tokens
    parser = Parser(tokens)
    # Parse the tokens and save the resulting AST
    ast = parser.parse()
    # If there was an error then returning the error and none as the result
    if ast.error: return None, ast.error

    interpreter = Interpreter()
    result = interpreter.visit(ast.node)

    return result.value, None

# Define a function that returns the current date and time in a specific format
def get_current_date():
    # Return the current date and time in the format "Month Day, Year Hour:Minute:Second"
    return datetime.date.today().strftime("%B %d, %Y") + " " + datetime.datetime.now().strftime("%H:%M:%S")

# Try to get the filename passed as an argument to the script
try:
    filename = sys.argv[1]
except IndexError:
    # If no filename was passed, set the filename to None
    filename = None

# Set a flag to determine whether the user is asked if they want to run the script in debug mode
ask_debug = False
# Set a flag to determine whether the script is running in debug mode
dev = False

# If the ask_debug flag is set to True and the script is not already running in debug mode
if ask_debug and not dev:
    # Keep asking the user if they want to run the script in debug mode until they provide a valid response
    while True:
        debug = input("Do you want to begin this session as a debug session [y/n] ")
        # If answer is y then luanch in dev mode
        if debug == "y":
            dev = True
            break
        # If answer is n then luanch in shell mode
        elif debug == "n":
            dev = False
            break
        # If answer is not a n or y then ask user to input correct answer again and again
        # until correct answer is given
        else:
            print(f"The expected input was not y or n please try again.")

# If the script is not running in debug mode
if not dev:
    # Print the welcome message and instructions for using the shell
    print(f"PAWN 0.0.1 (main, ALPHA) on {platform.system()} {platform.release()}, shell session started at {get_current_date()}")
    print(f"Type 'help()' for help")

    # Run an infinite loop to read and execute input from the user
    try:
        while True:
            # Read a line of input from the user
            text = input(">>> ")

            # Parse and execute the input and save the result and any error that occurred
            result, error = pawn(text)

            # If an error occurred, print it
            if error: print(error.as_string())
            # If no error occurred, print the result of the execution
            else: print(result)
    # If the user sends a keyboard interrupt (Ctrl+C), print a message and exit the program
    except KeyboardInterrupt:
        print(f"\nSession ended on {get_current_date()}")
        exit()
# If the script is running in debug mode
else:
    # Set a list of test statements to be executed
    text = ["-2", "-2^2"]

    # Print a warning that the script is running in debug mode
    print("Warning: Debug mode is on!!!")
    # Loop through the test statements
    for i in range(len(text)):
        # Print the statement being executed
        print(f"Running statement '{text[i]}'\n")

        # Parse and execute the statement and save the result and any error that occurred
        result, error = pawn(text[i])

        # If an error occurred, print it
        if error: print(error.as_string())
        # If no error occurred, print the result of the execution
        else: print(result)
        # Print a separator line
        print("--------------------------\n")
