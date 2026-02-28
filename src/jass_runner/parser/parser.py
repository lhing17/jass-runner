"""JASS解析器实现。

此模块实现JASS代码的递归下降解析器。
它将词法分析器的标记流转换为抽象语法树（AST）。
"""

from typing import List
# Re-export AST nodes to maintain backward compatibility
from .ast_nodes import (
    Parameter, GlobalDecl, LocalDecl, FunctionDecl, AST,
    NativeCallNode, SetStmt, IfStmt, LoopStmt, ExitWhenStmt, ReturnStmt
)
# Re-export errors to maintain backward compatibility
from .errors import ParseError, MissingKeywordError, UnexpectedTokenError, ParameterError
from .base_parser import BaseParser
from .expression_parser import ExpressionParserMixin
from .global_parser import GlobalParserMixin
from .statement_parser import StatementParserMixin
from .function_parser import FunctionParserMixin
from .assignment_parser import AssignmentParserMixin

class Parser(BaseParser, GlobalParserMixin, FunctionParserMixin, StatementParserMixin, ExpressionParserMixin, AssignmentParserMixin):
    """JASS代码的递归下降解析器。"""

    def parse(self) -> AST:
        """解析JASS代码并返回AST。

        返回：
            包含全局变量声明和函数声明的AST
        """
        # 从词法分析器获取所有标记，过滤掉空白和注释
        self.tokens = [
            token for token in self.lexer.tokenize()
            if token.type not in ('WHITESPACE', 'COMMENT', 'MULTILINE_COMMENT')
        ]

        if not self.tokens:
            return AST(globals=[], functions=[])

        self.token_index = 0
        self.current_token = self.tokens[0] if self.tokens else None

        # 首先解析可选的 globals 块
        globals_list = self.parse_globals_block()

        # 存储全局变量名用于冲突检查
        self.global_names = {g.name for g in globals_list}

        functions: List[FunctionDecl] = []

        # 主解析循环：查找函数声明
        while self.current_token is not None:
            if (self.current_token.type == 'KEYWORD'
                    and self.current_token.value == 'function'):
                func = self.parse_function_declaration()
                if func is not None:
                    functions.append(func)
            else:
                self.next_token()

        return AST(globals=globals_list, functions=functions)
