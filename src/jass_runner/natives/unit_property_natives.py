"""单位属性 native 函数实现。

此模块包含单位属性访问和修改的 native 函数。
"""

import logging
from .base import NativeFunction
from .handle import Unit

logger = logging.getLogger(__name__)

# 单位状态类型常量
UNIT_STATE_LIFE = 0
UNIT_STATE_MAX_LIFE = 1
UNIT_STATE_MANA = 2
UNIT_STATE_MAX_MANA = 3


class SetUnitState(NativeFunction):
    """设置单位状态（生命值/魔法值）。"""

    @property
    def name(self) -> str:
        return "SetUnitState"

    def execute(self, state_context, unit: Unit, state_type: int, value: float):
        """执行 SetUnitState native 函数。

        参数：
            state_context: 状态上下文
            unit: 单位对象
            state_type: 状态类型（0=生命, 1=最大生命, 2=魔法, 3=最大魔法）
            value: 新的状态值
        """
        if unit is None:
            logger.warning("[SetUnitState] 尝试设置 None 单位的状态")
            return

        # 状态类型映射
        state_map = {
            UNIT_STATE_LIFE: "UNIT_STATE_LIFE",
            UNIT_STATE_MAX_LIFE: "UNIT_STATE_MAX_LIFE",
            UNIT_STATE_MANA: "UNIT_STATE_MANA",
            UNIT_STATE_MAX_MANA: "UNIT_STATE_MAX_MANA",
        }

        state_str = state_map.get(state_type)
        if state_str is None:
            logger.warning(f"[SetUnitState] 未知状态类型: {state_type}")
            return

        # 通过 HandleManager 设置状态
        handle_manager = state_context.handle_manager
        handle_manager.set_unit_state(unit.id, state_str, value)

        logger.debug(f"[SetUnitState] 单位 {unit.id} 的 {state_str} 设置为 {value}")
