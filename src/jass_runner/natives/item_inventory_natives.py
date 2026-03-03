"""物品背包系统 Native 函数实现。

此模块包含单位物品背包相关的 Native 函数。
"""

import logging
from typing import Optional

from jass_runner.natives.base import NativeFunction
from jass_runner.natives.handle import Unit, Item
from jass_runner.natives.state import StateContext
from jass_runner.utils import int_to_fourcc, fourcc_to_int as string_to_fourcc

logger = logging.getLogger(__name__)


class UnitAddItem(NativeFunction):
    """将物品添加到单位背包。"""

    @property
    def name(self) -> str:
        return "UnitAddItem"

    def execute(self, state_context: StateContext, unit: Unit, item: Item) -> bool:
        """执行添加物品操作。

        参数：
            state_context: 状态上下文
            unit: 目标单位
            item: 要添加的物品

        返回：
            添加成功返回True，失败返回False
        """
        if unit.find_item(item) >= 0:
            logger.warning(f"[UnitAddItem] 物品 {item.id} 已在单位背包中")
            return False
        result = unit.add_item(item)
        if result:
            logger.info(f"[UnitAddItem] 物品 {item.id} 添加到单位 {unit.id}")
        else:
            logger.warning(f"[UnitAddItem] 单位 {unit.id} 背包已满，无法添加物品")
        return result
