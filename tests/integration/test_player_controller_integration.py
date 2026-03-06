"""玩家控制器 native 函数集成测试。"""

import pytest
from src.jass_runner.natives.player import Player
from src.jass_runner.natives.player_controller_natives import (
    GetPlayerController,
    ConvertMapControl,
)


class TestPlayerControllerIntegration:
    """测试玩家控制器相关 native 函数在 VM 中的集成。"""

    def test_get_player_controller_for_player_0(self):
        """测试获取玩家0的控制器类型为 USER。"""
        state_context = None
        player = Player("handle0", 0)

        result = GetPlayerController().execute(state_context, player)

        # 玩家0应该是 USER (0)
        assert result == 0

    def test_get_player_controller_for_player_9(self):
        """测试获取玩家9的控制器类型为 COMPUTER。"""
        state_context = None
        player = Player("handle9", 9)

        result = GetPlayerController().execute(state_context, player)

        # 玩家9应该是 COMPUTER (1)
        assert result == 1

    def test_get_player_controller_for_player_13(self):
        """测试获取玩家13的控制器类型为 NEUTRAL。"""
        state_context = None
        player = Player("handle13", 13)

        result = GetPlayerController().execute(state_context, player)

        # 玩家13应该是 NEUTRAL (3)
        assert result == 3

    def test_get_player_controller_returns_user_for_none(self):
        """测试获取 None 玩家时返回 USER。"""
        state_context = None

        result = GetPlayerController().execute(state_context, None)

        # None 玩家应该返回 USER (0)
        assert result == 0

    def test_convert_map_control_returns_same_value(self):
        """测试 ConvertMapControl 返回相同的整数值。"""
        state_context = None

        # 测试所有控制器类型
        for i in range(6):
            result = ConvertMapControl().execute(state_context, i)
            assert result == i

    def test_player_controller_matches_player_attribute(self):
        """测试 GetPlayerController 返回的值与 player.controller 属性一致。"""
        state_context = None

        # 测试不同玩家ID
        for player_id in [0, 5, 8, 11, 12, 15]:
            player = Player(f"handle{player_id}", player_id)
            result = GetPlayerController().execute(state_context, player)
            assert result == player.controller
