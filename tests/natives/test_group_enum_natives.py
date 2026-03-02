"""单位组枚举Native函数测试。

此模块包含单位组枚举相关native函数的测试用例。
"""

import pytest
from jass_runner.natives.state import StateContext
from jass_runner.natives.group_natives import (
    CreateGroup, GroupEnumUnitsOfPlayer, BlzGroupGetSize, GroupAddUnit,
    GroupEnumUnitsInRange, GroupEnumUnitsInRangeOfLoc
)
from jass_runner.natives.location import LocationConstructor


class TestGroupEnumUnitsOfPlayer:
    """测试GroupEnumUnitsOfPlayer native函数。"""

    def test_enum_units_of_player(self):
        """测试按玩家枚举单位到组。"""
        state = StateContext()
        create_group = CreateGroup()
        enum_units = GroupEnumUnitsOfPlayer()
        get_size = BlzGroupGetSize()

        group = create_group.execute(state)
        # 创建玩家0的单位
        unit1 = state.handle_manager.create_unit("hfoo", 0, 100.0, 200.0, 0.0)
        unit2 = state.handle_manager.create_unit("hfoo", 0, 150.0, 250.0, 0.0)
        # 创建玩家1的单位
        unit3 = state.handle_manager.create_unit("hfoo", 1, 300.0, 400.0, 0.0)

        # 枚举玩家0的单位到组
        player = state.handle_manager.get_player(0)
        enum_units.execute(state, group, player, None)

        result = get_size.execute(state, group)
        assert result == 2

    def test_enum_units_of_player_clears_group(self):
        """测试枚举前清空组。"""
        state = StateContext()
        create_group = CreateGroup()
        add_unit = GroupAddUnit()
        enum_units = GroupEnumUnitsOfPlayer()
        get_size = BlzGroupGetSize()

        group = create_group.execute(state)
        # 先添加一个其他单位到组
        other_unit = state.handle_manager.create_unit("hfoo", 1, 500.0, 500.0, 0.0)
        add_unit.execute(state, group, other_unit)

        # 枚举玩家0的单位（应该清空之前的）
        player = state.handle_manager.get_player(0)
        unit1 = state.handle_manager.create_unit("hfoo", 0, 100.0, 200.0, 0.0)
        enum_units.execute(state, group, player, None)

        result = get_size.execute(state, group)
        assert result == 1

    def test_enum_units_of_player_with_filter(self):
        """测试按玩家枚举单位并应用过滤器。"""
        state = StateContext()
        create_group = CreateGroup()
        enum_units = GroupEnumUnitsOfPlayer()
        get_size = BlzGroupGetSize()

        group = create_group.execute(state)
        # 创建不同类型的单位
        unit1 = state.handle_manager.create_unit("hfoo", 0, 100.0, 200.0, 0.0)  # 步兵
        unit2 = state.handle_manager.create_unit("hkni", 0, 150.0, 250.0, 0.0)  # 骑士

        # 只枚举步兵类型的单位
        player = state.handle_manager.get_player(0)
        filter_func = lambda u: u.unit_type == "hfoo"
        enum_units.execute(state, group, player, filter_func)

        result = get_size.execute(state, group)
        assert result == 1

    def test_enum_units_of_none_player(self):
        """测试枚举None玩家不报错。"""
        state = StateContext()
        create_group = CreateGroup()
        enum_units = GroupEnumUnitsOfPlayer()

        group = create_group.execute(state)

        # 应该不报错，只是记录警告
        enum_units.execute(state, group, None, None)


class TestGroupEnumUnitsInRange:
    """测试GroupEnumUnitsInRange native函数。"""

    def test_enum_units_in_range(self):
        """测试在范围内枚举单位。"""
        state = StateContext()
        create_group = CreateGroup()
        enum_units = GroupEnumUnitsInRange()
        get_size = BlzGroupGetSize()

        group = create_group.execute(state)
        # 在范围内创建单位
        unit1 = state.handle_manager.create_unit("hfoo", 0, 100.0, 200.0, 0.0)  # 距离0
        unit2 = state.handle_manager.create_unit("hfoo", 0, 150.0, 200.0, 0.0)  # 距离50
        # 在范围外创建单位
        unit3 = state.handle_manager.create_unit("hfoo", 0, 300.0, 200.0, 0.0)  # 距离200

        # 枚举中心(100, 200)半径100范围内的单位
        enum_units.execute(state, group, 100.0, 200.0, 100.0, None)

        result = get_size.execute(state, group)
        assert result == 2

    def test_enum_units_in_range_with_filter(self):
        """测试在范围内枚举单位并应用过滤器。"""
        state = StateContext()
        create_group = CreateGroup()
        enum_units = GroupEnumUnitsInRange()
        get_size = BlzGroupGetSize()

        group = create_group.execute(state)
        # 在范围内创建不同类型单位
        unit1 = state.handle_manager.create_unit("hfoo", 0, 100.0, 200.0, 0.0)  # 步兵
        unit2 = state.handle_manager.create_unit("hkni", 0, 150.0, 200.0, 0.0)  # 骑士

        # 只枚举步兵
        filter_func = lambda u: u.unit_type == "hfoo"
        enum_units.execute(state, group, 100.0, 200.0, 100.0, filter_func)

        result = get_size.execute(state, group)
        assert result == 1

    def test_enum_units_in_range_negative_radius(self):
        """测试负半径不报错。"""
        state = StateContext()
        create_group = CreateGroup()
        enum_units = GroupEnumUnitsInRange()

        group = create_group.execute(state)

        # 应该不报错，只是记录警告
        enum_units.execute(state, group, 100.0, 200.0, -100.0, None)


class TestGroupEnumUnitsInRangeOfLoc:
    """测试GroupEnumUnitsInRangeOfLoc native函数。"""

    def test_enum_units_in_range_of_loc(self):
        """测试在Location范围内枚举单位。"""
        state = StateContext()
        create_group = CreateGroup()
        create_loc = LocationConstructor()
        enum_units = GroupEnumUnitsInRangeOfLoc()
        get_size = BlzGroupGetSize()

        group = create_group.execute(state)
        # 创建Location
        loc = create_loc.execute(state, 100.0, 200.0)
        # 在范围内创建单位
        unit1 = state.handle_manager.create_unit("hfoo", 0, 100.0, 200.0, 0.0)
        unit2 = state.handle_manager.create_unit("hfoo", 0, 150.0, 200.0, 0.0)

        # 枚举Location半径100范围内的单位
        enum_units.execute(state, group, loc, 100.0, None)

        result = get_size.execute(state, group)
        assert result == 2

    def test_enum_units_in_range_of_none_loc(self):
        """测试枚举None Location不报错。"""
        state = StateContext()
        create_group = CreateGroup()
        enum_units = GroupEnumUnitsInRangeOfLoc()

        group = create_group.execute(state)

        # 应该不报错，只是记录警告
        enum_units.execute(state, group, None, 100.0, None)
