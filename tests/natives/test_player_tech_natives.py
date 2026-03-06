"""玩家科技Native函数测试。"""

import pytest
from unittest.mock import MagicMock
from src.jass_runner.natives.player_tech_natives import SetPlayerTechMaxAllowed, GetPlayerTechMaxAllowed, AddPlayerTechResearched, SetPlayerTechResearched, GetPlayerTechResearched
from src.jass_runner.natives.player import Player


class TestSetPlayerTechMaxAllowed:
    """测试SetPlayerTechMaxAllowed native函数。"""

    def test_set_player_tech_max_allowed(self):
        """测试设置玩家科技最大允许等级。"""
        native = SetPlayerTechMaxAllowed()
        state_context = MagicMock()
        player = Player("test_handle", 0)
        tech_id = 1214542384  # 'Hpal'

        result = native.execute(state_context, player, tech_id, 5)
        assert result is None
        assert player.get_tech_max_allowed(tech_id) == 5

    def test_set_player_tech_max_allowed_none_player(self):
        """测试player为None时的处理。"""
        native = SetPlayerTechMaxAllowed()
        state_context = MagicMock()

        result = native.execute(state_context, None, 1214542384, 5)
        assert result is None


class TestGetPlayerTechMaxAllowed:
    """测试GetPlayerTechMaxAllowed native函数。"""

    def test_get_player_tech_max_allowed(self):
        """测试获取玩家科技最大允许等级。"""
        native = GetPlayerTechMaxAllowed()
        state_context = MagicMock()
        player = Player("test_handle", 0)
        tech_id = 1214542384

        player.set_tech_max_allowed(tech_id, 5)
        result = native.execute(state_context, player, tech_id)
        assert result == 5

    def test_get_player_tech_max_allowed_default(self):
        """测试获取未设置的科技最大允许等级返回0。"""
        native = GetPlayerTechMaxAllowed()
        state_context = MagicMock()
        player = Player("test_handle", 0)
        tech_id = 1214542384

        result = native.execute(state_context, player, tech_id)
        assert result == 0

    def test_get_player_tech_max_allowed_none_player(self):
        """测试player为None时返回0。"""
        native = GetPlayerTechMaxAllowed()
        state_context = MagicMock()

        result = native.execute(state_context, None, 1214542384)
        assert result == 0


class TestAddPlayerTechResearched:
    """测试AddPlayerTechResearched native函数。"""

    def test_add_player_tech_researched(self):
        """测试增加玩家科技研究等级。"""
        native = AddPlayerTechResearched()
        state_context = MagicMock()
        player = Player("test_handle", 0)
        tech_id = 1214542384

        player.set_tech_researched(tech_id, 1)
        result = native.execute(state_context, player, tech_id, 2)
        assert result is None
        assert player.get_tech_count(tech_id, False) == 3

    def test_add_player_tech_researched_none_player(self):
        """测试player为None时的处理。"""
        native = AddPlayerTechResearched()
        state_context = MagicMock()

        result = native.execute(state_context, None, 1214542384, 2)
        assert result is None


class TestSetPlayerTechResearched:
    """测试SetPlayerTechResearched native函数。"""

    def test_set_player_tech_researched(self):
        """测试设置玩家科技研究等级。"""
        native = SetPlayerTechResearched()
        state_context = MagicMock()
        player = Player("test_handle", 0)
        tech_id = 1214542384

        result = native.execute(state_context, player, tech_id, 5)
        assert result is None
        assert player.get_tech_count(tech_id, False) == 5

    def test_set_player_tech_researched_none_player(self):
        """测试player为None时的处理。"""
        native = SetPlayerTechResearched()
        state_context = MagicMock()

        result = native.execute(state_context, None, 1214542384, 5)
        assert result is None


class TestGetPlayerTechResearched:
    """测试GetPlayerTechResearched native函数。"""

    def test_get_player_tech_researched_true(self):
        """测试获取已研究的科技返回True。"""
        native = GetPlayerTechResearched()
        state_context = MagicMock()
        player = Player("test_handle", 0)
        tech_id = 1214542384

        player.set_tech_researched(tech_id, 3)
        result = native.execute(state_context, player, tech_id, False)
        assert result is True

    def test_get_player_tech_researched_false(self):
        """测试获取未研究的科技返回False。"""
        native = GetPlayerTechResearched()
        state_context = MagicMock()
        player = Player("test_handle", 0)
        tech_id = 1214542384

        result = native.execute(state_context, player, tech_id, False)
        assert result is False

    def test_get_player_tech_researched_zero_level(self):
        """测试等级为0时返回False。"""
        native = GetPlayerTechResearched()
        state_context = MagicMock()
        player = Player("test_handle", 0)
        tech_id = 1214542384

        player.set_tech_researched(tech_id, 0)
        result = native.execute(state_context, player, tech_id, False)
        assert result is False

    def test_get_player_tech_researched_none_player(self):
        """测试player为None时返回False。"""
        native = GetPlayerTechResearched()
        state_context = MagicMock()

        result = native.execute(state_context, None, 1214542384, False)
        assert result is False
