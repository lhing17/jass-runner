from typing import Optional, TYPE_CHECKING, Any
from .ast_nodes import LocalDecl, NativeCallNode, SetStmt, ArrayDecl, SetArrayStmt
from .errors import ParseError

if TYPE_CHECKING:
    from .base_parser import BaseParser

class AssignmentParserMixin:
    """提供赋值和调用语句解析功能。"""

    def _parse_call_args(self: 'BaseParser', error_on_unknown: bool = False) -> list:
        """解析函数调用参数列表，支持嵌套调用和复杂表达式。

        前置条件：当前 token 是 '(' 后的第一个参数token
        后置条件：当前 token 是 ')'

        参数：
            error_on_unknown: 遇到不支持的类型时是否记录错误并继续解析
                            如果为False（默认），则遇到不支持的类型时停止解析

        返回：
            参数列表，支持嵌套 NativeCallNode 和表达式字符串
        """
        from .ast_nodes import NativeCallNode

        args = []

        while self.current_token and self.current_token.value != ')':
            arg_value = self._parse_single_arg(error_on_unknown)
            if arg_value is not None:
                args.append(arg_value)
            # 检查是否有逗号继续下一个参数，或者遇到右括号结束
            if self.current_token and self.current_token.value == ',':
                self.next_token()
            elif self.current_token and self.current_token.value == ')':
                break
        return args

    def _parse_single_arg(self: 'BaseParser', error_on_unknown: bool = False) -> Any:
        """解析单个参数，支持字面量、变量、嵌套调用和复杂表达式。

        返回：
            解析后的参数值（字符串字面量、数值字符串、NativeCallNode或表达式字符串）
        """
        from .ast_nodes import NativeCallNode

        # 收集当前参数的所有token，直到遇到逗号或右括号
        arg_tokens = []
        current_func_name = None
        paren_depth = 0

        while self.current_token and self.current_token.value != ')' and self.current_token.value != ',':
            token = self.current_token

            # 遇到嵌套函数调用：标识符 + 左括号
            if token.type == 'IDENTIFIER' and self._peek_token() == '(':
                func_name = token.value
                self.next_token()  # 越过标识符
                self.next_token()  # 越过左括号

                # 递归解析嵌套参数
                nested_args = self._parse_call_args(error_on_unknown)

                # 跳过右括号
                if self.current_token and self.current_token.value == ')':
                    self.next_token()

                # 创建 NativeCallNode 并作为token处理
                arg_tokens.append(NativeCallNode(func_name=func_name, args=nested_args))
                continue

            # 遇到数组访问：标识符 + 左方括号
            if token.type == 'IDENTIFIER' and self._peek_token() == '[':
                from .ast_nodes import ArrayAccess
                array_name = token.value
                self.next_token()  # 越过标识符
                self.next_token()  # 越过 '['

                # 解析索引
                index = None
                if self.current_token:
                    if self.current_token.type == 'INTEGER':
                        from .ast_nodes import IntegerExpr
                        index = IntegerExpr(value=self.current_token.value)
                        self.next_token()
                    elif self.current_token.type == 'IDENTIFIER':
                        from .ast_nodes import VariableExpr
                        index = VariableExpr(name=self.current_token.value)
                        self.next_token()

                # 跳过右方括号
                if self.current_token and self.current_token.value == ']':
                    self.next_token()

                # 创建 ArrayAccess 节点
                arg_tokens.append(ArrayAccess(array_name=array_name, index=index))
                continue

            # 遇到左括号（不是函数调用，而是表达式的一部分）
            if token.value == '(':
                paren_depth += 1
                arg_tokens.append(str(token.value))
                self.next_token()
                continue

            # 遇到右括号
            if token.value == ')':
                if paren_depth > 0:
                    paren_depth -= 1
                    arg_tokens.append(str(token.value))
                    self.next_token()
                    continue
                # 否则是参数结束，退出循环
                break

            # 收集token值
            if token.type == 'IDENTIFIER' or (token.type == 'KEYWORD' and token.value == 'function'):
                arg_tokens.append(str(token.value))
            else:
                arg_tokens.append(str(token.value))
            self.next_token()

        # 处理收集的token
        if not arg_tokens:
            return None

        # 如果只有一个token且是NativeCallNode或ArrayAccess，直接返回
        if len(arg_tokens) == 1:
            token = arg_tokens[0]
            if hasattr(token, 'func_name') or type(token).__name__ == 'ArrayAccess':
                return token
            # 尝试解析为数字
            try:
                return str(int(token))
            except ValueError:
                try:
                    return str(float(token))
                except ValueError:
                    # 不是数字，直接返回原值（保留字符串引号）
                    return token

        # 多个token：检查是否是函数引用（function FuncName）
        if len(arg_tokens) == 2 and arg_tokens[0] == 'function':
            # 函数引用：返回 "function:FuncName" 格式
            return f"function:{arg_tokens[1]}"

        # 多个token：组合成混合列表（字符串和NativeCallNode）
        # 这样可以保留嵌套函数调用供evaluator处理
        result = []
        for t in arg_tokens:
            if hasattr(t, 'func_name'):
                # NativeCallNode 保留原样
                result.append(t)
            else:
                result.append(str(t))
        return result

    def _peek_token(self: 'BaseParser') -> Optional[str]:
        """查看下一个token的值，不移动当前位置。"""
        if not hasattr(self, 'tokens') or self.token_index + 1 >= len(self.tokens):
            return None
        return self.tokens[self.token_index + 1].value

    def parse_local_declaration(self: 'BaseParser') -> Optional[Any]:
        """解析局部变量声明。

        格式: local <type> [array] <name> [= <value>]
        注意: array声明不支持初始化
        """
        try:
            # 跳过'local'关键词
            self.next_token()

            # 获取变量类型（可以是关键词如'integer'或标识符）
            if not self.current_token:
                return None
            var_type = self.current_token.value
            self.next_token()

            # 检查是否是数组声明
            is_array = False
            if self.current_token and self.current_token.type == 'KEYWORD' and \
               self.current_token.value == 'array':
                is_array = True
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

            # 数组声明不支持初始化
            if is_array:
                if self.current_token and self.current_token.value == '=':
                    self.errors.append(ParseError(
                        message="数组声明不支持初始化",
                        line=self.current_token.line if self.current_token else 0,
                        column=self.current_token.column if self.current_token else 0
                    ))
                    return None
                # 如果存在分号则跳过
                if self.current_token and self.current_token.value == ';':
                    self.next_token()
                return ArrayDecl(
                    name=var_name,
                    element_type=var_type,
                    is_global=False
                )

            # 检查赋值（普通变量）
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
                    elif self.current_token.type == 'KEYWORD' and self.current_token.value in ('true', 'false'):
                        # 布尔值
                        value = self.current_token.value
                        self.next_token()
                    elif self.current_token.type == 'IDENTIFIER' or (self.current_token.type == 'KEYWORD' and self.current_token.value in self.TYPE_KEYWORDS):
                        # 可能是函数调用，如 CreateUnit(...) 或 CreateForce()
                        # 注意：类型关键词（如 force）在函数名位置也应被视为标识符
                        func_name = self.current_token.value
                        self.next_token()

                        if self.current_token and self.current_token.value == '(':
                            # 这是一个函数调用
                            self.next_token()  # 跳过 '('

                            # 使用 _parse_call_args 解析参数列表，支持嵌套调用
                            args = self._parse_call_args()

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

    def parse_call_statement(self: 'BaseParser') -> Optional[NativeCallNode]:
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

            # 使用 _parse_call_args 解析参数列表
            args = self._parse_call_args()

            # 检查右括号
            if self.current_token and self.current_token.value == ')':
                self.next_token()

            # 如果存在分号则跳过
            if self.current_token and self.current_token.value == ';':
                self.next_token()

            return NativeCallNode(func_name=func_name, args=args)

        except Exception:
            return None

    def _parse_array_access_expression(self: 'BaseParser', array_name: str) -> Optional[Any]:
        """解析数组访问表达式 [index]。

        参数：
            array_name: 数组名称

        返回：
            ArrayAccess节点或None（如果解析失败）
        """
        from .ast_nodes import ArrayAccess

        # 当前token是'['
        self.next_token()  # 跳过 '['

        # 解析索引表达式（简化：支持字面量和变量）
        index = None
        if self.current_token:
            if self.current_token.type == 'INTEGER':
                from .ast_nodes import IntegerExpr
                index = IntegerExpr(value=self.current_token.value)
                self.next_token()
            elif self.current_token.type == 'IDENTIFIER':
                from .ast_nodes import VariableExpr
                index = VariableExpr(name=self.current_token.value)
                self.next_token()

        # 期望 ']'
        if not self.current_token or self.current_token.value != ']':
            self.errors.append(ParseError(
                message="期望']'结束数组索引",
                line=self.current_token.line if self.current_token else 0,
                column=self.current_token.column if self.current_token else 0
            ))
            return None
        self.next_token()  # 跳过 ']'

        return ArrayAccess(array_name=array_name, index=index)

    def _parse_set_array_statement(self: 'BaseParser', array_name: str) -> Optional[SetArrayStmt]:
        """解析数组元素赋值语句。

        参数：
            array_name: 数组名称

        返回：
            SetArrayStmt节点或None（如果解析失败）
        """
        from .ast_nodes import SetArrayStmt, IntegerExpr, VariableExpr

        # 当前token是'['
        self.next_token()  # 跳过 '['

        # 解析索引表达式
        index = None
        if self.current_token:
            if self.current_token.type == 'INTEGER':
                index = IntegerExpr(value=self.current_token.value)
                self.next_token()
            elif self.current_token.type == 'IDENTIFIER':
                index = VariableExpr(name=self.current_token.value)
                self.next_token()

        # 期望']'
        if not self.current_token or self.current_token.value != ']':
            self.errors.append(ParseError(
                message="数组赋值期望']'",
                line=self.current_token.line if self.current_token else 0,
                column=self.current_token.column if self.current_token else 0
            ))
            return None
        self.next_token()  # 跳过 ']'

        # 期望'='
        if not self.current_token or self.current_token.value != '=':
            self.errors.append(ParseError(
                message="数组赋值期望'='",
                line=self.current_token.line if self.current_token else 0,
                column=self.current_token.column if self.current_token else 0
            ))
            return None
        self.next_token()  # 跳过 '='

        # 解析右侧值
        value = None
        if self.current_token:
            if self.current_token.type == 'INTEGER':
                value = IntegerExpr(value=self.current_token.value)
                self.next_token()
            elif self.current_token.type == 'IDENTIFIER' or (self.current_token.type == 'KEYWORD' and self.current_token.value in self.TYPE_KEYWORDS):
                # 可能是函数调用或变量引用
                # 注意：类型关键词（如 force）在函数名位置也应被视为标识符
                expr_name = self.current_token.value
                self.next_token()

                if self.current_token and self.current_token.value == '(':
                    # 这是一个函数调用
                    self.next_token()  # 跳过 '('

                    # 使用 _parse_call_args 解析参数列表
                    args = self._parse_call_args()

                    # 跳过右括号
                    if self.current_token and self.current_token.value == ')':
                        self.next_token()

                    value = NativeCallNode(func_name=expr_name, args=args)
                else:
                    # 不是函数调用，作为变量引用
                    value = VariableExpr(name=expr_name)

        # 如果存在分号则跳过
        if self.current_token and self.current_token.value == ';':
            self.next_token()

        return SetArrayStmt(
            array_name=array_name,
            index=index,
            value=value
        )

    def parse_set_statement(self: 'BaseParser') -> Optional[SetStmt]:
        """解析set赋值语句。"""
        try:
            # 跳过'set'关键词
            self.next_token()

            # 获取变量名
            if not self.current_token or self.current_token.type != 'IDENTIFIER':
                return None
            var_name = self.current_token.value
            self.next_token()

            # 检查是否是数组赋值 arr[...] = ...
            if self.current_token and self.current_token.value == '[':
                return self._parse_set_array_statement(var_name)

            # 检查是否尝试修改常量（普通变量）
            if hasattr(self, 'constant_names') and var_name in self.constant_names:
                self.errors.append(ParseError(
                    message=f"不能修改常量 '{var_name}'",
                    line=self.current_token.line if self.current_token else 0,
                    column=self.current_token.column if self.current_token else 0
                ))
                # 继续消耗token以同步，但返回None表示解析失败
                if self.current_token and self.current_token.value == '=':
                    self.next_token()
                    # 跳过右侧值
                    while (self.current_token and
                           not (self.current_token.type == 'KEYWORD' and
                                self.current_token.value in ('set', 'call', 'local', 'return',
                                                             'exitwhen', 'loop', 'if', 'elseif',
                                                             'else', 'endif', 'endloop', 'endfunction'))):
                        self.next_token()
                return None

            # 检查赋值操作符
            if not self.current_token or self.current_token.value != '=':
                return None
            self.next_token()

            # 解析右侧值（可以是字面量、函数调用、数组访问或表达式）
            value = None
            if self.current_token and (self.current_token.type == 'IDENTIFIER' or
                                       (self.current_token.type == 'KEYWORD' and self.current_token.value in self.TYPE_KEYWORDS)):
                # 可能是函数调用，如 CreateUnit(...)，数组访问如 arr[0]，或表达式如 i + 1
                # 注意：类型关键词（如 force）在函数名位置也应被视为标识符
                expr_name = self.current_token.value
                self.next_token()

                # 检查是否是数组访问 arr[...]
                if self.current_token and self.current_token.value == '[':
                    value = self._parse_array_access_expression(expr_name)
                elif self.current_token and self.current_token.value == '(':
                    # 这是一个函数调用
                    self.next_token()  # 跳过 '('

                    # 使用 _parse_call_args 解析参数列表
                    args = self._parse_call_args()

                    # 跳过右括号
                    if self.current_token and self.current_token.value == ')':
                        self.next_token()

                    value = NativeCallNode(func_name=expr_name, args=args)
                elif self.current_token and self.current_token.type == 'OPERATOR':
                    # 不是函数调用，但是表达式开始（如 i + 1）
                    # 将标识符和后续token组合成表达式字符串
                    expr_parts = [expr_name]
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
                    value = expr_name
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
                elif self.current_token.type == 'KEYWORD' and self.current_token.value in ('true', 'false'):
                    # 布尔值
                    value = self.current_token.value
                    self.next_token()

            # 如果存在分号则跳过
            if self.current_token and self.current_token.value == ';':
                self.next_token()

            return SetStmt(var_name=var_name, value=value)

        except Exception:
            return None
