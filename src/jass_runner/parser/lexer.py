"""Simple JASS lexer."""

from dataclasses import dataclass
from typing import List, Iterator
import re

@dataclass
class Token:
    """Represents a token in JASS code."""
    type: str
    value: str
    line: int
    column: int

class Lexer:
    """Simple lexer for JASS code."""

    # JASS keywords
    KEYWORDS = {
        'function', 'takes', 'returns', 'nothing', 'integer', 'real',
        'string', 'boolean', 'code', 'handle', 'endfunction', 'call',
        'if', 'then', 'else', 'endif', 'loop', 'endloop', 'exitwhen',
        'set', 'local', 'constant', 'array', 'native', 'type', 'extends',
        # Additional keywords from user-provided list
        'true', 'false', 'null', 'elseif', 'return', 'and', 'or', 'not',
        'globals', 'endglobals'
    }

    # Basic token patterns (update order for better matching)
    TOKEN_PATTERNS = [
        ('WHITESPACE', r'\s+'),
        ('MULTILINE_COMMENT', r'/\*[\s\S]*?\*/'),
        ('COMMENT', r'//.*'),
        ('STRING', r'"[^"]*"'),
        ('NUMBER', r'\d+(\.\d+)?'),
        ('OPERATOR', r'[+\-*/=<>!&|^%~]+'),
        ('PUNCTUATION', r'[(),;.:{}]'),
        ('IDENTIFIER', r'[a-zA-Z_][a-zA-Z0-9_]*'),
    ]

    def __init__(self, code: str):
        self.code = code
        self.pos = 0
        self.line = 1
        self.column = 1

    def tokenize(self) -> Iterator[Token]:
        """Generate tokens from the code."""
        while self.pos < len(self.code):
            matched = False

            for token_type, pattern in self.TOKEN_PATTERNS:
                regex = re.compile(pattern)
                match = regex.match(self.code, self.pos)

                if match:
                    value = match.group(0)

                    # Skip whitespace and comments
                    if token_type not in ('WHITESPACE', 'COMMENT', 'MULTILINE_COMMENT'):
                        # Check if identifier is a keyword
                        actual_type = token_type
                        if token_type == 'IDENTIFIER' and value in self.KEYWORDS:
                            actual_type = 'KEYWORD'

                        yield Token(
                            type=actual_type,
                            value=value,
                            line=self.line,
                            column=self.column
                        )

                    # Update position and line/column counters
                    self.pos = match.end()
                    self._update_position(value)
                    matched = True
                    break

            if not matched:
                # No pattern matched, skip one character
                self._update_position(self.code[self.pos])
                self.pos += 1

    def _update_position(self, text: str):
        """Update line and column counters based on text."""
        lines = text.count('\n')
        if lines > 0:
            self.line += lines
            self.column = 1 + len(text) - text.rfind('\n') - 1
        else:
            self.column += len(text)