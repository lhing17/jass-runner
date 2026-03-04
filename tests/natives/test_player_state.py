"""玩家状态管理测试。"""

from src.jass_runner.natives.handle import Player


def test_player_initial_resources():
    """测试 Player 初始资源值。"""
    player = Player("h001", 0)

    assert player.get_state(1) == 500   # GOLD 初始值
    assert player.get_state(2) == 0     # LUMBER 初始值
    assert player.get_state(4) == 100   # FOOD_CAP 初始值
    assert player.get_state(5) == 0     # FOOD_USED 初始值


def test_player_set_resources():
    """测试设置玩家资源。"""
    player = Player("h002", 0)

    # 设置黄金
    result = player.set_state(1, 1000)
    assert result == 1000
    assert player.get_state(1) == 1000

    # 设置木材
    result = player.set_state(2, 500)
    assert result == 500
    assert player.get_state(2) == 500


def test_player_resource_clamping():
    """测试资源值截断。"""
    player = Player("h003", 0)

    # 测试上限截断
    result = player.set_state(1, 2000000)  # 超过100万
    assert result == 1000000
    assert player.get_state(1) == 1000000

    # 测试下限截断（负数）
    result = player.set_state(1, -100)
    assert result == 0
    assert player.get_state(1) == 0


class TestConvertPlayerState:
    """测试 ConvertPlayerState native 函数。"""

    def test_convert_player_state_returns_input(self):
        """测试 ConvertPlayerState 返回传入的整数。"""
        from unittest.mock import MagicMock
        from src.jass_runner.natives.player_state_natives import (
            ConvertPlayerState,
        )

        native = ConvertPlayerState()
        state_context = MagicMock()

        result = native.execute(state_context, 0)
        assert result == 0

        result = native.execute(state_context, 25)
        assert result == 25

    def test_convert_player_state_with_various_values(self):
        """测试不同 playerstate 值。"""
        from unittest.mock import MagicMock
        from src.jass_runner.natives.player_state_natives import (
            ConvertPlayerState,
        )

        native = ConvertPlayerState()
        state_context = MagicMock()

        # 测试资源状态
        assert native.execute(state_context, 1) == 1  # GOLD
        assert native.execute(state_context, 2) == 2  # LUMBER

        # 测试其他状态
        assert native.execute(state_context, 11) == 11  # OBSERVER
        assert native.execute(state_context, 25) == 25  # NO_CREEP_SLEEP
