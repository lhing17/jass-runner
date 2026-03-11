from typing import Optional, TYPE_CHECKING, Any
if TYPE_CHECKING:
    from .base_parser import BaseParser
    from .lexer import Token

class ExpressionParserMixin:
    """提供条件表达式解析功能。"""

    def parse_condition(self: 'BaseParser') -> Optional[str]:
        """解析条件表达式（支持比较操作符、逻辑运算符和嵌套函数调用）。

        返回：
            条件表达式字符串，如果解析失败返回None
        """
        if not self.current_token:
            return None

        # 解析表达式（支持嵌套）
        result = self._parse_expression(0)
        return result

    def _parse_expression(self: 'BaseParser', min_precedence: int) -> Optional[str]:
        """使用递归下降算法解析表达式，支持运算符优先级。

        参数：
            min_precedence: 最小优先级，用于处理运算符优先级

        返回：
            表达式字符串
        """
        # 解析左侧操作数（一元运算符或基本表达式）
        left = self._parse_unary()
        if left is None:
            return None

        # 处理二元运算符（比较运算符和逻辑运算符）
        while True:
            # 获取当前运算符优先级
            op = self._get_current_operator()
            if op is None:
                break

            precedence = self._get_operator_precedence(op)
            if precedence < min_precedence:
                break

            # 消费运算符
            self.next_token()

            # 解析右侧操作数
            right = self._parse_expression(precedence + 1)
            if right is None:
                break

            # 组合表达式
            left = f"{left} {op} {right}"

        return left

    def _parse_unary(self: 'BaseParser') -> Optional[str]:
        """解析一元表达式（not、括号、函数调用等）。

        返回：
            表达式字符串
        """
        if not self.current_token:
            return None

        # 处理一元运算符 not
        if (self.current_token.type == 'KEYWORD' and
            self.current_token.value == 'not'):
            self.next_token()  # 跳过 'not'
            operand = self._parse_unary()  # 递归解析操作数
            if operand is None:
                return None
            return f"not {operand}"

        # 处理括号表达式
        if self.current_token.value == '(':
            self.next_token()  # 跳过 '('
            expr = self._parse_expression(0)
            # 跳过右括号
            if self.current_token and self.current_token.value == ')':
                self.next_token()
            return expr

        # 处理布尔值 true/false
        if (self.current_token.type == 'KEYWORD' and
            self.current_token.value in ('true', 'false')):
            value = self.current_token.value
            self.next_token()
            return value

        # 处理标识符（变量或函数调用）
        if self.current_token.type == 'IDENTIFIER':
            return self._parse_identifier_or_call()

        # 处理整数和实数字面量
        if self.current_token.type in ('INTEGER', 'REAL'):
            value = str(self.current_token.value)
            self.next_token()
            return value

        # 处理字符串字面量
        if self.current_token.type == 'STRING':
            value = str(self.current_token.value)
            self.next_token()
            return value

        return None

    def _parse_identifier_or_call(self: 'BaseParser') -> Optional[str]:
        """解析标识符、函数调用或数组访问。

        返回：
            标识符名称、函数调用字符串或数组访问字符串
        """
        if not self.current_token or self.current_token.type != 'IDENTIFIER':
            return None

        name = self.current_token.value
        self.next_token()

        # 检查是否是数组访问
        if self.current_token and self.current_token.value == '[':
            self.next_token()  # 跳过 '['
            # 解析索引
            index = self._parse_expression(0)
            # 跳过右方括号
            if self.current_token and self.current_token.value == ']':
                self.next_token()
            return f"{name}[{index}]"

        # 检查是否是函数调用
        if self.current_token and self.current_token.value == '(':
            # 解析函数调用参数
            args = self._parse_call_args_for_condition()
            if args:
                return f"{name}({', '.join(args)})"
            else:
                return f"{name}()"

        return name

    def _parse_call_args_for_condition(self: 'BaseParser') -> list:
        """为条件表达式解析函数调用参数列表。

        前置条件：当前 token 是 '('
        返回：
            参数字符串列表
        """
        if not self.current_token or self.current_token.value != '(':
            return []

        self.next_token()  # 跳过 '('

        args = []
        while self.current_token and self.current_token.value != ')':
            # 解析单个参数
            arg = self._parse_arg_for_condition()
            if arg is not None:
                args.append(arg)

            # 检查是否有逗号继续下一个参数
            if self.current_token and self.current_token.value == ',':
                self.next_token()
            elif self.current_token and self.current_token.value == ')':
                break
            elif not self.current_token:
                break

        # 跳过右括号
        if self.current_token and self.current_token.value == ')':
            self.next_token()

        return args

    def _parse_arg_for_condition(self: 'BaseParser') -> Optional[str]:
        """为条件表达式解析单个参数。

        返回：
            参数字符串表示
        """
        if not self.current_token:
            return None

        tokens = []

        # 处理嵌套函数调用
        if (self.current_token.type == 'IDENTIFIER' and
            self._peek_token() == '('):
            func_name = self.current_token.value
            self.next_token()  # 跳过函数名
            nested_args = self._parse_call_args_for_condition()
            if nested_args:
                return f"{func_name}({', '.join(nested_args)})"
            else:
                return f"{func_name}()"

        # 收集普通token直到遇到逗号或右括号
        while (self.current_token and
               self.current_token.value not in (',', ')')):

            token = self.current_token

            # 处理括号内的表达式
            if token.value == '(':
                self.next_token()
                nested = self._parse_expression(0)
                if self.current_token and self.current_token.value == ')':
                    self.next_token()
                if nested:
                    tokens.append(f"({nested})")
                continue

            # 处理布尔值
            if token.type == 'KEYWORD' and token.value in ('true', 'false', 'not'):
                tokens.append(token.value)
                self.next_token()
                continue

            # 处理普通token
            if token.type == 'STRING':
                tokens.append(str(token.value))
            elif token.type in ('INTEGER', 'REAL'):
                tokens.append(str(token.value))
            else:
                tokens.append(str(token.value))
            self.next_token()

        # 组合token
        if not tokens:
            return None

        return ' '.join(tokens)

    def _get_current_operator(self: 'BaseParser') -> Optional[str]:
        """获取当前位置的运算符（如果有）。

        返回：
            运算符字符串，如果不是运算符则返回None
        """
        if not self.current_token:
            return None

        # 比较运算符
        if self.current_token.type == 'OPERATOR':
            return self.current_token.value

        # 逻辑运算符
        if (self.current_token.type == 'KEYWORD' and
            self.current_token.value in ('and', 'or')):
            return self.current_token.value

        return None

    def _get_operator_precedence(self, op: str) -> int:
        """获取运算符优先级。

        参数：
            op: 运算符

        返回：
            优先级数字（越大优先级越高）
        """
        precedence = {
            'or': 1,
            'and': 2,
            '==': 3, '!=': 3,
            '<': 4, '>': 4, '<=': 4, '>=': 4,
        }
        return precedence.get(op, 0)

    def _peek_token(self: 'BaseParser') -> Optional[str]:
        """查看下一个token的值，不移动当前位置。"""
        if not hasattr(self, 'tokens') or self.token_index + 1 >= len(self.tokens):
            return None
        return self.tokens[self.token_index + 1].value
