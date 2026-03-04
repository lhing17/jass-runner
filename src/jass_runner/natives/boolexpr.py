"""JASS布尔表达式类。

此模块包含JASS布尔表达式handle的实现。
"""

from .handle_base import Handle


class BoolExpr(Handle):
    """布尔表达式基类，用于条件判断和过滤。

    属性：
        _func: 包装的函数（可为None）
    """

    def __init__(self, handle_id: str):
        """初始化布尔表达式。

        参数：
            handle_id: 唯一标识符
        """
        super().__init__(handle_id, "boolexpr")
        self._func = None

    def evaluate(self, *args, **kwargs) -> bool:
        """评估表达式，返回布尔值。

        参数：
            *args, **kwargs: 传递给包装函数的参数

        返回：
            评估结果，无函数时返回False
        """
        if self._func:
            return bool(self._func(*args, **kwargs))
        return False


class ConditionFunc(BoolExpr):
    """条件函数，用于触发器条件判断。

    继承自 BoolExpr，专门用于 TriggerAddCondition。
    包装的函数不接受参数，返回布尔值。
    """

    def __init__(self, handle_id: str, func=None):
        """初始化条件函数。

        参数：
            handle_id: 唯一标识符
            func: 条件函数（无参数，返回bool）
        """
        super().__init__(handle_id)
        self.type_name = "conditionfunc"
        self._func = func

    def evaluate(self) -> bool:
        """评估条件。

        返回：
            条件函数的执行结果，无函数时返回False
        """
        if self._func:
            return bool(self._func())
        return False


class FilterFunc(BoolExpr):
    """过滤函数，用于单位组枚举过滤。

    继承自 BoolExpr，专门用于 GroupEnumUnits 等函数。
    包装的函数接受一个单位参数，返回布尔值。
    """

    def __init__(self, handle_id: str, func=None):
        """初始化过滤函数。

        参数：
            handle_id: 唯一标识符
            func: 过滤函数（接受unit参数，返回bool）
        """
        super().__init__(handle_id)
        self.type_name = "filterfunc"
        self._func = func

    def evaluate(self, unit) -> bool:
        """评估单位是否符合过滤条件。

        参数：
            unit: 要评估的单位对象

        返回：
            过滤函数的执行结果，无函数时返回False
        """
        if self._func:
            return bool(self._func(unit))
        return False


class AndExpr(BoolExpr):
    """逻辑与表达式。

    组合两个布尔表达式，当两者都为True时返回True。
    """

    def __init__(self, handle_id: str, operand_a: BoolExpr, operand_b: BoolExpr):
        """初始化逻辑与表达式。

        参数：
            handle_id: 唯一标识符
            operand_a: 第一个操作数
            operand_b: 第二个操作数
        """
        super().__init__(handle_id)
        self._operand_a = operand_a
        self._operand_b = operand_b

    def evaluate(self, *args, **kwargs) -> bool:
        """评估逻辑与表达式。

        参数：
            *args, **kwargs: 传递给操作数的参数

        返回：
            两个操作数都为True时返回True
        """
        return self._operand_a.evaluate(*args, **kwargs) and self._operand_b.evaluate(*args, **kwargs)


class OrExpr(BoolExpr):
    """逻辑或表达式。

    组合两个布尔表达式，当任一者为True时返回True。
    """

    def __init__(self, handle_id: str, operand_a: BoolExpr, operand_b: BoolExpr):
        """初始化逻辑或表达式。

        参数：
            handle_id: 唯一标识符
            operand_a: 第一个操作数
            operand_b: 第二个操作数
        """
        super().__init__(handle_id)
        self._operand_a = operand_a
        self._operand_b = operand_b

    def evaluate(self, *args, **kwargs) -> bool:
        """评估逻辑或表达式。

        参数：
            *args, **kwargs: 传递给操作数的参数

        返回：
            任一操作数为True时返回True
        """
        return self._operand_a.evaluate(*args, **kwargs) or self._operand_b.evaluate(*args, **kwargs)


class NotExpr(BoolExpr):
    """逻辑非表达式。

    对一个布尔表达式取反。
    """

    def __init__(self, handle_id: str, operand: BoolExpr):
        """初始化逻辑非表达式。

        参数：
            handle_id: 唯一标识符
            operand: 操作数
        """
        super().__init__(handle_id)
        self._operand = operand

    def evaluate(self, *args, **kwargs) -> bool:
        """评估逻辑非表达式。

        参数：
            *args, **kwargs: 传递给操作数的参数

        返回：
            操作数为False时返回True
        """
        return not self._operand.evaluate(*args, **kwargs)
