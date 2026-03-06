"""技能格子槽位 native 函数集成测试。"""

import pytest
from src.jass_runner.natives.unit import Unit, MAX_ITEM_TYPE_SLOTS, MAX_UNIT_TYPE_SLOTS
from src.jass_runner.natives.unit_slots_natives import (
    SetAllItemTypeSlots,
    SetAllUnitTypeSlots,
    SetItemTypeSlots,
    SetUnitTypeSlots,
)


class TestUnitSlotsIntegration:
    """测试技能格子槽位相关 native 函数的集成。"""

    def test_default_slots(self):
        """测试单位默认槽位数为11。"""
        unit = Unit("test_unit", "hfoo", 0, 0, 0, 0)

        assert unit._item_type_slots == 11
        assert unit._unit_type_slots == 11

    def test_set_item_type_slots_within_limit(self):
        """测试在限制范围内设置物品类型槽位。"""
        state_context = None
        unit = Unit("test_unit", "hfoo", 0, 0, 0, 0)

        result = SetItemTypeSlots().execute(state_context, unit, 5)

        assert result == 5
        assert unit._item_type_slots == 5

    def test_set_item_type_slots_clamped(self):
        """测试设置物品类型槽位时截断到全局最大值。"""
        state_context = None
        unit = Unit("test_unit", "hfoo", 0, 0, 0, 0)

        # 先设置全局最大值为8
        SetAllItemTypeSlots().execute(state_context, 8)

        # 尝试设置10，应该被截断到8
        result = SetItemTypeSlots().execute(state_context, unit, 10)

        assert result == 8
        assert unit._item_type_slots == 8

    def test_set_unit_type_slots_within_limit(self):
        """测试在限制范围内设置单位类型槽位。"""
        state_context = None
        unit = Unit("test_unit", "hfoo", 0, 0, 0, 0)

        result = SetUnitTypeSlots().execute(state_context, unit, 6)

        assert result == 6
        assert unit._unit_type_slots == 6

    def test_set_all_item_type_slots_affects_new_units(self):
        """测试设置全局物品类型槽位影响后续单位设置。"""
        state_context = None

        # 设置全局最大值为5
        SetAllItemTypeSlots().execute(state_context, 5)

        # 创建新单位并尝试设置10
        unit = Unit("test_unit", "hfoo", 0, 0, 0, 0)
        result = SetItemTypeSlots().execute(state_context, unit, 10)

        # 应该被截断到5
        assert result == 5
        assert unit._item_type_slots == 5

    def test_clamp_negative_slots(self):
        """测试负数槽位数被截断到0。"""
        state_context = None
        unit = Unit("test_unit", "hfoo", 0, 0, 0, 0)

        result = SetItemTypeSlots().execute(state_context, unit, -3)

        assert result == 0
        assert unit._item_type_slots == 0

    def test_set_all_clamp_to_max(self):
        """测试设置全局槽位时截断到11。"""
        state_context = None

        result = SetAllItemTypeSlots().execute(state_context, 20)

        assert result == 11
