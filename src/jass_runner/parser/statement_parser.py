from typing import List, Optional, Any, TYPE_CHECKING
from .ast_nodes import (
    IfStmt, LoopStmt, ExitWhenStmt, ReturnStmt
)
from .errors import ParseError

if TYPE_CHECKING:
    from .base_parser import BaseParser
    from .expression_parser import ExpressionParserMixin
    from .assignment_parser import AssignmentParserMixin

class StatementParserMixin:
    """提供语句解析功能。"""

    def parse_statement(self: 'BaseParser') -> Optional[Any]:
        """解析语句。"""
        if not self.current_token:
            return None

        # 解析局部声明
        if self.current_token.type == 'KEYWORD' and self.current_token.value == 'local':
            # 使用 cast 或假设 self 混合了 AssignmentParserMixin
            return self.parse_local_declaration()

        # 解析call语句
        if self.current_token.type == 'KEYWORD' and self.current_token.value == 'call':
            return self.parse_call_statement()

        # 解析set语句
        if self.current_token.type == 'KEYWORD' and self.current_token.value == 'set':
            return self.parse_set_statement()

        # 解析if语句
        if self.current_token.type == 'KEYWORD' and self.current_token.value == 'if':
            return self.parse_if_statement()

        # 解析loop语句
        if self.current_token.type == 'KEYWORD' and self.current_token.value == 'loop':
            return self.parse_loop_statement()

        # 解析exitwhen语句
        if self.current_token.type == 'KEYWORD' and self.current_token.value == 'exitwhen':
            return self.parse_exitwhen_statement()

        # 解析return语句
        if self.current_token.type == 'KEYWORD' and self.current_token.value == 'return':
            return self.parse_return_statement()

        # 目前跳过其他标记
        self.next_token()
        return None

    def parse_if_statement(self: 'BaseParser') -> Optional[IfStmt]:
        """解析if语句。"""
        try:
            # 跳过'if'关键词
            self.next_token()

            # 解析条件表达式
            condition = self.parse_condition()
            if condition is None:
                return None

            # 匹配'then'关键词
            if not self.match_keyword('then'):
                return None

            # 解析then分支的语句列表
            then_body = []
            while (self.current_token and
                   not (self.current_token.type == 'KEYWORD' and
                        self.current_token.value in ('else', 'elseif', 'endif'))):
                statement = self.parse_statement()
                if statement:
                    then_body.append(statement)

            # 解析elseif分支和else分支
            elseif_branches = []
            else_body = []

            # 处理elseif分支
            while (self.current_token and
                   self.current_token.type == 'KEYWORD' and
                   self.current_token.value == 'elseif'):
                # 跳过'elseif'关键词
                self.next_token()

                # 解析elseif条件
                elseif_condition = self.parse_condition()
                if elseif_condition is None:
                    return None

                # 匹配'then'关键词
                if not self.match_keyword('then'):
                    return None

                # 解析elseif分支的语句列表
                elseif_body = []
                while (self.current_token and
                       not (self.current_token.type == 'KEYWORD' and
                            self.current_token.value in ('else', 'elseif', 'endif'))):
                    statement = self.parse_statement()
                    if statement:
                        elseif_body.append(statement)

                elseif_branches.append({"condition": elseif_condition, "body": elseif_body})

            # 处理else分支
            if (self.current_token and
                self.current_token.type == 'KEYWORD' and
                self.current_token.value == 'else'):
                # 跳过'else'关键词
                self.next_token()

                # 解析else分支的语句列表
                while (self.current_token and
                       not (self.current_token.type == 'KEYWORD' and
                            self.current_token.value == 'endif')):
                    statement = self.parse_statement()
                    if statement:
                        else_body.append(statement)

            # 匹配'endif'关键词
            if self.current_token and self.current_token.type == 'KEYWORD' and self.current_token.value == 'endif':
                self.next_token()

            return IfStmt(
                condition=condition,
                then_body=then_body,
                elseif_branches=elseif_branches,
                else_body=else_body
            )

        except Exception:
            return None

    def parse_loop_statement(self: 'BaseParser') -> Optional[LoopStmt]:
        """解析loop循环语句。"""
        try:
            # 跳过'loop'关键词
            self.next_token()

            # 解析循环体内的语句列表
            body = []
            while (self.current_token and
                   not (self.current_token.type == 'KEYWORD' and
                        self.current_token.value == 'endloop')):
                statement = self.parse_statement()
                if statement:
                    body.append(statement)

            # 匹配'endloop'关键词
            if self.current_token and self.current_token.type == 'KEYWORD' and self.current_token.value == 'endloop':
                self.next_token()

            return LoopStmt(body=body)

        except Exception:
            return None

    def parse_exitwhen_statement(self: 'BaseParser') -> Optional[ExitWhenStmt]:
        """解析exitwhen退出循环语句。"""
        try:
            # 跳过'exitwhen'关键词
            self.next_token()

            # 解析条件表达式
            condition = self.parse_condition()
            if condition is None:
                return None

            return ExitWhenStmt(condition=condition)

        except Exception:
            return None

    def parse_return_statement(self: 'BaseParser') -> Optional[ReturnStmt]:
        """解析return返回语句。"""
        try:
            # 跳过'return'关键词
            self.next_token()

            # 检查是否有返回值
            value = None
            if (self.current_token and
                not (self.current_token.type == 'KEYWORD' and
                     self.current_token.value == 'endfunction')):
                # 解析返回值表达式
                if self.current_token.type == 'INTEGER':
                    value = str(self.current_token.value)
                    self.next_token()
                elif self.current_token.type == 'REAL':
                    value = str(self.current_token.value)
                    self.next_token()
                elif self.current_token.type == 'STRING':
                    value = self.current_token.value
                    self.next_token()
                elif self.current_token.type == 'IDENTIFIER':
                    value = self.current_token.value
                    self.next_token()
                elif self.current_token.type == 'KEYWORD' and self.current_token.value in ('true', 'false'):
                    value = self.current_token.value
                    self.next_token()

            return ReturnStmt(value=value)

        except Exception:
            return None
