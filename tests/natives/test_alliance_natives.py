"""联盟相关 native 函数测试。"""

import pytest
from unittest.mock import MagicMock
from src.jass_runner.natives.alliance_natives import ConvertAllianceType
from src.jass_runner.natives.alliance import ALLIANCE_PASSIVE, ALLIANCE_SHARED_VISION


class TestConvertAllianceType:
    """测试 ConvertAllianceType native 函数。"""

    def test_convert_alliance_type_returns_input(self):
        """测试 ConvertAllianceType 返回传入的整数。"""
        native = ConvertAllianceType()
        state_context = MagicMock()

        result = native.execute(state_context, 0)
        assert result == 0

        result = native.execute(state_context, 5)
        assert result == 5

    def test_convert_alliance_type_with_constants(self):
        """测试使用联盟常量。"""
        native = ConvertAllianceType()
        state_context = MagicMock()

        assert native.execute(state_context, ALLIANCE_PASSIVE) == ALLIANCE_PASSIVE
        assert native.execute(state_context, ALLIANCE_SHARED_VISION) == ALLIANCE_SHARED_VISION


class TestSetPlayerAlliance:
    """测试 SetPlayerAlliance native 函数。"""

    def test_set_alliance_true(self):
        """测试设置联盟关系为 true。"""
        from src.jass_runner.natives.alliance_manager import AllianceManager
        from src.jass_runner.natives.alliance_natives import SetPlayerAlliance

        native = SetPlayerAlliance()
        state_context = MagicMock()
        state_context.alliance_manager = AllianceManager()

        player0 = MagicMock()
        player0.player_id = 0
        player1 = MagicMock()
        player1.player_id = 1

        native.execute(state_context, player0, player1, ALLIANCE_PASSIVE, True)

        assert state_context.alliance_manager.get_alliance(0, 1, ALLIANCE_PASSIVE) is True

    def test_set_alliance_false(self):
        """测试设置联盟关系为 false。"""
        from src.jass_runner.natives.alliance_manager import AllianceManager
        from src.jass_runner.natives.alliance_natives import SetPlayerAlliance

        native = SetPlayerAlliance()
        state_context = MagicMock()
        state_context.alliance_manager = AllianceManager()

        player0 = MagicMock()
        player0.player_id = 0
        player1 = MagicMock()
        player1.player_id = 1

        # 先设置再取消
        native.execute(state_context, player0, player1, ALLIANCE_PASSIVE, True)
        native.execute(state_context, player0, player1, ALLIANCE_PASSIVE, False)

        assert state_context.alliance_manager.get_alliance(0, 1, ALLIANCE_PASSIVE) is False

    def test_set_alliance_with_none_player(self):
        """测试传入 None player 时的处理。"""
        from src.jass_runner.natives.alliance_manager import AllianceManager
        from src.jass_runner.natives.alliance_natives import SetPlayerAlliance

        native = SetPlayerAlliance()
        state_context = MagicMock()
        state_context.alliance_manager = AllianceManager()

        # 不应抛出异常
        native.execute(state_context, None, MagicMock(), ALLIANCE_PASSIVE, True)
        native.execute(state_context, MagicMock(), None, ALLIANCE_PASSIVE, True)


class TestGetPlayerAlliance:
    """测试 GetPlayerAlliance native 函数。"""

    def test_get_alliance_true(self):
        """测试获取已启用的联盟关系。"""
        from src.jass_runner.natives.alliance_manager import AllianceManager
        from src.jass_runner.natives.alliance_natives import GetPlayerAlliance

        native = GetPlayerAlliance()
        state_context = MagicMock()
        state_context.alliance_manager = AllianceManager()

        player0 = MagicMock()
        player0.player_id = 0
        player1 = MagicMock()
        player1.player_id = 1

        # 先设置
        state_context.alliance_manager.set_alliance(0, 1, ALLIANCE_PASSIVE, True)

        result = native.execute(state_context, player0, player1, ALLIANCE_PASSIVE)
        assert result is True

    def test_get_alliance_false(self):
        """测试获取未启用的联盟关系。"""
        from src.jass_runner.natives.alliance_manager import AllianceManager
        from src.jass_runner.natives.alliance_natives import GetPlayerAlliance

        native = GetPlayerAlliance()
        state_context = MagicMock()
        state_context.alliance_manager = AllianceManager()

        player0 = MagicMock()
        player0.player_id = 0
        player1 = MagicMock()
        player1.player_id = 1

        result = native.execute(state_context, player0, player1, ALLIANCE_PASSIVE)
        assert result is False

    def test_get_alliance_with_none_player(self):
        """测试传入 None player 时返回 False。"""
        from src.jass_runner.natives.alliance_manager import AllianceManager
        from src.jass_runner.natives.alliance_natives import GetPlayerAlliance

        native = GetPlayerAlliance()
        state_context = MagicMock()
        state_context.alliance_manager = AllianceManager()

        result = native.execute(state_context, None, MagicMock(), ALLIANCE_PASSIVE)
        assert result is False

        result = native.execute(state_context, MagicMock(), None, ALLIANCE_PASSIVE)
        assert result is False
