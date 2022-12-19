from errors.error import Error

class IllegalCharError(Error):
    # Error for when an illegal character is encountered in the input
    def __init__(self, details, pos_start, pos_end):
        super().__init__('Illegal Charector', details, pos_start, pos_end)

class InvalidSyntaxError(Error):
    # Error for when the input has invalid syntax
    def __init__(self, details, pos_start, pos_end):
        super().__init__('Invalid Syntax', details, pos_start, pos_end)