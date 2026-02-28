from typing import List, Optional, TYPE_CHECKING
from .ast_nodes import FunctionDecl, Parameter
from .errors import ParseError, MissingKeywordError, UnexpectedTokenError

if TYPE_CHECKING:
    from .base_parser import BaseParser
    from .statement_parser import StatementParserMixin

class FunctionParserMixin:
    """提供函数声明解析功能。"""

    def parse_function_declaration(self: 'BaseParser') -> Optional[FunctionDecl]:
        """解析函数声明。

        返回：
            如果成功返回FunctionDecl，如果解析失败返回None
        """
        if not self.current_token:
            return None

        # 存储位置用于错误报告
        start_line = self.current_token.line
        start_column = self.current_token.column

        try:
            # 匹配'function'关键词
            if not self.match_keyword('function'):
                return None

            # 解析函数名
            if (self.current_token is None
                    or self.current_token.type != 'IDENTIFIER'):
                # 创建错误信息
                if self.current_token is None:
                    error = UnexpectedTokenError(
                        message="Expected function name identifier, got end of input",
                        expected="identifier",
                        actual="end of input",
                        line=start_line,
                        column=start_column + len('function ')  # 近似位置
                    )
                else:
                    error = UnexpectedTokenError(
                        message="Expected function name identifier",
                        expected="identifier",
                        actual=self.current_token.value,
                        line=self.current_token.line,
                        column=self.current_token.column
                    )
                self.add_error(error)
                self.skip_to_next_function()
                return None

            func_name = self.current_token.value
            self.next_token()

            # 匹配'takes'关键词
            if not self.match_keyword('takes'):
                # 为缺失的'takes'关键词创建错误
                error_line = self.current_token.line if self.current_token else start_line
                error_column = self.current_token.column if self.current_token else start_column + len('function ') + len(func_name)
                error = MissingKeywordError(
                    message="Missing 'takes' keyword in function declaration",
                    keyword='takes',
                    line=error_line,
                    column=error_column
                )
                self.add_error(error)
                self.skip_to_next_function()
                return None

            # 解析参数列表
            parameters = self.parse_parameter_list()

            # 匹配'returns'关键词
            if not self.match_keyword('returns'):
                # 为缺失的'returns'关键词创建错误
                error_line = self.current_token.line if self.current_token else start_line
                # 近似列位置：在函数名、takes和参数之后
                error_column = self.current_token.column if self.current_token else start_column + len('function ') + len(func_name) + len(' takes ')  # 近似值
                error = MissingKeywordError(
                    message="Missing 'returns' keyword in function declaration",
                    keyword='returns',
                    line=error_line,
                    column=error_column
                )
                self.add_error(error)
                self.skip_to_next_function()
                return None

            # 解析返回类型
            if self.current_token is None:
                # 为缺失的返回类型创建错误
                error_line = start_line
                error_column = start_column + len('function ') + len(func_name) + len(' takes ')  # 近似值
                error = UnexpectedTokenError(
                    message="Expected return type, got end of input",
                    expected="return type (nothing, integer, real, string, boolean, code, handle)",
                    actual="end of input",
                    line=error_line,
                    column=error_column
                )
                self.add_error(error)
                self.skip_to_next_function()
                return None

            return_type = self.current_token.value
            self.next_token()

            # 解析函数体
            body = []
            while self.current_token and not (self.current_token.type == 'KEYWORD' and self.current_token.value == 'endfunction'):
                # 调用由 StatementParserMixin 提供的方法
                # 显式使用 cast 或假设 self 有此方法
                if hasattr(self, 'parse_statement'):
                    statement = self.parse_statement()
                    if statement:
                        body.append(statement)
                else:
                    self.next_token() # 避免死循环

            if self.current_token and self.current_token.value == 'endfunction':
                self.next_token()

            # 创建函数声明
            return FunctionDecl(
                name=func_name,
                parameters=parameters,
                return_type=return_type,
                line=start_line,
                column=start_column,
                body=body
            )

        except Exception:
            # 如果发生任何错误，跳到下一个函数
            self.skip_to_next_function()
            return None

    def parse_parameter_list(self: 'BaseParser') -> List[Parameter]:
        """解析参数列表。

        返回：
            Parameter对象列表
        """
        parameters: List[Parameter] = []

        # 检查是否为'nothing'
        if (self.current_token is not None
                and self.current_token.value == 'nothing'):
            self.next_token()
            return parameters

        # 解析第一个参数
        param = self.parse_parameter()
        if param is not None:
            parameters.append(param)

        # 解析用逗号分隔的附加参数
        while (self.current_token is not None and
               self.current_token.value == ','):
            self.next_token()  # 跳过逗号
            param = self.parse_parameter()
            if param is not None:
                parameters.append(param)

        # 检查缺失的逗号：如果下一个标记看起来像类型关键词
        # （但不是'nothing'，因为上面已经处理了）
        if (self.current_token is not None and
                self.current_token.value in self.TYPE_KEYWORDS and
                self.current_token.value != 'nothing'):
            # 缺失逗号错误
            error = ParseError(
                message=f"Missing comma between parameters, got '{self.current_token.value}'",
                line=self.current_token.line,
                column=self.current_token.column
            )
            self.add_error(error)

        return parameters

    def parse_parameter(self: 'BaseParser') -> Optional[Parameter]:
        """解析单个参数。

        返回：
            如果成功返回Parameter，如果解析失败返回None
        """
        if self.current_token is None:
            # 在正常解析中这不应该发生，但为了安全添加错误
            self.add_error(ParseError(
                message="Unexpected end of input while parsing parameter",
                line=0,  # 未知行
                column=0  # 未知列
            ))
            return None

        # 参数类型
        param_type = self.current_token.value
        type_line = self.current_token.line
        type_column = self.current_token.column
        self.next_token()

        # 参数名
        if (self.current_token is None
                or self.current_token.type != 'IDENTIFIER'):
            # 为缺失的参数名创建错误
            if self.current_token is None:
                error = UnexpectedTokenError(
                    message="Expected parameter name, got end of input",
                    expected="identifier",
                    actual="end of input",
                    line=type_line,
                    column=type_column + len(param_type)  # 类型后的近似位置
                )
            else:
                error = UnexpectedTokenError(
                    message="Expected parameter name after type",
                    expected="identifier",
                    actual=self.current_token.value,
                    line=self.current_token.line,
                    column=self.current_token.column
                )
            self.add_error(error)
            return None

        param_name = self.current_token.value
        self.next_token()

        return Parameter(
            name=param_name,
            type=param_type,
            line=type_line,
            column=type_column
        )
