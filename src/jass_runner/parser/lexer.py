"""简单的JASS词法分析器。"""

from dataclasses import dataclass
from typing import List, Iterator
import re

@dataclass
class Token:
    """表示JASS代码中的一个标记。"""
    type: str
    value: str
    line: int
    column: int

class Lexer:
    """简单的JASS代码词法分析器。"""

    # JASS keywords
    KEYWORDS = {
        'function', 'takes', 'returns', 'nothing', 'integer', 'real',
        'string', 'boolean', 'code', 'handle', 'endfunction', 'call',
        'if', 'then', 'else', 'endif', 'loop', 'endloop', 'exitwhen',
        'set', 'local', 'constant', 'array', 'native', 'type', 'extends',
        # 用户提供列表中的额外关键词
        'true', 'false', 'null', 'elseif', 'return', 'and', 'or', 'not',
        'globals', 'endglobals'
    }

    # 基本标记模式（更新顺序以获得更好的匹配）
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
        """从代码生成标记。"""
        while self.pos < len(self.code):
            matched = False

            for token_type, pattern in self.TOKEN_PATTERNS:
                regex = re.compile(pattern)
                match = regex.match(self.code, self.pos)

                if match:
                    value = match.group(0)

                    # 跳过空白和注释
                    if token_type not in ('WHITESPACE', 'COMMENT', 'MULTILINE_COMMENT'):
                        # 检查标识符是否为关键词
                        actual_type = token_type
                        if token_type == 'IDENTIFIER' and value in self.KEYWORDS:
                            actual_type = 'KEYWORD'

                        yield Token(
                            type=actual_type,
                            value=value,
                            line=self.line,
                            column=self.column
                        )

                    # 更新位置和行/列计数器
                    self.pos = match.end()
                    self._update_position(value)
                    matched = True
                    break

            if not matched:
                # 没有匹配的模式，跳过一个字符
                self._update_position(self.code[self.pos])
                self.pos += 1

    def _update_position(self, text: str):
        """基于文本更新行和列计数器。"""
        lines = text.count('\n')
        if lines > 0:
            self.line += lines
            self.column = 1 + len(text) - text.rfind('\n') - 1
        else:
            self.column += len(text)