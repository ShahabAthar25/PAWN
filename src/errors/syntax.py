from errors.error import Error

class IllegalCharError(Error):
    def __init__(self, details):
        super().__init__('Illegal Charector', details)