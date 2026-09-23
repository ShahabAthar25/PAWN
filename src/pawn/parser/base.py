class Parser:

    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = -1
        self.current_tok = None

        self.advance()

    def retreat(self):
        self.pos -= 1

        if self.pos < len(self.tokens):
            self.current_tok = self.tokens[self.pos]

        return self

    def advance(self):
        self.pos += 1

        if self.pos < len(self.tokens):
            self.current_tok = self.tokens[self.pos]

        return self
