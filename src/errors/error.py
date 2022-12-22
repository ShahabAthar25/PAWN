from errors.string_with_arrows import string_with_arrows

class Error:
    def __init__(self, name, details, pos_start, pos_end):
        # Initializing an error base class that will take in name, details and the positions
        # from where the error began to where the errror ended
        self.name = name
        self.details = details
        self.pos_start = pos_start
        self.pos_end = pos_end

    # Definging a as_string method so the lexer or parser could throw errors
    def as_string(self):
        result = f'{self.name}: {self.details}\n'
        result += f'    File {self.pos_start.filename}, line {self.pos_start.line + 1}'
        result += '\n        ' + string_with_arrows(self.pos_start.filetext, self.pos_start, self.pos_end)
        return result