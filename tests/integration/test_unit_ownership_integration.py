"""单位所有权Native函数集成测试。

此模块包含单位所有权和范围检测的集成测试用例。
"""

import pytest
from jass_runner.natives.state import StateContext
from jass_runner.natives.unit_ownership_natives import (
    IsUnitOwnedByPlayer,
    SetUnitOwner,
    IsUnitAlly,
    IsUnitEnemy,
)
from jass_runner.natives.unit_range_natives import (
    IsUnitInRange,
    IsUnitInRangeXY,
    IsUnitInRangeLoc,
)
from jass_runner.natives.location import Location


class TestUnitOwnershipWorkflow:
    """测试单位所有权完整工作流程。"""

    def test_complete_ownership_transfer(self):
        """测试完整的单位所有权转移流程。"""
        state = StateContext()
        set_owner = SetUnitOwner()
        is_owned = IsUnitOwnedByPlayer()

        # 创建玩家0的单位
        unit = state.handle_manager.create_unit("hfoo", 0, 100.0, 200.0, 0.0)
        # 获取玩家0和玩家1
        player0 = state.handle_manager.get_player(0)
        player1 = state.handle_manager.get_player(1)

        # 初始属于玩家0
        assert is_owned.execute(state, unit, player0) is True
        assert is_owned.execute(state, unit, player1) is False

        # 转移所有权
        set_owner.execute(state, unit, player1, False)

        # 现在属于玩家1
        assert is_owned.execute(state, unit, player0) is False
        assert is_owned.execute(state, unit, player1) is True

    def test_ally_and_enemy_detection(self):
        """测试盟友和敌人检测。"""
        state = StateContext()
        is_ally = IsUnitAlly()
        is_enemy = IsUnitEnemy()

        # 创建玩家0的单位
        unit = state.handle_manager.create_unit("hfoo", 0, 100.0, 200.0, 0.0)
        # 获取玩家1
        player1 = state.handle_manager.get_player(1)

        # 初始无关系
        assert is_ally.execute(state, unit, player1) is False
        assert is_enemy.execute(state, unit, player1) is False

        # 设置为盟友
        unit_owner = state.handle_manager.get_player(0)
        unit_owner.set_alliance(1, True)

        assert is_ally.execute(state, unit, player1) is True
        assert is_enemy.execute(state, unit, player1) is False

        # 改为敌人
        unit_owner.set_alliance(1, False)

        assert is_ally.execute(state, unit, player1) is False
        assert is_enemy.execute(state, unit, player1) is True


class TestUnitRangeDetectionWorkflow:
    """测试单位范围检测完整工作流程。"""

    def test_range_detection_between_units(self):
        """测试单位间范围检测。"""
        state = StateContext()
        is_in_range = IsUnitInRange()

        # 创建两个单位
        unit1 = state.handle_manager.create_unit("hfoo", 0, 0.0, 0.0, 0.0)
        unit2 = state.handle_manager.create_unit("hfoo", 1, 50.0, 0.0, 0.0)

        assert is_in_range.execute(unit1, unit2, 100.0) is True
        assert is_in_range.execute(unit1, unit2, 40.0) is False

    def test_range_detection_with_coordinates(self):
        """测试坐标范围检测。"""
        state = StateContext()
        is_in_range_xy = IsUnitInRangeXY()

        # 创建单位在距离(0,0)为50的位置
        unit = state.handle_manager.create_unit("hfoo", 0, 30.0, 40.0, 0.0)

        assert is_in_range_xy.execute(unit, 0.0, 0.0, 50.0) is True
        assert is_in_range_xy.execute(unit, 0.0, 0.0, 49.9) is False

    def test_range_detection_with_location(self):
        """测试位置范围检测。"""
        state = StateContext()
        is_in_range_loc = IsUnitInRangeLoc()

        # 创建单位在距离(0,0)为50的位置
        unit = state.handle_manager.create_unit("hfoo", 0, 30.0, 40.0, 0.0)
        loc = Location(0.0, 0.0)

        assert is_in_range_loc.execute(unit, loc, 50.0) is True
        assert is_in_range_loc.execute(unit, loc, 49.9) is False
