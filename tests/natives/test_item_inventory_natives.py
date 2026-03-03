"""物品背包 Native 函数单元测试。"""

import pytest
from jass_runner.natives.handle import Unit, Item, Player
from jass_runner.natives.manager import HandleManager
from jass_runner.natives.item_inventory_natives import UnitAddItem
from jass_runner.natives.state import StateContext


class TestUnitAddItem:
    """测试 UnitAddItem 函数。"""

    def test_add_item_to_empty_slot_success(self):
        """测试成功添加物品到空槽位。"""
        # 准备
        state_context = StateContext()
        handle_manager = state_context.handle_manager
        player = handle_manager.get_player(0)
        unit = handle_manager.create_unit(0, player, 0.0, 0.0, 0.0)
        item = handle_manager.create_item("ratf", 1.0, 1.0)
        native = UnitAddItem()

        # 执行
        result = native.execute(state_context, unit, item)

        # 验证
        assert result is True
        assert unit.find_item(item) >= 0

    def test_add_item_when_inventory_full_fails(self):
        """测试背包满时添加失败。"""
        state_context = StateContext()
        handle_manager = state_context.handle_manager
        player = handle_manager.get_player(0)
        unit = handle_manager.create_unit(0, player, 0.0, 0.0, 0.0)
        native = UnitAddItem()

        # 填满6个槽位
        for i in range(6):
            item = handle_manager.create_item(f"item{i}", float(i), float(i))
            unit.add_item(item)

        # 尝试添加第7个
        extra_item = handle_manager.create_item("extra", 10.0, 10.0)
        result = native.execute(state_context, unit, extra_item)

        assert result is False

    def test_add_same_item_twice_fails(self):
        """测试同一物品添加两次失败。"""
        state_context = StateContext()
        handle_manager = state_context.handle_manager
        player = handle_manager.get_player(0)
        unit = handle_manager.create_unit(0, player, 0.0, 0.0, 0.0)
        item = handle_manager.create_item("ratf", 1.0, 1.0)
        native = UnitAddItem()

        # 第一次添加
        result1 = native.execute(state_context, unit, item)
        assert result1 is True

        # 第二次添加（同一物品）
        result2 = native.execute(state_context, unit, item)
        assert result2 is False
