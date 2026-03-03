"""Player类测试。

此模块包含Player类的单元测试，特别是关系管理功能。
"""

import pytest
from src.jass_runner.natives.handle import Player


class TestPlayerAlliance:
    """测试Player类的盟友/敌对关系管理功能。"""

    def test_player_default_no_alliance(self):
        """测试Player默认无任何关系。"""
        # 准备
        player = Player("player_0", 0)

        # 验证
        assert not player.is_ally(1)
        assert not player.is_enemy(1)
        assert not player.is_ally(2)
        assert not player.is_enemy(2)

    def test_player_set_alliance_true(self):
        """测试设置其他玩家为盟友。"""
        # 准备
        player = Player("player_0", 0)

        # 执行
        player.set_alliance(1, True)

        # 验证
        assert player.is_ally(1)
        assert not player.is_enemy(1)

    def test_player_set_alliance_false(self):
        """测试设置其他玩家为敌人。"""
        # 准备
        player = Player("player_0", 0)

        # 执行
        player.set_alliance(1, False)

        # 验证
        assert not player.is_ally(1)
        assert player.is_enemy(1)

    def test_player_alliance_mutual_exclusive(self):
        """测试盟友和敌人关系互斥。"""
        # 准备
        player = Player("player_0", 0)

        # 先设为盟友
        player.set_alliance(1, True)
        assert player.is_ally(1)
        assert not player.is_enemy(1)

        # 改为敌人
        player.set_alliance(1, False)
        assert not player.is_ally(1)
        assert player.is_enemy(1)

        # 改回盟友
        player.set_alliance(1, True)
        assert player.is_ally(1)
        assert not player.is_enemy(1)
