class Error:
    def __init__(self, name, details):
        self.name = name
        self.details = details

    def as_string(self):
        result = f'{self.name}: {self.details}'
        return result