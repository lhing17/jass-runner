"""单位所有权Native函数测试。

此模块包含单位所有权相关native函数的测试用例。
"""

import pytest
from jass_runner.natives.state import StateContext
from jass_runner.natives.unit_ownership_natives import IsUnitOwnedByPlayer


class TestIsUnitOwnedByPlayer:
    """测试IsUnitOwnedByPlayer native函数。"""

    def test_unit_owned_by_correct_player(self):
        """测试单位被正确玩家拥有返回True。"""
        state = StateContext()
        is_owned = IsUnitOwnedByPlayer()

        # 创建玩家0的单位
        unit = state.handle_manager.create_unit("hfoo", 0, 100.0, 200.0, 0.0)
        # 获取玩家0的player对象
        player = state.handle_manager.get_player(0)

        result = is_owned.execute(state, unit, player)

        assert result is True

    def test_unit_not_owned_by_different_player(self):
        """测试单位被不同玩家拥有返回False。"""
        state = StateContext()
        is_owned = IsUnitOwnedByPlayer()

        # 创建玩家0的单位
        unit = state.handle_manager.create_unit("hfoo", 0, 100.0, 200.0, 0.0)
        # 获取玩家1的player对象
        player = state.handle_manager.get_player(1)

        result = is_owned.execute(state, unit, player)

        assert result is False

    def test_null_unit_returns_false(self):
        """测试None单位返回False。"""
        state = StateContext()
        is_owned = IsUnitOwnedByPlayer()

        player = state.handle_manager.get_player(0)

        result = is_owned.execute(state, None, player)

        assert result is False

    def test_null_player_returns_false(self):
        """测试None玩家返回False。"""
        state = StateContext()
        is_owned = IsUnitOwnedByPlayer()

        unit = state.handle_manager.create_unit("hfoo", 0, 100.0, 200.0, 0.0)

        result = is_owned.execute(state, unit, None)

        assert result is False


class TestSetUnitOwner:
    """测试SetUnitOwner native函数。"""

    def test_set_unit_owner_changes_owner(self):
        """测试变更单位所有者。"""
        from jass_runner.natives.unit_ownership_natives import SetUnitOwner
        state = StateContext()
        native = SetUnitOwner()

        # 创建玩家0的单位
        unit = state.handle_manager.create_unit("hfoo", 0, 100.0, 200.0, 0.0)
        # 获取玩家1的player对象
        new_owner = state.handle_manager.get_player(1)

        native.execute(state, unit, new_owner, False)

        assert unit.player_id == 1

    def test_set_unit_owner_with_change_color(self):
        """测试变更单位所有者并改变颜色。"""
        from jass_runner.natives.unit_ownership_natives import SetUnitOwner
        state = StateContext()
        native = SetUnitOwner()

        # 创建玩家0的单位
        unit = state.handle_manager.create_unit("hfoo", 0, 100.0, 200.0, 0.0)
        # 获取玩家2的player对象
        new_owner = state.handle_manager.get_player(2)

        native.execute(state, unit, new_owner, True)

        assert unit.player_id == 2
        # changeColor为True时，单位颜色应改变
        assert unit.color == 2

    def test_null_unit_does_nothing(self):
        """测试null单位不执行操作。"""
        from jass_runner.natives.unit_ownership_natives import SetUnitOwner
        state = StateContext()
        native = SetUnitOwner()

        new_owner = state.handle_manager.get_player(1)

        result = native.execute(state, None, new_owner, False)

        assert result is None

    def test_null_player_does_nothing(self):
        """测试null玩家不执行操作。"""
        from jass_runner.natives.unit_ownership_natives import SetUnitOwner
        state = StateContext()
        native = SetUnitOwner()

        # 创建玩家0的单位
        unit = state.handle_manager.create_unit("hfoo", 0, 100.0, 200.0, 0.0)

        result = native.execute(state, unit, None, False)

        assert result is None
        assert unit.player_id == 0  # 未改变
