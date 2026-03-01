"""数学基础Native函数实现。

此模块包含JASS基础数学native函数的实现，如SquareRoot等。
"""

import math
from .base import NativeFunction


class SquareRoot(NativeFunction):
    """计算平方根。

    此函数模拟JASS中的SquareRoot native函数，计算一个实数的平方根。
    对于负数输入，返回0（与JASS行为一致）。
    """

    @property
    def name(self) -> str:
        """获取函数名称。

        返回：
            函数名称"SquareRoot"
        """
        return "SquareRoot"

    def execute(self, state_context, r: float) -> float:
        """执行SquareRoot native函数。

        参数：
            state_context: 状态上下文
            r: 要计算平方根的实数

        返回：
            float: r的平方根，如果r为负数则返回0.0
        """
        if r < 0:
            return 0.0
        return math.sqrt(r)


class Pow(NativeFunction):
    """计算幂运算。

    此函数模拟JASS中的Pow native函数，计算x的power次方。
    支持正指数、负指数、零指数和分数指数。
    """

    @property
    def name(self) -> str:
        """获取函数名称。

        返回：
            函数名称"Pow"
        """
        return "Pow"

    def execute(self, state_context, x: float, power: float) -> float:
        """执行Pow native函数。

        参数：
            state_context: 状态上下文
            x: 底数
            power: 指数

        返回：
            float: x的power次方
        """
        return math.pow(x, power)


class Cos(NativeFunction):
    """计算余弦值。

    此函数模拟JASS中的Cos native函数，计算一个实数的余弦值。
    JASS使用弧度制，与Python math.cos一致。
    """

    @property
    def name(self) -> str:
        """获取函数名称。

        返回：
            函数名称"Cos"
        """
        return "Cos"

    def execute(self, state_context, r: float) -> float:
        """执行Cos native函数。

        参数：
            state_context: 状态上下文
            r: 弧度值

        返回：
            float: r的余弦值
        """
        return math.cos(r)


class Sin(NativeFunction):
    """计算正弦值。

    此函数模拟JASS中的Sin native函数，计算一个实数的正弦值。
    JASS使用弧度制，与Python math.sin一致。
    """

    @property
    def name(self) -> str:
        """获取函数名称。

        返回：
            函数名称"Sin"
        """
        return "Sin"

    def execute(self, state_context, r: float) -> float:
        """执行Sin native函数。

        参数：
            state_context: 状态上下文
            r: 弧度值

        返回：
            float: r的正弦值
        """
        return math.sin(r)
