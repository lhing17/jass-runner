"""玩家科技功能测试。"""

import pytest
from src.jass_runner.natives.player import Player


class TestPlayerTech:
    """测试Player类的科技功能。"""

    def test_set_and_get_tech_max_allowed(self):
        """测试设置和获取科技最大允许等级。"""
        player = Player("test_handle", 0)
        tech_id = 1214542384  # 'Hpal'的FourCC值

        player.set_tech_max_allowed(tech_id, 5)
        assert player.get_tech_max_allowed(tech_id) == 5

    def test_get_tech_max_allowed_default(self):
        """测试获取未设置的科技最大允许等级返回0。"""
        player = Player("test_handle", 0)
        tech_id = 1214542384

        assert player.get_tech_max_allowed(tech_id) == 0

    def test_set_and_get_tech_researched(self):
        """测试设置和获取科技研究等级。"""
        player = Player("test_handle", 0)
        tech_id = 1214542384

        player.set_tech_researched(tech_id, 3)
        assert player.get_tech_researched(tech_id, False) is True
        assert player.get_tech_count(tech_id, False) == 3

    def test_add_tech_researched(self):
        """测试增加科技研究等级。"""
        player = Player("test_handle", 0)
        tech_id = 1214542384

        player.set_tech_researched(tech_id, 1)
        player.add_tech_researched(tech_id, 2)
        assert player.get_tech_count(tech_id, False) == 3

    def test_get_tech_researched_false(self):
        """测试未研究的科技返回False。"""
        player = Player("test_handle", 0)
        tech_id = 1214542384

        assert player.get_tech_researched(tech_id, False) is False

    def test_get_tech_count_default(self):
        """测试获取未设置的科技等级返回0。"""
        player = Player("test_handle", 0)
        tech_id = 1214542384

        assert player.get_tech_count(tech_id, False) == 0
