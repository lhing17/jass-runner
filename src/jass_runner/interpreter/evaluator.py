"""JASS表达式求值器。"""

from typing import Any
from .context import ExecutionContext


class Evaluator:
    """求值JASS表达式。"""

    def __init__(self, context: ExecutionContext):
        self.context = context

    def evaluate(self, expression: str) -> Any:
        """求值一个JASS表达式。"""
        expression = expression.strip()

        # 处理字符串字面量
        if expression.startswith('"') and expression.endswith('"'):
            return expression[1:-1]

        # 处理整数字面量
        if expression.isdigit():
            return int(expression)

        # 处理浮点数字面量
        try:
            return float(expression)
        except ValueError:
            pass

        # 处理变量引用
        if self.context.has_variable(expression):
            return self.context.get_variable(expression)

        # 默认：作为字符串返回
        return expression