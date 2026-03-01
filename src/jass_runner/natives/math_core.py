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
