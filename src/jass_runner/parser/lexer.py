"""简单的JASS词法分析器。"""

from dataclasses import dataclass
from typing import List, Iterator
import re
from ..utils import fourcc_to_int

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

    def _try_match_fourcc(self) -> Iterator[Token]:
        """尝试匹配FourCC格式（单引号包围的4个字符）。

        FourCC格式：'ABCD'，其中ABCD是恰好4个ASCII字符。
        如果匹配成功，将其作为INTEGER类型的token返回。
        """
        if self.code[self.pos] != "'":
            return

        # 检查是否有足够的字符
        if self.pos + 6 > len(self.code):
            return

        # 检查格式：'xxxx'
        chars = self.code[self.pos + 1:self.pos + 5]
        end_quote = self.code[self.pos + 5]

        if end_quote != "'":
            return

        # 验证中间4个字符都是有效的ASCII字符
        if not all(32 <= ord(c) <= 126 for c in chars):
            return

        # 转换为整数
        try:
            value = fourcc_to_int(chars)
            yield Token(
                type='INTEGER',
                value=value,
                line=self.line,
                column=self.column
            )
            # 更新位置（跳过 'xxxx' 共6个字符）
            self._update_position(self.code[self.pos:self.pos + 6])
            self.pos += 6
        except ValueError:
            # 转换失败，不处理
            pass

    def tokenize(self) -> Iterator[Token]:
        """从代码生成标记。"""
        while self.pos < len(self.code):
            matched = False

            # 首先尝试匹配FourCC格式（单引号后跟恰好4个字符再跟单引号）
            if self.code[self.pos] == "'":
                fourcc_matched = False
                for token in self._try_match_fourcc():
                    yield token
                    fourcc_matched = True
                if fourcc_matched:
                    continue
                # FourCC匹配失败，将单引号作为普通标点符号处理
                yield Token(
                    type='PUNCTUATION',
                    value="'",
                    line=self.line,
                    column=self.column
                )
                self._update_position("'")
                self.pos += 1
                continue

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

                        # 处理数字：区分为INTEGER或REAL
                        processed_value = value
                        if token_type == 'NUMBER':
                            if '.' in value:
                                actual_type = 'REAL'
                                processed_value = float(value)
                            else:
                                actual_type = 'INTEGER'
                                processed_value = int(value)

                        yield Token(
                            type=actual_type,
                            value=processed_value,
                            line=self.line,
                            column=self.column
                        )

                    # 更新位置和行/列计数器（使用原始字符串值）
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