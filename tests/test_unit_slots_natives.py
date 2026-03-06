"""技能格子槽位 native 函数单元测试。"""

import pytest
from unittest.mock import MagicMock

from jass_runner.natives.unit_slots_natives import (
    SetAllItemTypeSlots,
    SetAllUnitTypeSlots,
    SetItemTypeSlots,
    SetUnitTypeSlots,
)
from jass_runner.natives.unit import MAX_ITEM_TYPE_SLOTS, MAX_UNIT_TYPE_SLOTS


class TestSetAllItemTypeSlots:
    """测试 SetAllItemTypeSlots native 函数。"""

    def test_set_valid_slots(self):
        """测试设置有效的槽位数。"""
        native = SetAllItemTypeSlots()
        mock_context = MagicMock()

        result = native.execute(mock_context, 8)

        assert result == 8

    def test_clamp_to_max(self):
        """测试超过最大值时截断。"""
        native = SetAllItemTypeSlots()
        mock_context = MagicMock()

        result = native.execute(mock_context, 15)

        assert result == 11  # 截断到最大值

    def test_clamp_to_min(self):
        """测试负数时截断到0。"""
        native = SetAllItemTypeSlots()
        mock_context = MagicMock()

        result = native.execute(mock_context, -5)

        assert result == 0


class TestSetAllUnitTypeSlots:
    """测试 SetAllUnitTypeSlots native 函数。"""

    def test_set_valid_slots(self):
        """测试设置有效的槽位数。"""
        native = SetAllUnitTypeSlots()
        mock_context = MagicMock()

        result = native.execute(mock_context, 6)

        assert result == 6

    def test_clamp_to_max(self):
        """测试超过最大值时截断。"""
        native = SetAllUnitTypeSlots()
        mock_context = MagicMock()

        result = native.execute(mock_context, 20)

        assert result == 11  # 截断到最大值


class TestSetItemTypeSlots:
    """测试 SetItemTypeSlots native 函数。"""

    def test_set_valid_slots(self):
        """测试为单位设置有效的槽位数。"""
        native = SetItemTypeSlots()
        mock_context = MagicMock()
        mock_unit = MagicMock()
        mock_unit.id = "unit_001"
        mock_unit.set_item_type_slots.return_value = 5

        result = native.execute(mock_context, mock_unit, 5)

        assert result == 5
        mock_unit.set_item_type_slots.assert_called_once_with(5)

    def test_returns_zero_for_none_unit(self):
        """测试单位对象为None时返回0。"""
        native = SetItemTypeSlots()
        mock_context = MagicMock()

        result = native.execute(mock_context, None, 5)

        assert result == 0


class TestSetUnitTypeSlots:
    """测试 SetUnitTypeSlots native 函数。"""

    def test_set_valid_slots(self):
        """测试为单位设置有效的槽位数。"""
        native = SetUnitTypeSlots()
        mock_context = MagicMock()
        mock_unit = MagicMock()
        mock_unit.id = "unit_002"
        mock_unit.set_unit_type_slots.return_value = 7

        result = native.execute(mock_context, mock_unit, 7)

        assert result == 7
        mock_unit.set_unit_type_slots.assert_called_once_with(7)

    def test_returns_zero_for_none_unit(self):
        """测试单位对象为None时返回0。"""
        native = SetUnitTypeSlots()
        mock_context = MagicMock()

        result = native.execute(mock_context, None, 7)

        assert result == 0
