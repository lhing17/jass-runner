"""玩家相关 native 函数测试。"""

import pytest
from src.jass_runner.natives.player_state_natives import GetPlayerState
from src.jass_runner.natives.state import StateContext
from src.jass_runner.natives.handle import Player


def test_get_player_state():
    """测试 GetPlayerState native 函数。"""
    # 准备
    state_context = StateContext()
    native = GetPlayerState()

    player = state_context.handle_manager.get_player(0)
    result = native.execute(state_context, player, 1)  # GOLD

    assert result == 500  # 初始黄金


def test_get_player_state_lumber():
    """测试 GetPlayerState 获取木材。"""
    state_context = StateContext()
    native = GetPlayerState()

    player = state_context.handle_manager.get_player(0)
    result = native.execute(state_context, player, 2)  # LUMBER

    assert result == 0  # 初始木材


def test_get_player_state_food_cap():
    """测试 GetPlayerState 获取人口上限。"""
    state_context = StateContext()
    native = GetPlayerState()

    player = state_context.handle_manager.get_player(0)
    result = native.execute(state_context, player, 4)  # FOOD_CAP

    assert result == 100  # 初始人口上限


def test_get_player_state_food_used():
    """测试 GetPlayerState 获取已用人口。"""
    state_context = StateContext()
    native = GetPlayerState()

    player = state_context.handle_manager.get_player(0)
    result = native.execute(state_context, player, 5)  # FOOD_USED

    assert result == 0  # 初始已用人口


def test_get_player_state_with_none_player():
    """测试 GetPlayerState 处理 None 玩家。"""
    state_context = StateContext()
    native = GetPlayerState()

    result = native.execute(state_context, None, 1)

    assert result == 0


def test_get_player_state_different_player():
    """测试不同玩家的状态值。"""
    state_context = StateContext()
    native = GetPlayerState()

    # 获取玩家 0 和玩家 1
    player0 = state_context.handle_manager.get_player(0)
    player1 = state_context.handle_manager.get_player(1)

    # 修改玩家黄金
    player0._gold = 2000
    player1._gold = 1000

    result0 = native.execute(state_context, player0, 1)
    result1 = native.execute(state_context, player1, 1)

    assert result0 == 2000
    assert result1 == 1000
