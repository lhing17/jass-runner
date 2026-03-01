"""数学扩展Native函数实现。

此模块包含JASS扩展数学native函数的实现，如Tan等三角函数。
"""

import math
import random
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


class R2S(NativeFunction):
    """实数转字符串。

    此函数模拟JASS中的R2S native函数，将实数转换为字符串，
    格式化为3位小数。
    """

    @property
    def name(self) -> str:
        """获取函数名称。

        返回：
            函数名称"R2S"
        """
        return "R2S"

    def execute(self, state_context, r: float) -> str:
        """执行R2S native函数。

        参数：
            state_context: 状态上下文
            r: 要转换的实数

        返回：
            str: 格式化为3位小数的字符串
        """
        return f"{r:.3f}"


class S2R(NativeFunction):
    """字符串转实数。

    此函数模拟JASS中的S2R native函数，将字符串转换为实数。
    转换失败时返回0.0。
    """

    @property
    def name(self) -> str:
        """获取函数名称。

        返回：
            函数名称"S2R"
        """
        return "S2R"

    def execute(self, state_context, s: str) -> float:
        """执行S2R native函数。

        参数：
            state_context: 状态上下文
            s: 要转换的字符串

        返回：
            float: 转换后的实数，失败时返回0.0
        """
        try:
            return float(s)
        except (ValueError, TypeError):
            return 0.0


class I2S(NativeFunction):
    """整数转字符串。

    此函数模拟JASS中的I2S native函数，将整数转换为字符串。
    """

    @property
    def name(self) -> str:
        """获取函数名称。

        返回：
            函数名称"I2S"
        """
        return "I2S"

    def execute(self, state_context, i: int) -> str:
        """执行I2S native函数。

        参数：
            state_context: 状态上下文
            i: 要转换的整数

        返回：
            str: 转换后的字符串
        """
        return str(i)


class S2I(NativeFunction):
    """字符串转整数。

    此函数模拟JASS中的S2I native函数，将字符串转换为整数。
    转换失败时返回0。
    """

    @property
    def name(self) -> str:
        """获取函数名称。

        返回：
            函数名称"S2I"
        """
        return "S2I"

    def execute(self, state_context, s: str) -> int:
        """执行S2I native函数。

        参数：
            state_context: 状态上下文
            s: 要转换的字符串

        返回：
            int: 转换后的整数，失败时返回0
        """
        try:
            return int(float(s))
        except (ValueError, TypeError):
            return 0


class GetRandomInt(NativeFunction):
    """获取随机整数。

    此函数模拟JASS中的GetRandomInt native函数，在[low, high]范围内返回随机整数。
    如果high < low，返回low。
    """

    @property
    def name(self) -> str:
        """获取函数名称。

        返回：
            函数名称"GetRandomInt"
        """
        return "GetRandomInt"

    def execute(self, state_context, low: int, high: int) -> int:
        """执行GetRandomInt native函数。

        参数：
            state_context: 状态上下文
            low: 最小值
            high: 最大值

        返回：
            int: [low, high]范围内的随机整数，如果high<low则返回low
        """
        if high < low:
            return low
        return random.randint(low, high)


class GetRandomReal(NativeFunction):
    """获取随机实数。

    此函数模拟JASS中的GetRandomReal native函数，在[low, high]范围内返回随机实数。
    如果high < low，返回low。
    """

    @property
    def name(self) -> str:
        """获取函数名称。

        返回：
            函数名称"GetRandomReal"
        """
        return "GetRandomReal"

    def execute(self, state_context, low: float, high: float) -> float:
        """执行GetRandomReal native函数。

        参数：
            state_context: 状态上下文
            low: 最小值
            high: 最大值

        返回：
            float: [low, high]范围内的随机实数，如果high<low则返回low
        """
        if high < low:
            return low
        return random.uniform(low, high)
