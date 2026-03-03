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
