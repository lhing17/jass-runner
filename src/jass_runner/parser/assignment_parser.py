from typing import Optional, TYPE_CHECKING
from .ast_nodes import LocalDecl, NativeCallNode, SetStmt
from .errors import ParseError

if TYPE_CHECKING:
    from .base_parser import BaseParser

class AssignmentParserMixin:
    """提供赋值和调用语句解析功能。"""

    def parse_local_declaration(self: 'BaseParser') -> Optional[LocalDecl]:
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

    def parse_set_statement(self: 'BaseParser') -> Optional[SetStmt]:
        """解析set赋值语句。"""
        try:
            # 跳过'set'关键词
            self.next_token()

            # 获取变量名
            if not self.current_token or self.current_token.type != 'IDENTIFIER':
                return None
            var_name = self.current_token.value

            # 检查是否尝试修改常量
            if hasattr(self, 'constant_names') and var_name in self.constant_names:
                self.errors.append(ParseError(
                    message=f"不能修改常量 '{var_name}'",
                    line=self.current_token.line,
                    column=self.current_token.column
                ))
                # 继续消耗token以同步，但返回None表示解析失败
                self.next_token()
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
