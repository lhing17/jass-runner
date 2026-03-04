"""布尔表达式相关的原生函数。

此模块包含 Condition、Filter、And、Or、Not 等 native 函数的实现，
用于创建和管理布尔表达式、条件函数和过滤函数。
"""

import logging
from typing import Callable, Optional
from ..natives.base import NativeFunction


logger = logging.getLogger(__name__)


class Condition(NativeFunction):
    """将 code 函数包装为 conditionfunc。

    创建一个 conditionfunc 对象，包装传入的函数。
    被包装的函数不接受参数，应返回布尔值。
    """

    @property
    def name(self) -> str:
        """获取 native 函数的名称。

        返回：
            "Condition"
        """
        return "Condition"

    def execute(self, state_context, func: Callable, *args, **kwargs):
        """执行 Condition native 函数。

        参数：
            state_context: 状态上下文，必须包含 handle_manager
            func: 要包装的条件函数（无参数，返回bool）
            *args: 额外位置参数
            **kwargs: 关键字参数

        返回：
            conditionfunc 的 handle ID，失败返回 None
        """
        # 检查 state_context 和 handle_manager
        if state_context is None:
            logger.error("[Condition] state_context is None")
            return None

        if not hasattr(state_context, 'handle_manager') or state_context.handle_manager is None:
            logger.error("[Condition] handle_manager not found in state_context")
            return None

        # 检查 func 是否可调用
        if not callable(func):
            logger.error("[Condition] func is not callable")
            return None

        # 生成唯一ID
        handle_id = f"condition_{state_context.handle_manager._generate_id()}"

        # 导入 ConditionFunc 类
        from .handle import ConditionFunc

        # 创建 ConditionFunc 对象
        condition = ConditionFunc(handle_id, func)

        # 注册到 handle_manager
        state_context.handle_manager._register_handle(condition)

        logger.info(f"[Condition] Created conditionfunc: {handle_id}")
        return handle_id


class Filter(NativeFunction):
    """将 code 函数包装为 filterfunc。

    创建一个 filterfunc 对象，包装传入的函数。
    被包装的函数接受一个单位参数，应返回布尔值。
    """

    @property
    def name(self) -> str:
        """获取 native 函数的名称。

        返回：
            "Filter"
        """
        return "Filter"

    def execute(self, state_context, func: Callable, *args, **kwargs):
        """执行 Filter native 函数。

        参数：
            state_context: 状态上下文，必须包含 handle_manager
            func: 要包装的过滤函数（接受unit参数，返回bool）
            *args: 额外位置参数
            **kwargs: 关键字参数

        返回：
            filterfunc 的 handle ID，失败返回 None
        """
        # 检查 state_context 和 handle_manager
        if state_context is None:
            logger.error("[Filter] state_context is None")
            return None

        if not hasattr(state_context, 'handle_manager') or state_context.handle_manager is None:
            logger.error("[Filter] handle_manager not found in state_context")
            return None

        # 检查 func 是否可调用
        if not callable(func):
            logger.error("[Filter] func is not callable")
            return None

        # 生成唯一ID
        handle_id = f"filter_{state_context.handle_manager._generate_id()}"

        # 导入 FilterFunc 类
        from .handle import FilterFunc

        # 创建 FilterFunc 对象
        filter_func = FilterFunc(handle_id, func)

        # 注册到 handle_manager
        state_context.handle_manager._register_handle(filter_func)

        logger.info(f"[Filter] Created filterfunc: {handle_id}")
        return handle_id


class DestroyCondition(NativeFunction):
    """销毁 conditionfunc。"""

    @property
    def name(self) -> str:
        """获取 native 函数的名称。

        返回：
            "DestroyCondition"
        """
        return "DestroyCondition"

    def execute(self, state_context, condition_id: str, *args, **kwargs):
        """执行 DestroyCondition native 函数。

        参数：
            state_context: 状态上下文，必须包含 handle_manager
            condition_id: 要销毁的 conditionfunc ID
            *args: 额外位置参数
            **kwargs: 关键字参数

        返回：
            None（对应 JASS 的 nothing）
        """
        # 检查 state_context 和 handle_manager
        if state_context is None or not hasattr(state_context, 'handle_manager'):
            logger.error("[DestroyCondition] state_context or handle_manager not found")
            return None

        # 销毁 handle
        success = state_context.handle_manager.destroy_handle(condition_id)
        if success:
            logger.info(f"[DestroyCondition] Destroyed conditionfunc: {condition_id}")
        else:
            logger.warning(f"[DestroyCondition] conditionfunc not found: {condition_id}")

        return None


class DestroyFilter(NativeFunction):
    """销毁 filterfunc。"""

    @property
    def name(self) -> str:
        """获取 native 函数的名称。

        返回：
            "DestroyFilter"
        """
        return "DestroyFilter"

    def execute(self, state_context, filter_id: str, *args, **kwargs):
        """执行 DestroyFilter native 函数。

        参数：
            state_context: 状态上下文，必须包含 handle_manager
            filter_id: 要销毁的 filterfunc ID
            *args: 额外位置参数
            **kwargs: 关键字参数

        返回：
            None（对应 JASS 的 nothing）
        """
        # 检查 state_context 和 handle_manager
        if state_context is None or not hasattr(state_context, 'handle_manager'):
            logger.error("[DestroyFilter] state_context or handle_manager not found")
            return None

        # 销毁 handle
        success = state_context.handle_manager.destroy_handle(filter_id)
        if success:
            logger.info(f"[DestroyFilter] Destroyed filterfunc: {filter_id}")
        else:
            logger.warning(f"[DestroyFilter] filterfunc not found: {filter_id}")

        return None


class And(NativeFunction):
    """创建逻辑与表达式。"""

    @property
    def name(self) -> str:
        """获取 native 函数的名称。

        返回：
            "And"
        """
        return "And"

    def execute(self, state_context, operand_a: str, operand_b: str, *args, **kwargs):
        """执行 And native 函数。

        参数：
            state_context: 状态上下文，必须包含 handle_manager
            operand_a: 第一个 boolexpr 的 handle ID
            operand_b: 第二个 boolexpr 的 handle ID
            *args: 额外位置参数
            **kwargs: 关键字参数

        返回：
            新的 boolexpr handle ID，失败返回 None
        """
        # 检查 state_context 和 handle_manager
        if state_context is None:
            logger.error("[And] state_context is None")
            return None

        if not hasattr(state_context, 'handle_manager') or state_context.handle_manager is None:
            logger.error("[And] handle_manager not found in state_context")
            return None

        # 获取两个操作数
        expr_a = state_context.handle_manager.get_boolexpr(operand_a)
        expr_b = state_context.handle_manager.get_boolexpr(operand_b)

        if expr_a is None:
            logger.error(f"[And] operand_a not found: {operand_a}")
            return None

        if expr_b is None:
            logger.error(f"[And] operand_b not found: {operand_b}")
            return None

        # 生成唯一ID
        handle_id = f"boolexpr_{state_context.handle_manager._generate_id()}"

        # 导入 AndExpr 类
        from .handle import AndExpr

        # 创建 AndExpr 对象
        and_expr = AndExpr(handle_id, expr_a, expr_b)

        # 注册到 handle_manager
        state_context.handle_manager._register_handle(and_expr)

        logger.info(f"[And] Created boolexpr: {handle_id}")
        return handle_id


class Or(NativeFunction):
    """创建逻辑或表达式。"""

    @property
    def name(self) -> str:
        """获取 native 函数的名称。

        返回：
            "Or"
        """
        return "Or"

    def execute(self, state_context, operand_a: str, operand_b: str, *args, **kwargs):
        """执行 Or native 函数。

        参数：
            state_context: 状态上下文，必须包含 handle_manager
            operand_a: 第一个 boolexpr 的 handle ID
            operand_b: 第二个 boolexpr 的 handle ID
            *args: 额外位置参数
            **kwargs: 关键字参数

        返回：
            新的 boolexpr handle ID，失败返回 None
        """
        # 检查 state_context 和 handle_manager
        if state_context is None:
            logger.error("[Or] state_context is None")
            return None

        if not hasattr(state_context, 'handle_manager') or state_context.handle_manager is None:
            logger.error("[Or] handle_manager not found in state_context")
            return None

        # 获取两个操作数
        expr_a = state_context.handle_manager.get_boolexpr(operand_a)
        expr_b = state_context.handle_manager.get_boolexpr(operand_b)

        if expr_a is None:
            logger.error(f"[Or] operand_a not found: {operand_a}")
            return None

        if expr_b is None:
            logger.error(f"[Or] operand_b not found: {operand_b}")
            return None

        # 生成唯一ID
        handle_id = f"boolexpr_{state_context.handle_manager._generate_id()}"

        # 导入 OrExpr 类
        from .handle import OrExpr

        # 创建 OrExpr 对象
        or_expr = OrExpr(handle_id, expr_a, expr_b)

        # 注册到 handle_manager
        state_context.handle_manager._register_handle(or_expr)

        logger.info(f"[Or] Created boolexpr: {handle_id}")
        return handle_id


class Not(NativeFunction):
    """创建逻辑非表达式。"""

    @property
    def name(self) -> str:
        """获取 native 函数的名称。

        返回：
            "Not"
        """
        return "Not"

    def execute(self, state_context, operand: str, *args, **kwargs):
        """执行 Not native 函数。

        参数：
            state_context: 状态上下文，必须包含 handle_manager
            operand: boolexpr 的 handle ID
            *args: 额外位置参数
            **kwargs: 关键字参数

        返回：
            新的 boolexpr handle ID，失败返回 None
        """
        # 检查 state_context 和 handle_manager
        if state_context is None:
            logger.error("[Not] state_context is None")
            return None

        if not hasattr(state_context, 'handle_manager') or state_context.handle_manager is None:
            logger.error("[Not] handle_manager not found in state_context")
            return None

        # 获取操作数
        expr = state_context.handle_manager.get_boolexpr(operand)

        if expr is None:
            logger.error(f"[Not] operand not found: {operand}")
            return None

        # 生成唯一ID
        handle_id = f"boolexpr_{state_context.handle_manager._generate_id()}"

        # 导入 NotExpr 类
        from .handle import NotExpr

        # 创建 NotExpr 对象
        not_expr = NotExpr(handle_id, expr)

        # 注册到 handle_manager
        state_context.handle_manager._register_handle(not_expr)

        logger.info(f"[Not] Created boolexpr: {handle_id}")
        return handle_id


class DestroyBoolExpr(NativeFunction):
    """销毁 boolexpr。"""

    @property
    def name(self) -> str:
        """获取 native 函数的名称。

        返回：
            "DestroyBoolExpr"
        """
        return "DestroyBoolExpr"

    def execute(self, state_context, boolexpr_id: str, *args, **kwargs):
        """执行 DestroyBoolExpr native 函数。

        参数：
            state_context: 状态上下文，必须包含 handle_manager
            boolexpr_id: 要销毁的 boolexpr ID
            *args: 额外位置参数
            **kwargs: 关键字参数

        返回：
            None（对应 JASS 的 nothing）
        """
        # 检查 state_context 和 handle_manager
        if state_context is None or not hasattr(state_context, 'handle_manager'):
            logger.error("[DestroyBoolExpr] state_context or handle_manager not found")
            return None

        # 销毁 handle
        success = state_context.handle_manager.destroy_handle(boolexpr_id)
        if success:
            logger.info(f"[DestroyBoolExpr] Destroyed boolexpr: {boolexpr_id}")
        else:
            logger.warning(f"[DestroyBoolExpr] boolexpr not found: {boolexpr_id}")

        return None
