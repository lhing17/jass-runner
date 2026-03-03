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


class UnitAddItemById(NativeFunction):
    """创建物品并添加到单位背包。"""

    @property
    def name(self) -> str:
        return "UnitAddItemById"

    def execute(self, state_context: StateContext, unit: Unit, item_type_id: int, slot: int = -1) -> Optional[Item]:
        """执行创建并添加物品操作。

        参数：
            state_context: 状态上下文
            unit: 目标单位
            item_type_id: 物品类型ID（FourCC整数）
            slot: 目标槽位（-1表示自动找空槽，0-5表示指定槽位）

        返回：
            创建并添加成功返回Item对象，失败返回None
        """
        item_type_str = int_to_fourcc(item_type_id)
        handle_manager = state_context.handle_manager

        # 创建物品（使用单位位置）
        item = handle_manager.create_item(item_type_str, unit.x, unit.y)

        # 添加到单位
        if unit.add_item(item, slot):
            slot_str = f"槽位 {slot}" if slot >= 0 else "自动槽位"
            logger.info(f"[UnitAddItemById] 创建 {item_type_str} 并添加到单位 {unit.id} 的{slot_str}")
            return item
        else:
            # 添加失败，销毁物品
            handle_manager.destroy_handle(item.id)
            slot_str = f"槽位 {slot}" if slot >= 0 else "背包"
            logger.warning(f"[UnitAddItemById] {slot_str}已满或无效，销毁已创建的 {item_type_str}")
            return None


class UnitRemoveItem(NativeFunction):
    """从单位移除并销毁物品。"""

    @property
    def name(self) -> str:
        return "UnitRemoveItem"

    def execute(self, state_context: StateContext, unit: Unit, item: Item) -> bool:
        """执行移除并销毁操作。

        参数：
            state_context: 状态上下文
            unit: 目标单位
            item: 要移除的物品

        返回：
            移除成功返回True，物品不在背包中返回False
        """
        result = unit.remove_item(item)
        if result:
            handle_manager = state_context.handle_manager
            handle_manager.destroy_handle(item.id)
            logger.info(f"[UnitRemoveItem] 销毁物品 {item.id}")
            return True
        logger.warning(f"[UnitRemoveItem] 物品 {item.id} 不在单位 {unit.id} 背包中")
        return False


class UnitRemoveItemFromSlot(NativeFunction):
    """从指定槽位移除并销毁物品。"""

    @property
    def name(self) -> str:
        return "UnitRemoveItemFromSlot"

    def execute(self, state_context: StateContext, unit: Unit, slot: int) -> bool:
        """执行从槽位移除并销毁操作。

        参数：
            state_context: 状态上下文
            unit: 目标单位
            slot: 槽位索引（0-5）

        返回：
            移除成功返回True，槽位为空或越界返回False
        """
        item = unit.get_item_in_slot(slot)
        if item:
            unit.remove_item_from_slot(slot)
            handle_manager = state_context.handle_manager
            handle_manager.destroy_handle(item.id)
            logger.info(f"[UnitRemoveItemFromSlot] 槽位 {slot} 的物品已销毁")
            return True
        logger.warning(f"[UnitRemoveItemFromSlot] 槽位 {slot} 为空或无效")
        return False


class GetItemTypeId(NativeFunction):
    """获取物品类型ID（FourCC整数）。"""

    @property
    def name(self) -> str:
        return "GetItemTypeId"

    def execute(self, state_context: StateContext, item: Item) -> int:
        """返回物品类型ID。

        参数：
            state_context: 状态上下文
            item: 物品对象

        返回：
            物品类型ID（FourCC整数）
        """
        return string_to_fourcc(item.item_type)


class UnitItemInSlot(NativeFunction):
    """获取单位指定槽位的物品。"""

    @property
    def name(self) -> str:
        return "UnitItemInSlot"

    def execute(self, state_context: StateContext, unit: Unit, slot: int) -> Optional[Item]:
        """返回指定槽位的物品，空槽返回None。

        参数：
            state_context: 状态上下文
            unit: 目标单位
            slot: 槽位索引（0-5）

        返回：
            该槽位的物品，无效槽位或空槽返回None
        """
        return unit.get_item_in_slot(slot)
