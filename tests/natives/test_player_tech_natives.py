"""玩家科技Native函数测试。"""

import pytest
from unittest.mock import MagicMock
from src.jass_runner.natives.player_tech_natives import SetPlayerTechMaxAllowed
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
