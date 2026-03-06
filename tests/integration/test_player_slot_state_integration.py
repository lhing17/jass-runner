"""玩家插槽状态 native 函数集成测试。"""

import pytest
from src.jass_runner.natives.player import Player
from src.jass_runner.natives.player_slot_state_natives import (
    GetPlayerSlotState,
    ConvertPlayerSlotState,
)


class TestPlayerSlotStateIntegration:
    """测试玩家插槽状态相关 native 函数在 VM 中的集成。"""

    def test_get_player_slot_state_for_player_0(self):
        """测试获取玩家0的插槽状态为 PLAYING。"""
        state_context = None
        player = Player("handle0", 0)

        result = GetPlayerSlotState().execute(state_context, player)

        # 玩家0应该是 PLAYING (1)
        assert result == 1

    def test_get_player_slot_state_for_player_11(self):
        """测试获取玩家11的插槽状态为 PLAYING。"""
        state_context = None
        player = Player("handle11", 11)

        result = GetPlayerSlotState().execute(state_context, player)

        # 玩家11应该是 PLAYING (1)
        assert result == 1

    def test_get_player_slot_state_for_player_12(self):
        """测试获取玩家12的插槽状态为 EMPTY。"""
        state_context = None
        player = Player("handle12", 12)

        result = GetPlayerSlotState().execute(state_context, player)

        # 玩家12应该是 EMPTY (0)
        assert result == 0

    def test_get_player_slot_state_for_player_15(self):
        """测试获取玩家15的插槽状态为 EMPTY。"""
        state_context = None
        player = Player("handle15", 15)

        result = GetPlayerSlotState().execute(state_context, player)

        # 玩家15应该是 EMPTY (0)
        assert result == 0

    def test_get_player_slot_state_returns_empty_for_none(self):
        """测试获取 None 玩家时返回 EMPTY。"""
        state_context = None

        result = GetPlayerSlotState().execute(state_context, None)

        # None 玩家应该返回 EMPTY (0)
        assert result == 0

    def test_convert_player_slot_state_returns_same_value(self):
        """测试 ConvertPlayerSlotState 返回相同的整数值。"""
        state_context = None

        # 测试所有插槽状态
        for i in range(3):
            result = ConvertPlayerSlotState().execute(state_context, i)
            assert result == i

    def test_player_slot_state_matches_player_attribute(self):
        """测试 GetPlayerSlotState 返回的值与 player.slot_state 属性一致。"""
        state_context = None

        # 测试不同玩家ID
        for player_id in [0, 5, 11, 12, 13, 15]:
            player = Player(f"handle{player_id}", player_id)
            result = GetPlayerSlotState().execute(state_context, player)
            assert result == player.slot_state
