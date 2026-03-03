"""物品背包 Native 函数单元测试。"""

import pytest
from jass_runner.natives.handle import Unit, Item, Player
from jass_runner.natives.manager import HandleManager
from jass_runner.natives.item_inventory_natives import UnitAddItem, UnitAddItemById
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


class TestUnitAddItemById:
    """测试 UnitAddItemById 函数。"""

    def test_add_item_by_id_auto_slot(self):
        """测试自动找空槽添加。"""
        state_context = StateContext()
        handle_manager = state_context.handle_manager
        player = handle_manager.get_player(0)
        unit = handle_manager.create_unit(0, player, 0.0, 0.0, 0.0)
        native = UnitAddItemById()

        # FourCC 'ratf' = 1718903154
        item_type_id = 1718903154
        result = native.execute(state_context, unit, item_type_id, -1)

        assert result is not None
        assert result.item_type == "ratf"
        assert unit.find_item(result) >= 0

    def test_add_item_by_id_specific_slot(self):
        """测试指定槽位添加。"""
        state_context = StateContext()
        handle_manager = state_context.handle_manager
        player = handle_manager.get_player(0)
        unit = handle_manager.create_unit(0, player, 0.0, 0.0, 0.0)
        native = UnitAddItemById()

        item_type_id = 1718903154  # 'ratf'
        result = native.execute(state_context, unit, item_type_id, 3)

        assert result is not None
        assert unit.get_item_in_slot(3) is result

    def test_add_item_by_id_occupied_slot_fails(self):
        """测试指定槽位被占时失败。"""
        state_context = StateContext()
        handle_manager = state_context.handle_manager
        player = handle_manager.get_player(0)
        unit = handle_manager.create_unit(0, player, 0.0, 0.0, 0.0)
        native = UnitAddItemById()

        # 先占用槽位3
        existing_item = handle_manager.create_item("existing", 1.0, 1.0)
        unit.add_item(existing_item, 3)

        # 尝试添加到槽位3
        item_type_id = 1380010356
        result = native.execute(state_context, unit, item_type_id, 3)

        assert result is None
        # 确认原有物品仍在
        assert unit.get_item_in_slot(3) is existing_item
