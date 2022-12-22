from errors.string_with_arrows import string_with_arrows
from errors.error import Error


class RTError(Error):
    def __init__(self, details, pos_start, pos_end, context):
        super().__init__("Runtime Error", details, pos_start, pos_end)
        self.context = context

    def as_string(self):
        result = self.generate_traceback()
        result += f'{self.name}: {self.details}'
        result += '\n       ' + string_with_arrows(self.pos_start.filetext, self.pos_start, self.pos_end)
        return result

    def generate_traceback(self):
        result = ''
        pos = self.pos_start
        ctx = self.context

        while ctx:
            result += f'    File {pos.filename}, line {pos.line + 1}, in {ctx.display_name}\n'
            pos = ctx.parent_entry_pos
            ctx = ctx.parent

        return "Traceback (In the order of most recent call last):\n" + result