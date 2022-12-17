from errors.error import Error

class IllegalCharError(Error):
    def __init__(self, details, pos_start, pos_end):
        super().__init__('Illegal Charector', details, pos_start, pos_end)

class InvalidSyntaxError(Error):
    def __init__(self, details, pos_start, pos_end):
        super().__init__('Invalid Syntax', details, pos_start, pos_end)