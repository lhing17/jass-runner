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
