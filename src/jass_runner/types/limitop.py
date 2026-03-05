"""LimitOp比较操作符类型定义。

此模块定义JASS中使用的比较操作符常量和相关工具方法。
"""


class LimitOp:
    """JASS比较操作符常量定义。

    定义了6个比较操作符常量，用于条件判断和比较操作。
    常量值与JASS规范保持一致。
    """

    # 比较操作符常量
    LESS_THAN = 0
    LESS_THAN_OR_EQUAL = 1
    EQUAL = 2
    GREATER_THAN_OR_EQUAL = 3
    GREATER_THAN = 4
    NOT_EQUAL = 5

    # 浮点数比较的默认epsilon值
    _EPSILON = 0.001

    @staticmethod
    def compare(op: int, a: float, b: float) -> bool:
        """执行比较操作。

        根据指定的操作符比较两个数值。对于相等性比较，
        使用epsilon值处理浮点数精度问题。

        参数：
            op: 比较操作符（使用LimitOp常量）
            a: 第一个操作数
            b: 第二个操作数

        返回：
            比较结果，满足条件返回True，否则返回False

        示例：
            >>> LimitOp.compare(LimitOp.LESS_THAN, 1.0, 2.0)
            True
            >>> LimitOp.compare(LimitOp.EQUAL, 1.0, 1.0005)
            True
        """
        if op == LimitOp.LESS_THAN:
            return a < b
        elif op == LimitOp.LESS_THAN_OR_EQUAL:
            return a <= b
        elif op == LimitOp.EQUAL:
            return abs(a - b) < LimitOp._EPSILON
        elif op == LimitOp.GREATER_THAN_OR_EQUAL:
            return a >= b
        elif op == LimitOp.GREATER_THAN:
            return a > b
        elif op == LimitOp.NOT_EQUAL:
            return abs(a - b) >= LimitOp._EPSILON
        else:
            return False
