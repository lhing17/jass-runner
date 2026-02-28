"""JASS解析器模块。

此模块包含JASS代码的词法分析和语法分析功能。
"""

from .lexer import Lexer, Token
from .errors import ParseError, MissingKeywordError, UnexpectedTokenError, ParameterError
from .ast_nodes import (
    Parameter, GlobalDecl, LocalDecl, FunctionDecl, AST,
    NativeCallNode, SetStmt, IfStmt, LoopStmt, ExitWhenStmt, ReturnStmt
)
from .parser import Parser

__all__ = [
    # 词法分析
    'Lexer',
    'Token',
    # 错误类
    'ParseError',
    'MissingKeywordError',
    'UnexpectedTokenError',
    'ParameterError',
    # AST节点
    'Parameter',
    'GlobalDecl',
    'LocalDecl',
    'FunctionDecl',
    'AST',
    'NativeCallNode',
    'SetStmt',
    'IfStmt',
    'LoopStmt',
    'ExitWhenStmt',
    'ReturnStmt',
    # 解析器
    'Parser',
]
