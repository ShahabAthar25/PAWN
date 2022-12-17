class Error:
    def __init__(self, name, details, pos_start, pos_end):
        self.name = name
        self.details = details
        self.pos_start = pos_start
        self.pos_end = pos_end

    def as_string(self):
        result = f'{self.name}: {self.details}\n'
        result += f'    File {self.pos_start.filename}, line {self.pos_start.line + 1}'
        return result