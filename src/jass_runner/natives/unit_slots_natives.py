"""单位技能格子槽位相关 native 函数实现。

此模块包含与单位技能格子槽位设置相关的 JASS native 函数。
"""

import logging
from typing import TYPE_CHECKING

from .base import NativeFunction
from .unit import MAX_ITEM_TYPE_SLOTS, MAX_UNIT_TYPE_SLOTS

if TYPE_CHECKING:
    from .state import StateContext
    from .handle import Unit

logger = logging.getLogger(__name__)


class SetAllItemTypeSlots(NativeFunction):
    """设置全局物品类型最大槽位数。"""

    @property
    def name(self) -> str:
        return "SetAllItemTypeSlots"

    def execute(self, state_context: 'StateContext', slots: int) -> int:
        """执行 SetAllItemTypeSlots native 函数。

        参数：
            state_context: 状态上下文
            slots: 期望的最大槽位数

        返回：
            实际设置的最大槽位数（会被截断到 0-11 范围）
        """
        global MAX_ITEM_TYPE_SLOTS
        actual_slots = max(0, min(slots, 11))
        MAX_ITEM_TYPE_SLOTS = actual_slots
        logger.info(f"[SetAllItemTypeSlots] 设置全局物品类型最大槽位数为: {actual_slots}")
        return actual_slots


class SetAllUnitTypeSlots(NativeFunction):
    """设置全局单位类型最大槽位数。"""

    @property
    def name(self) -> str:
        return "SetAllUnitTypeSlots"

    def execute(self, state_context: 'StateContext', slots: int) -> int:
        """执行 SetAllUnitTypeSlots native 函数。

        参数：
            state_context: 状态上下文
            slots: 期望的最大槽位数

        返回：
            实际设置的最大槽位数（会被截断到 0-11 范围）
        """
        global MAX_UNIT_TYPE_SLOTS
        actual_slots = max(0, min(slots, 11))
        MAX_UNIT_TYPE_SLOTS = actual_slots
        logger.info(f"[SetAllUnitTypeSlots] 设置全局单位类型最大槽位数为: {actual_slots}")
        return actual_slots


class SetItemTypeSlots(NativeFunction):
    """为单位设置技能格子中出售物品的槽位数。"""

    @property
    def name(self) -> str:
        return "SetItemTypeSlots"

    def execute(self, state_context: 'StateContext', unit: 'Unit', slots: int) -> int:
        """执行 SetItemTypeSlots native 函数。

        参数：
            state_context: 状态上下文
            unit: 单位对象
            slots: 期望的槽位数

        返回：
            实际设置的槽位数（会被截断到 0-MAX_ITEM_TYPE_SLOTS 范围）
        """
        if unit is None:
            logger.warning("[SetItemTypeSlots] 单位对象为 None")
            return 0

        actual_slots = unit.set_item_type_slots(slots)
        logger.info(f"[SetItemTypeSlots] 单位{unit.id} 设置物品类型槽位数为: {actual_slots}")
        return actual_slots


class SetUnitTypeSlots(NativeFunction):
    """为单位设置技能格子中出售单位的槽位数。"""

    @property
    def name(self) -> str:
        return "SetUnitTypeSlots"

    def execute(self, state_context: 'StateContext', unit: 'Unit', slots: int) -> int:
        """执行 SetUnitTypeSlots native 函数。

        参数：
            state_context: 状态上下文
            unit: 单位对象
            slots: 期望的槽位数

        返回：
            实际设置的槽位数（会被截断到 0-MAX_UNIT_TYPE_SLOTS 范围）
        """
        if unit is None:
            logger.warning("[SetUnitTypeSlots] 单位对象为 None")
            return 0

        actual_slots = unit.set_unit_type_slots(slots)
        logger.info(f"[SetUnitTypeSlots] 单位{unit.id} 设置单位类型槽位数为: {actual_slots}")
        return actual_slots
