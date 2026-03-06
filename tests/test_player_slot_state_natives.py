"""玩家插槽状态 native 函数单元测试。"""

import pytest
from unittest.mock import MagicMock

from jass_runner.natives.player_slot_state_natives import GetPlayerSlotState, ConvertPlayerSlotState


class TestGetPlayerSlotState:
    """测试 GetPlayerSlotState native 函数。"""

    def test_returns_playing_for_player_id_0(self):
        """测试玩家0返回 PLAYING 插槽状态。"""
        native = GetPlayerSlotState()
        mock_context = MagicMock()
        mock_player = MagicMock()
        mock_player.player_id = 0
        mock_player.slot_state = 1  # PLAYER_SLOT_STATE_PLAYING

        result = native.execute(mock_context, mock_player)

        assert result == mock_player.slot_state

    def test_returns_playing_for_player_id_11(self):
        """测试玩家11返回 PLAYING 插槽状态。"""
        native = GetPlayerSlotState()
        mock_context = MagicMock()
        mock_player = MagicMock()
        mock_player.player_id = 11
        mock_player.slot_state = 1  # PLAYER_SLOT_STATE_PLAYING

        result = native.execute(mock_context, mock_player)

        assert result == mock_player.slot_state

    def test_returns_empty_for_player_id_12(self):
        """测试玩家12返回 EMPTY 插槽状态。"""
        native = GetPlayerSlotState()
        mock_context = MagicMock()
        mock_player = MagicMock()
        mock_player.player_id = 12
        mock_player.slot_state = 0  # PLAYER_SLOT_STATE_EMPTY

        result = native.execute(mock_context, mock_player)

        assert result == mock_player.slot_state

    def test_returns_empty_for_player_id_15(self):
        """测试玩家15返回 EMPTY 插槽状态。"""
        native = GetPlayerSlotState()
        mock_context = MagicMock()
        mock_player = MagicMock()
        mock_player.player_id = 15
        mock_player.slot_state = 0  # PLAYER_SLOT_STATE_EMPTY

        result = native.execute(mock_context, mock_player)

        assert result == mock_player.slot_state

    def test_returns_empty_when_player_is_none(self):
        """测试玩家为None时返回 EMPTY (0)。"""
        native = GetPlayerSlotState()
        mock_context = MagicMock()

        result = native.execute(mock_context, None)

        assert result == 0


class TestConvertPlayerSlotState:
    """测试 ConvertPlayerSlotState native 函数。"""

    def test_returns_same_value_for_empty(self):
        """测试 EMPTY (0) 转换返回相同值。"""
        native = ConvertPlayerSlotState()
        mock_context = MagicMock()

        result = native.execute(mock_context, 0)

        assert result == 0

    def test_returns_same_value_for_playing(self):
        """测试 PLAYING (1) 转换返回相同值。"""
        native = ConvertPlayerSlotState()
        mock_context = MagicMock()

        result = native.execute(mock_context, 1)

        assert result == 1

    def test_returns_same_value_for_left(self):
        """测试 LEFT (2) 转换返回相同值。"""
        native = ConvertPlayerSlotState()
        mock_context = MagicMock()

        result = native.execute(mock_context, 2)

        assert result == 2

    def test_returns_same_value_for_any_integer(self):
        """测试任意整数转换返回相同值。"""
        native = ConvertPlayerSlotState()
        mock_context = MagicMock()

        for i in range(3):
            result = native.execute(mock_context, i)
            assert result == i
