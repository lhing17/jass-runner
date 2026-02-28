from typing import Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from .base_parser import BaseParser
    from .lexer import Token

class ExpressionParserMixin:
    """提供条件表达式解析功能。"""

    def parse_condition(self: 'BaseParser') -> Optional[str]:
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
