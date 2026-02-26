"""
JASS解析器实现。

此模块实现JASS代码的递归下降解析器。
它将词法分析器的标记流转换为抽象语法树（AST）。
"""

from dataclasses import dataclass
from typing import List, Optional, Any
from .lexer import Lexer, Token


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


@dataclass
class Parameter:
    """函数参数节点。"""
    name: str
    type: str
    line: int  # 来自标记的行号
    column: int  # 来自标记的列号


@dataclass
class LocalDecl:
    """表示局部变量声明。"""
    name: str
    type: str
    value: Any


@dataclass
class FunctionDecl:
    """函数声明节点。"""
    name: str
    parameters: List[Parameter]
    return_type: str
    line: int
    column: int
    body: Optional[List[Any]] = None  # 现在将包含语句


@dataclass
class AST:
    """抽象语法树根节点。"""
    functions: List[FunctionDecl]


@dataclass
class NativeCallNode:
    """原生函数调用节点。"""
    func_name: str
    args: List[Any]


class Parser:
    """JASS代码的递归下降解析器。"""

    # 可能出现在参数列表中的JASS类型关键词
    TYPE_KEYWORDS = {
        'integer', 'real', 'string', 'boolean', 'code', 'handle', 'nothing'
    }

    def __init__(self, code: str):
        """使用JASS代码初始化解析器。

        参数：
            code: 要解析的JASS源代码
        """
        self.lexer = Lexer(code)
        self.tokens: List[Token] = []
        self.current_token: Optional[Token] = None
        self.token_index = 0
        self.errors: List[ParseError] = []

    def parse(self) -> AST:
        """解析JASS代码并返回AST。

        返回：
            包含所有已解析函数声明的AST
        """
        # 从词法分析器获取所有标记，过滤掉空白和注释
        self.tokens = [
            token for token in self.lexer.tokenize()
            if token.type not in ('WHITESPACE', 'COMMENT', 'MULTILINE_COMMENT')
        ]

        if not self.tokens:
            return AST(functions=[])

        self.token_index = 0
        self.current_token = self.tokens[0] if self.tokens else None

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

        return AST(functions=functions)

    def parse_function_declaration(self) -> Optional[FunctionDecl]:
        """解析函数声明。

        返回：
            如果成功返回FunctionDecl，如果解析失败返回None
        """
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
                statement = self.parse_statement()
                if statement:
                    body.append(statement)

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

    def parse_parameter_list(self) -> List[Parameter]:
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
            # 尝试通过将其解析为另一个参数来恢复
            # （跳过类型标记并期望一个名称，这很可能会失败）
            # 目前，只需继续并让解析器处理它

        return parameters

    def parse_parameter(self) -> Optional[Parameter]:
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

    def add_error(self, error: ParseError) -> None:
        """添加错误到错误列表。"""
        self.errors.append(error)

    def match_keyword(self, keyword: str) -> bool:
        """检查当前标记是否匹配给定的关键词。

        参数：
            keyword: 要匹配的关键词

        返回：
            如果匹配返回True，否则返回False
        """
        if (self.current_token is not None and
                self.current_token.type == 'KEYWORD' and
                self.current_token.value == keyword):
            self.next_token()
            return True
        return False

    def next_token(self) -> None:
        """前进到下一个标记。"""
        self.token_index += 1
        if self.token_index < len(self.tokens):
            self.current_token = self.tokens[self.token_index]
        else:
            self.current_token = None

    def skip_to_next_function(self) -> None:
        """跳过标记直到下一个函数声明或标记结束。"""
        while self.current_token is not None:
            if (self.current_token.type == 'KEYWORD'
                    and self.current_token.value == 'function'):
                return
            self.next_token()

    def parse_statement(self) -> Optional[Any]:
        """解析语句。"""
        if not self.current_token:
            return None

        # 解析局部声明
        if self.current_token.type == 'KEYWORD' and self.current_token.value == 'local':
            return self.parse_local_declaration()

        # 目前跳过其他标记
        self.next_token()
        return None

    def parse_local_declaration(self) -> Optional[LocalDecl]:
        """解析局部变量声明。"""
        try:
            # 跳过'local'关键词
            self.next_token()

            # 获取变量类型（可以是关键词如'integer'或标识符）
            if not self.current_token:
                return None
            var_type = self.current_token.value
            self.next_token()

            # 获取变量名
            if not self.current_token or self.current_token.type != 'IDENTIFIER':
                return None
            var_name = self.current_token.value
            self.next_token()

            # 检查赋值
            value = None
            if self.current_token and self.current_token.value == '=':
                self.next_token()
                # 解析表达式（简化）
                if self.current_token:
                    if self.current_token.type == 'NUMBER':
                        value = int(self.current_token.value)
                    elif self.current_token.type == 'STRING':
                        value = self.current_token.value[1:-1]  # 移除引号
                    self.next_token()

            # 如果存在分号则跳过
            if self.current_token and self.current_token.value == ';':
                self.next_token()

            return LocalDecl(name=var_name, type=var_type, value=value)

        except Exception:
            return None
