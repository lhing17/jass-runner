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
class GlobalDecl:
    """全局变量声明节点。"""
    name: str
    type: str
    value: Any  # 初始值，可能为None


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
    globals: List[GlobalDecl] = None  # 全局变量声明列表

    def __post_init__(self):
        """初始化默认值。"""
        if self.globals is None:
            self.globals = []

@dataclass
class NativeCallNode:
    """原生函数调用节点。"""
    func_name: str
    args: List[Any]


@dataclass
class SetStmt:
    """变量赋值语句节点。"""
    var_name: str
    value: Any  # 可以是字面量或函数调用节点


@dataclass
class IfStmt:
    """if语句节点。"""
    condition: str  # 条件表达式
    then_body: List[Any]  # then分支的语句列表
    elseif_branches: List[dict] = None  # elseif分支列表，每个元素是{"condition": str, "body": List[Any]}
    else_body: List[Any] = None  # else分支的语句列表

    def __post_init__(self):
        """初始化默认值。"""
        if self.elseif_branches is None:
            self.elseif_branches = []
        if self.else_body is None:
            self.else_body = []


@dataclass
class LoopStmt:
    """loop循环语句节点。"""
    body: List[Any]  # 循环体内的语句列表


@dataclass
class ExitWhenStmt:
    """exitwhen循环退出语句节点。"""
    condition: str  # 退出条件表达式


@dataclass
class ReturnStmt:
    """return返回语句节点。"""
    value: Optional[Any]  # 返回值，如果是return nothing则为None


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

    def parse_globals_block(self) -> List[GlobalDecl]:
        """解析可选的globals块。

        返回：
            如果存在globals块返回GlobalDecl列表，否则返回空列表
        """
        globals_list = []

        # 检查是否存在 globals 关键字
        if not self.current_token or not (self.current_token.type == 'KEYWORD' and self.current_token.value == 'globals'):
            return globals_list

        # 跳过 'globals' 关键字
        self.next_token()

        # 解析变量声明列表直到 endglobals
        while (self.current_token and
               not (self.current_token.type == 'KEYWORD' and self.current_token.value == 'endglobals')):
            global_decl = self.parse_global_declaration()
            if global_decl:
                globals_list.append(global_decl)

        # 跳过 'endglobals' 关键字
        if self.current_token and self.current_token.type == 'KEYWORD' and self.current_token.value == 'endglobals':
            self.next_token()

        return globals_list

    def parse_global_declaration(self) -> Optional[GlobalDecl]:
        """解析单个全局变量声明。

        格式: <type> <name> [= <initial_value>]

        返回：
            GlobalDecl节点或None（如果解析失败）
        """
        try:
            # 获取变量类型
            if not self.current_token:
                return None

            var_type = self.current_token.value
            if var_type not in self.TYPE_KEYWORDS:
                return None
            self.next_token()

            # 获取变量名
            if not self.current_token or self.current_token.type != 'IDENTIFIER':
                return None
            var_name = self.current_token.value

            self.next_token()

            # 检查可选的初始值
            value = None
            if self.current_token and self.current_token.value == '=':
                self.next_token()
                if self.current_token:
                    if self.current_token.type == 'INTEGER':
                        value = self.current_token.value
                        self.next_token()
                    elif self.current_token.type == 'REAL':
                        value = self.current_token.value
                        self.next_token()
                    elif self.current_token.type == 'STRING':
                        value = self.current_token.value[1:-1]  # 移除引号
                        self.next_token()
                    elif self.current_token.type == 'KEYWORD' and self.current_token.value in ('true', 'false'):
                        value = self.current_token.value == 'true'
                        self.next_token()

            return GlobalDecl(name=var_name, type=var_type, value=value)

        except Exception:
            return None

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

            # 检查是否与全局变量同名（局部变量不能与全局变量同名）
            if hasattr(self, 'global_names') and var_name in self.global_names:
                self.errors.append(ParseError(
                    message=f"局部变量 '{var_name}' 与全局变量同名",
                    line=self.current_token.line,
                    column=self.current_token.column
                ))
                return None

            self.next_token()

            # 检查赋值
            value = None
            if self.current_token and self.current_token.value == '=':
                self.next_token()
                # 解析表达式
                if self.current_token:
                    if self.current_token.type == 'INTEGER':
                        value = self.current_token.value
                        self.next_token()
                    elif self.current_token.type == 'REAL':
                        value = self.current_token.value
                        self.next_token()
                    elif self.current_token.type == 'STRING':
                        value = self.current_token.value[1:-1]  # 移除引号
                        self.next_token()
                    elif self.current_token.type == 'IDENTIFIER':
                        # 可能是函数调用，如 CreateUnit(...)
                        func_name = self.current_token.value
                        self.next_token()

                        if self.current_token and self.current_token.value == '(':
                            # 这是一个函数调用
                            self.next_token()  # 跳过 '('

                            # 解析参数列表
                            args = []
                            while self.current_token and self.current_token.value != ')':
                                if self.current_token.type == 'INTEGER':
                                    args.append(str(self.current_token.value))
                                elif self.current_token.type == 'REAL':
                                    args.append(str(self.current_token.value))
                                elif self.current_token.type == 'STRING':
                                    args.append(self.current_token.value)
                                elif self.current_token.type == 'IDENTIFIER':
                                    args.append(self.current_token.value)
                                elif self.current_token.type == 'FOURCC':
                                    args.append(str(self.current_token.value))

                                self.next_token()

                                # 检查是否有逗号
                                if self.current_token and self.current_token.value == ',':
                                    self.next_token()
                                    continue
                                elif self.current_token and self.current_token.value == ')':
                                    break

                            # 跳过右括号
                            if self.current_token and self.current_token.value == ')':
                                self.next_token()

                            value = NativeCallNode(func_name=func_name, args=args)
                        else:
                            # 不是函数调用，作为变量引用处理（暂不支持）
                            value = None

            # 如果存在分号则跳过
            if self.current_token and self.current_token.value == ';':
                self.next_token()

            return LocalDecl(name=var_name, type=var_type, value=value)

        except Exception:
            return None

    def parse_call_statement(self) -> Optional[NativeCallNode]:
        """解析call语句。"""
        try:
            # 跳过'call'关键词
            self.next_token()

            # 获取函数名
            if not self.current_token or self.current_token.type != 'IDENTIFIER':
                return None
            func_name = self.current_token.value
            self.next_token()

            # 检查左括号
            if not self.current_token or self.current_token.value != '(':
                return None
            self.next_token()

            # 解析参数列表
            args = []
            while self.current_token and self.current_token.value != ')':
                # 解析参数表达式（简化：字面量或标识符）
                arg_value = None
                if self.current_token.type == 'INTEGER':
                    arg_value = self.current_token.value
                    args.append(str(arg_value))  # 转换为字符串以便求值器处理
                    self.next_token()
                elif self.current_token.type == 'REAL':
                    arg_value = self.current_token.value
                    args.append(str(arg_value))  # 转换为字符串以便求值器处理
                    self.next_token()
                elif self.current_token.type == 'STRING':
                    arg_value = self.current_token.value  # 保留引号以便求值器识别字符串字面量
                    args.append(arg_value)
                    self.next_token()
                elif self.current_token.type == 'IDENTIFIER':
                    arg_value = self.current_token.value
                    self.next_token()

                    # 检查是否是嵌套函数调用
                    if self.current_token and self.current_token.value == '(':
                        # 这是一个嵌套函数调用
                        self.next_token()  # 跳过 '('

                        # 解析嵌套函数的参数列表
                        nested_args = []
                        while self.current_token and self.current_token.value != ')':
                            if self.current_token.type == 'INTEGER':
                                nested_args.append(str(self.current_token.value))
                            elif self.current_token.type == 'REAL':
                                nested_args.append(str(self.current_token.value))
                            elif self.current_token.type == 'STRING':
                                nested_args.append(self.current_token.value)
                            elif self.current_token.type == 'IDENTIFIER':
                                nested_args.append(self.current_token.value)
                            elif self.current_token.type == 'FOURCC':
                                nested_args.append(str(self.current_token.value))

                            self.next_token()

                            # 检查是否有逗号
                            if self.current_token and self.current_token.value == ',':
                                self.next_token()
                                continue
                            elif self.current_token and self.current_token.value == ')':
                                break

                        # 跳过右括号
                        if self.current_token and self.current_token.value == ')':
                            self.next_token()

                        # 创建嵌套函数调用节点
                        arg_value = NativeCallNode(func_name=arg_value, args=nested_args)

                    args.append(arg_value)
                elif self.current_token.type == 'KEYWORD' and self.current_token.value in ('true', 'false'):
                    # 布尔值
                    arg_value = self.current_token.value
                    args.append(arg_value)
                    self.next_token()
                elif self.current_token.type == 'KEYWORD' and self.current_token.value == 'function':
                    # 函数引用: function func_name
                    self.next_token()  # 跳过 'function'
                    if self.current_token and self.current_token.type == 'IDENTIFIER':
                        func_ref = self.current_token.value
                        args.append(f"function:{func_ref}")
                        self.next_token()
                    else:
                        # 函数引用后面必须有函数名
                        break
                else:
                    # 不支持的类型
                    break

                # 检查是否有逗号继续下一个参数
                if self.current_token and self.current_token.value == ',':
                    self.next_token()
                    continue
                elif self.current_token and self.current_token.value == ')':
                    break

            # 检查右括号
            if self.current_token and self.current_token.value == ')':
                self.next_token()

            # 如果存在分号则跳过
            if self.current_token and self.current_token.value == ';':
                self.next_token()

            return NativeCallNode(func_name=func_name, args=args)

        except Exception:
            return None

    def parse_set_statement(self) -> Optional[SetStmt]:
        """解析set赋值语句。"""
        try:
            # 跳过'set'关键词
            self.next_token()

            # 获取变量名
            if not self.current_token or self.current_token.type != 'IDENTIFIER':
                return None
            var_name = self.current_token.value

            self.next_token()

            # 检查赋值操作符
            if not self.current_token or self.current_token.value != '=':
                return None
            self.next_token()

            # 解析右侧值（可以是字面量、函数调用或表达式）
            value = None
            if self.current_token and self.current_token.type == 'IDENTIFIER':
                # 可能是函数调用，如 CreateUnit(...)，或表达式如 i + 1
                func_name = self.current_token.value
                self.next_token()

                if self.current_token and self.current_token.value == '(':
                    # 这是一个函数调用
                    self.next_token()  # 跳过 '('

                    # 解析参数列表
                    args = []
                    while self.current_token and self.current_token.value != ')':
                        if self.current_token.type == 'INTEGER':
                            args.append(str(self.current_token.value))
                        elif self.current_token.type == 'REAL':
                            args.append(str(self.current_token.value))
                        elif self.current_token.type == 'STRING':
                            args.append(self.current_token.value)
                        elif self.current_token.type == 'IDENTIFIER':
                            args.append(self.current_token.value)
                        elif self.current_token.type == 'FOURCC':
                            args.append(str(self.current_token.value))

                        self.next_token()

                        # 检查是否有逗号
                        if self.current_token and self.current_token.value == ',':
                            self.next_token()
                            continue
                        elif self.current_token and self.current_token.value == ')':
                            break

                    # 跳过右括号
                    if self.current_token and self.current_token.value == ')':
                        self.next_token()

                    value = NativeCallNode(func_name=func_name, args=args)
                elif self.current_token and self.current_token.type == 'OPERATOR':
                    # 不是函数调用，但是表达式开始（如 i + 1）
                    # 将标识符和后续token组合成表达式字符串
                    expr_parts = [func_name]
                    # 继续读取直到语句结束
                    # 停止条件：遇到语句结束符; 或下一个语句开始关键词
                    statement_keywords = ('endloop', 'endif', 'else', 'elseif', 'endfunction',
                                         'set', 'call', 'local', 'return', 'exitwhen', 'loop', 'if', 'elseif')
                    while (self.current_token and
                           not (self.current_token.type == 'KEYWORD' and
                                self.current_token.value in statement_keywords)):
                        if self.current_token.value == ';':
                            self.next_token()
                            break
                        expr_parts.append(str(self.current_token.value))
                        self.next_token()
                    value = ' '.join(expr_parts)
                else:
                    # 不是函数调用也不是表达式，只是变量引用
                    # 这种情况在JASS set语句中不常见，但保留处理
                    value = func_name
            elif self.current_token:
                # 字面量或表达式
                if self.current_token.type == 'INTEGER':
                    value = self.current_token.value
                    self.next_token()
                elif self.current_token.type == 'REAL':
                    value = self.current_token.value
                    self.next_token()
                elif self.current_token.type == 'STRING':
                    value = self.current_token.value[1:-1]
                    self.next_token()

            # 如果存在分号则跳过
            if self.current_token and self.current_token.value == ';':
                self.next_token()

            return SetStmt(var_name=var_name, value=value)

        except Exception:
            return None

    def parse_if_statement(self) -> Optional[IfStmt]:
        """解析if语句。

        返回：
            如果成功返回IfStmt，如果解析失败返回None
        """
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

    def parse_loop_statement(self) -> Optional[LoopStmt]:
        """解析loop循环语句。

        返回：
            如果成功返回LoopStmt，如果解析失败返回None
        """
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

    def parse_exitwhen_statement(self) -> Optional[ExitWhenStmt]:
        """解析exitwhen退出循环语句。

        返回：
            如果成功返回ExitWhenStmt，如果解析失败返回None
        """
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

    def parse_return_statement(self) -> Optional[ReturnStmt]:
        """解析return返回语句。

        返回：
            如果成功返回ReturnStmt，如果解析失败返回None
        """
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

    def parse_condition(self) -> Optional[str]:
        """解析条件表达式（支持比较操作符）。

        返回：
            条件表达式字符串，如果解析失败返回None
        """
        if not self.current_token:
            return None

        # 处理布尔值true/false
        if self.current_token.type == 'KEYWORD' and self.current_token.value in ('true', 'false'):
            condition = self.current_token.value
            self.next_token()
            return condition

        # 处理标识符（变量或函数调用）
        if self.current_token.type == 'IDENTIFIER':
            condition = self.current_token.value
            self.next_token()

            # 检查是否是函数调用，如 SomeFunction()
            if self.current_token and self.current_token.value == '(':
                self.next_token()  # 跳过 '('

                # 解析参数列表（简化处理）
                while self.current_token and self.current_token.value != ')':
                    self.next_token()

                # 跳过右括号
                if self.current_token and self.current_token.value == ')':
                    self.next_token()

                condition += "()"

            # 检查是否有比较操作符（如 >, <, ==, !=, >=, <=）
            if self.current_token and self.current_token.type == 'OPERATOR':
                op = self.current_token.value
                self.next_token()

                # 解析操作符右侧的操作数
                if self.current_token:
                    if self.current_token.type in ('INTEGER', 'REAL'):
                        condition += f" {op} {self.current_token.value}"
                        self.next_token()
                    elif self.current_token.type == 'IDENTIFIER':
                        condition += f" {op} {self.current_token.value}"
                        self.next_token()
                    elif self.current_token.type == 'STRING':
                        condition += f" {op} {self.current_token.value}"
                        self.next_token()

            return condition

        # 处理整数和实数字面量
        if self.current_token.type in ('INTEGER', 'REAL'):
            condition = str(self.current_token.value)
            self.next_token()

            # 检查是否有比较操作符
            if self.current_token and self.current_token.type == 'OPERATOR':
                op = self.current_token.value
                self.next_token()

                # 解析操作符右侧的操作数
                if self.current_token:
                    if self.current_token.type in ('INTEGER', 'REAL'):
                        condition += f" {op} {self.current_token.value}"
                        self.next_token()
                    elif self.current_token.type == 'IDENTIFIER':
                        condition += f" {op} {self.current_token.value}"
                        self.next_token()

            return condition

        # 处理字符串字面量
        if self.current_token.type == 'STRING':
            condition = self.current_token.value
            self.next_token()
            return condition

        return None
