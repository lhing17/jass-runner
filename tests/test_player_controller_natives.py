"""玩家控制器 native 函数单元测试。"""

import pytest
from unittest.mock import MagicMock

from jass_runner.natives.player_controller_natives import GetPlayerController, ConvertMapControl


class TestGetPlayerController:
    """测试 GetPlayerController native 函数。"""

    def test_returns_user_for_player_id_0(self):
        """测试玩家0返回 USER 控制器类型。"""
        native = GetPlayerController()
        mock_context = MagicMock()
        mock_player = MagicMock()
        mock_player.player_id = 0
        mock_player.controller = 0  # MAP_CONTROL_USER

        result = native.execute(mock_context, mock_player)

        assert result == mock_player.controller

    def test_returns_computer_for_player_id_9(self):
        """测试玩家9返回 COMPUTER 控制器类型。"""
        native = GetPlayerController()
        mock_context = MagicMock()
        mock_player = MagicMock()
        mock_player.player_id = 9
        mock_player.controller = 1  # MAP_CONTROL_COMPUTER

        result = native.execute(mock_context, mock_player)

        assert result == mock_player.controller

    def test_returns_neutral_for_player_id_13(self):
        """测试玩家13返回 NEUTRAL 控制器类型。"""
        native = GetPlayerController()
        mock_context = MagicMock()
        mock_player = MagicMock()
        mock_player.player_id = 13
        mock_player.controller = 3  # MAP_CONTROL_NEUTRAL

        result = native.execute(mock_context, mock_player)

        assert result == mock_player.controller

    def test_returns_user_when_player_is_none(self):
        """测试玩家为None时返回 USER (0)。"""
        native = GetPlayerController()
        mock_context = MagicMock()

        result = native.execute(mock_context, None)

        assert result == 0


class TestConvertMapControl:
    """测试 ConvertMapControl native 函数。"""

    def test_returns_same_value_for_user(self):
        """测试 USER (0) 转换返回相同值。"""
        native = ConvertMapControl()
        mock_context = MagicMock()

        result = native.execute(mock_context, 0)

        assert result == 0

    def test_returns_same_value_for_computer(self):
        """测试 COMPUTER (1) 转换返回相同值。"""
        native = ConvertMapControl()
        mock_context = MagicMock()

        result = native.execute(mock_context, 1)

        assert result == 1

    def test_returns_same_value_for_neutral(self):
        """测试 NEUTRAL (3) 转换返回相同值。"""
        native = ConvertMapControl()
        mock_context = MagicMock()

        result = native.execute(mock_context, 3)

        assert result == 3

    def test_returns_same_value_for_any_integer(self):
        """测试任意整数转换返回相同值。"""
        native = ConvertMapControl()
        mock_context = MagicMock()

        for i in range(6):
            result = native.execute(mock_context, i)
            assert result == i
