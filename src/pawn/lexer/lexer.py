import re
from typing import Final, Generator

from pawn.errors.syntax import IllegalCharError
from pawn.lexer.position import Position
from pawn.lexer.tokens import KEYWORDS, Token, TokenType

# Master Token Specification using regex Named Capture Groups
# Order matters: longer/more specific rules must come before general ones
TOKEN_REGEX: Final[str] = "|".join(
    [
        # Single line comments (skipped)
        r"(?P<COMMENT>//[^\n]*)",
        # Whitespace (skipped)
        r"(?P<WHITESPACE>[ \t\r]+)",
        r"(?P<NEWLINE>\n)",
        # Literals
        r"(?P<STRING>\"(?:\\.|[^\\])*?\")",  # Matches "hello \"world\""
        r"(?P<FLOAT>\d+\.\d+)",
        r"(?P<INT>\d+)",
        r"(?P<IDENTIFIER>[a-zA-Z_][a-zA-Z0-9_]*)",
        # Two-character operators
        r"(?P<EE>==)",
        r"(?P<NE>!=)",
        r"(?P<LTE><=)",
        r"(?P<GTE>>=)",
        # Single-character operators & delimiters
        r"(?P<EQ>=)",
        r"(?P<LT><)",
        r"(?P<GT>>)",
        r"(?P<ADD>\+)",
        r"(?P<SUB>-)",
        r"(?P<MUL>\*)",
        r"(?P<DIV>/)",
        r"(?P<MOD>%)",
        r"(?P<POW>\^)",
        r"(?P<LPAREN>\()",
        r"(?P<RPAREN>\))",
        r"(?P<LCURLY>\{)",
        r"(?P<RCURLY>\})",
        r"(?P<COMMA>,)",
    ]
)

MASTER_PATTERN: Final[re.Pattern[str]] = re.compile(TOKEN_REGEX)


class Lexer:
    """Regex-based lexer using generators for on-demand tokenization."""

    def __init__(self, text: str, filename: str) -> None:
        self.text: str = text
        self.filename: str = filename

    def tokenize(self) -> Generator[Token, None, None]:
        """Yields tokens dynamically using regex scanning."""
        line = 1
        line_start = 0

        for match in MASTER_PATTERN.finditer(self.text):
            kind = match.lastgroup
            value = match.group()
            start_idx = match.start()
            end_idx = match.end()

            # Calculate exact coordinates for error diagnostics
            col_start = start_idx - line_start
            col_end = end_idx - line_start

            pos_start = Position(start_idx, col_start, line, self.filename, self.text)
            pos_end = Position(end_idx, col_end, line, self.filename, self.text)

            # Skip non-token elements
            if kind == "WHITESPACE" or kind == "COMMENT":
                continue
            elif kind == "NEWLINE":
                line += 1
                line_start = end_idx
                continue

            # Process Literals & Keywords
            if kind == "IDENTIFIER":
                tok_type = (
                    TokenType.KEYWORD if value in KEYWORDS else TokenType.IDENTIFIER
                )
                yield Token(tok_type, value, pos_start=pos_start, pos_end=pos_end)

            elif kind == "STRING":
                # Strip bounding quotes and resolve escape sequences like \n, \t, \"
                unquoted_val = value[1:-1].encode().decode("unicode_escape")
                yield Token(
                    TokenType.STRING, unquoted_val, pos_start=pos_start, pos_end=pos_end
                )

            elif kind == "INT":
                yield Token(
                    TokenType.INT, int(value), pos_start=pos_start, pos_end=pos_end
                )

            elif kind == "FLOAT":
                yield Token(
                    TokenType.FLOAT, float(value), pos_start=pos_start, pos_end=pos_end
                )

            else:
                # Operators / Delimiters match enum names directly (e.g. TokenType.ADD)
                tok_type = TokenType[kind]
                yield Token(tok_type, pos_start=pos_start, pos_end=pos_end)

            # Check if there are unparsed illegal characters between matches
            # Handled automatically by checking match boundaries if needed

        # Yield EOF marker
        eof_pos = Position(
            len(self.text), len(self.text) - line_start, line, self.filename, self.text
        )
        yield Token(TokenType.EOF, pos_start=eof_pos, pos_end=eof_pos)
