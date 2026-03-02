"""Blz单位组Native函数测试。"""

import pytest
from jass_runner.natives.state import StateContext
from jass_runner.natives.group_natives import (
    CreateGroup, GroupAddUnit, BlzGroupGetSize, BlzGroupUnitAt
)


class TestBlzGroupGetSize:
    """测试BlzGroupGetSize native函数。"""

    def test_get_size_of_empty_group(self):
        """测试获取空组大小。"""
        state = StateContext()
        create_group = CreateGroup()
        get_size = BlzGroupGetSize()

        group = create_group.execute(state)
        result = get_size.execute(state, group)

        assert result == 0

    def test_get_size_of_group_with_units(self):
        """测试获取有单位的组大小。"""
        state = StateContext()
        create_group = CreateGroup()
        add_unit = GroupAddUnit()
        get_size = BlzGroupGetSize()

        group = create_group.execute(state)
        unit1 = state.handle_manager.create_unit("hfoo", 0, 100.0, 200.0, 0.0)
        unit2 = state.handle_manager.create_unit("hfoo", 0, 150.0, 250.0, 0.0)
        add_unit.execute(state, group, unit1)
        add_unit.execute(state, group, unit2)

        result = get_size.execute(state, group)

        assert result == 2

    def test_get_size_of_none_group(self):
        """测试获取None组大小返回0。"""
        state = StateContext()
        get_size = BlzGroupGetSize()

        result = get_size.execute(state, None)

        assert result == 0


class TestBlzGroupUnitAt:
    """测试BlzGroupUnitAt native函数。"""

    def test_get_unit_at_valid_index(self):
        """测试获取有效索引的单位。"""
        state = StateContext()
        create_group = CreateGroup()
        add_unit = GroupAddUnit()
        get_unit = BlzGroupUnitAt()

        group = create_group.execute(state)
        unit = state.handle_manager.create_unit("hfoo", 0, 100.0, 200.0, 0.0)
        add_unit.execute(state, group, unit)

        result = get_unit.execute(state, group, 0)

        assert result == unit

    def test_get_unit_at_invalid_index(self):
        """测试获取无效索引返回None。"""
        state = StateContext()
        create_group = CreateGroup()
        get_unit = BlzGroupUnitAt()

        group = create_group.execute(state)

        result = get_unit.execute(state, group, 0)

        assert result is None

    def test_get_unit_at_none_group(self):
        """测试获取None组的单位返回None。"""
        state = StateContext()
        get_unit = BlzGroupUnitAt()

        result = get_unit.execute(state, None, 0)

        assert result is None
