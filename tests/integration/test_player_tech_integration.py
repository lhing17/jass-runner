"""玩家科技系统集成测试。"""

import pytest
from src.jass_runner.natives.player import Player
from src.jass_runner.natives.player_tech_natives import (
    SetPlayerTechMaxAllowed,
    GetPlayerTechMaxAllowed,
    AddPlayerTechResearched,
    SetPlayerTechResearched,
    GetPlayerTechResearched,
    GetPlayerTechCount,
)


class TestPlayerTechIntegration:
    """测试玩家科技系统完整工作流程。"""

    def test_complete_tech_research_flow(self):
        """测试完整的科技研究流程。"""
        state_context = None
        player = Player("test_handle", 0)
        tech_id = 1214542384  # 'Hpal'

        # 设置最大允许等级
        SetPlayerTechMaxAllowed().execute(state_context, player, tech_id, 5)
        assert GetPlayerTechMaxAllowed().execute(state_context, player, tech_id) == 5

        # 初始未研究
        assert GetPlayerTechResearched().execute(state_context, player, tech_id, False) is False
        assert GetPlayerTechCount().execute(state_context, player, tech_id, False) == 0

        # 研究科技
        SetPlayerTechResearched().execute(state_context, player, tech_id, 2)
        assert GetPlayerTechResearched().execute(state_context, player, tech_id, False) is True
        assert GetPlayerTechCount().execute(state_context, player, tech_id, False) == 2

        # 增加研究等级
        AddPlayerTechResearched().execute(state_context, player, tech_id, 2)
        assert GetPlayerTechCount().execute(state_context, player, tech_id, False) == 4

    def test_multi_player_tech_isolation(self):
        """测试多玩家科技独立。"""
        state_context = None
        player0 = Player("handle0", 0)
        player1 = Player("handle1", 1)
        tech_id = 1214542384

        # 玩家0研究科技
        SetPlayerTechResearched().execute(state_context, player0, tech_id, 3)

        # 玩家1未研究
        assert GetPlayerTechCount().execute(state_context, player1, tech_id, False) == 0
        assert GetPlayerTechResearched().execute(state_context, player1, tech_id, False) is False

        # 玩家0有研究
        assert GetPlayerTechCount().execute(state_context, player0, tech_id, False) == 3
        assert GetPlayerTechResearched().execute(state_context, player0, tech_id, False) is True

    def test_multiple_techs(self):
        """测试多个科技独立管理。"""
        state_context = None
        player = Player("test_handle", 0)
        tech1 = 1214542384  # 'Hpal'
        tech2 = 1214542385  # 'Hmkg'

        SetPlayerTechResearched().execute(state_context, player, tech1, 2)
        SetPlayerTechResearched().execute(state_context, player, tech2, 5)

        assert GetPlayerTechCount().execute(state_context, player, tech1, False) == 2
        assert GetPlayerTechCount().execute(state_context, player, tech2, False) == 5
