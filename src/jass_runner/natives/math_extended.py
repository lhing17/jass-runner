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
