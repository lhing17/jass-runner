"""解析器错误定义。

此模块包含解析器使用的所有错误类型定义。
"""

from dataclasses import dataclass


@dataclass
class ParseError:
    """解析器错误的基类。"""
    message: str
    line: int
    column: int

    def __str__(self) -> str:
        return f"{self.message} at line {self.line}, column {self.column}"


@dataclass
class MissingKeywordError(ParseError):
    """缺少必需的关键词时的错误。"""
    keyword: str

    def __str__(self) -> str:
        return (f"Missing keyword '{self.keyword}' {self.message} "
                f"at line {self.line}, column {self.column}")


@dataclass
class UnexpectedTokenError(ParseError):
    """遇到意外标记时的错误。"""
    expected: str
    actual: str

    def __str__(self) -> str:
        return (f"Expected {self.expected}, got '{self.actual}' {self.message} "
                f"at line {self.line}, column {self.column}")


@dataclass
class ParameterError(ParseError):
    """参数列表解析中的错误。"""
    pass
