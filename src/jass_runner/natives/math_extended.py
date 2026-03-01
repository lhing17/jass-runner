"""数学扩展Native函数实现。

此模块包含JASS扩展数学native函数的实现，如Tan等三角函数。
"""

import math
from .base import NativeFunction


class Tan(NativeFunction):
    """计算正切值。

    此函数模拟JASS中的Tan native函数，计算一个实数的正切值。
    JASS使用弧度制，与Python math.tan一致。
    """

    @property
    def name(self) -> str:
        """获取函数名称。

        返回：
            函数名称"Tan"
        """
        return "Tan"

    def execute(self, state_context, r: float) -> float:
        """执行Tan native函数。

        参数：
            state_context: 状态上下文
            r: 弧度值

        返回：
            float: r的正切值
        """
        return math.tan(r)


class ModuloInteger(NativeFunction):
    """计算整数模运算。

    此函数模拟JASS中的ModuloInteger native函数，计算两个整数的余数。
    当除数为0时，返回0以避免异常。
    """

    @property
    def name(self) -> str:
        """获取函数名称。

        返回：
            函数名称"ModuloInteger"
        """
        return "ModuloInteger"

    def execute(self, state_context, a: int, b: int) -> int:
        """执行ModuloInteger native函数。

        参数：
            state_context: 状态上下文
            a: 被除数
            b: 除数

        返回：
            int: a % b的余数，如果b为0则返回0
        """
        if b == 0:
            return 0
        return a % b


class ModuloReal(NativeFunction):
    """计算实数模运算。

    此函数模拟JASS中的ModuloReal native函数，计算两个实数的余数。
    当除数为0时，返回0.0以避免异常。
    """

    @property
    def name(self) -> str:
        """获取函数名称。

        返回：
            函数名称"ModuloReal"
        """
        return "ModuloReal"

    def execute(self, state_context, a: float, b: float) -> float:
        """执行ModuloReal native函数。

        参数：
            state_context: 状态上下文
            a: 被除数
            b: 除数

        返回：
            float: a % b的余数，如果b为0则返回0.0
        """
        if b == 0:
            return 0.0
        return a % b
