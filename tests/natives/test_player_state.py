"""玩家状态管理测试。"""

import pytest
from src.jass_runner.natives.handle import Player


def test_player_initial_resources():
    """测试 Player 初始资源值。"""
    player = Player("h001", 0)

    assert player.get_state(1) == 500   # GOLD 初始值
    assert player.get_state(2) == 0     # LUMBER 初始值
    assert player.get_state(4) == 100   # FOOD_CAP 初始值
    assert player.get_state(5) == 0     # FOOD_USED 初始值


def test_player_set_resources():
    """测试设置玩家资源。"""
    player = Player("h002", 0)

    # 设置黄金
    result = player.set_state(1, 1000)
    assert result == 1000
    assert player.get_state(1) == 1000

    # 设置木材
    result = player.set_state(2, 500)
    assert result == 500
    assert player.get_state(2) == 500


def test_player_resource_clamping():
    """测试资源值截断。"""
    player = Player("h003", 0)

    # 测试上限截断
    result = player.set_state(1, 2000000)  # 超过100万
    assert result == 1000000
    assert player.get_state(1) == 1000000

    # 测试下限截断（负数）
    result = player.set_state(1, -100)
    assert result == 0
    assert player.get_state(1) == 0
