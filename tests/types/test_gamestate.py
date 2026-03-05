"""GameState 类型测试。"""

import pytest
from jass_runner.types.gamestate import IGameState, FGameState


class TestIGameState:
    """测试 IGameState 类型。"""

    def test_divine_intervention_constant(self):
        """测试 DIVINE_INTERVENTION 常量值。"""
        assert IGameState.DIVINE_INTERVENTION == 0

    def test_disconnected_constant(self):
        """测试 DISCONNECTED 常量值。"""
        assert IGameState.DISCONNECTED == 1


class TestFGameState:
    """测试 FGameState 类型。"""

    def test_time_of_day_constant(self):
        """测试 TIME_OF_DAY 常量值。"""
        assert FGameState.TIME_OF_DAY == 2
