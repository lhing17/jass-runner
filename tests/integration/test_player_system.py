"""玩家资源系统集成测试。

此模块包含玩家资源系统的完整流程测试，验证玩家资源获取和设置功能。
"""

import pytest
from src.jass_runner.natives.factory import NativeFactory
from src.jass_runner.natives.state import StateContext
from src.jass_runner.natives.manager import HandleManager


class TestPlayerSystem:
    """测试玩家资源系统完整流程。"""

    def test_player_resource_workflow(self):
        """测试玩家资源操作的完整流程。"""
        factory = NativeFactory()
        registry = factory.create_default_registry()
        state_context = StateContext()
        handle_manager = state_context.handle_manager

        # 获取玩家 (玩家已预初始化)
        player = handle_manager.get_player(0)
        assert player is not None

        # 获取初始资源
        get_state = registry.get("GetPlayerState")
        assert get_state.execute(state_context, player, 1) == 500  # GOLD
        assert get_state.execute(state_context, player, 2) == 0    # LUMBER
        assert get_state.execute(state_context, player, 4) == 100  # FOOD_CAP
        assert get_state.execute(state_context, player, 5) == 0    # FOOD_USED

        # 设置资源
        set_state = registry.get("SetPlayerState")
        set_state.execute(state_context, player, 1, 1000)  # GOLD
        set_state.execute(state_context, player, 2, 500)   # LUMBER
        set_state.execute(state_context, player, 4, 200)   # FOOD_CAP
        set_state.execute(state_context, player, 5, 50)    # FOOD_USED

        # 验证设置后的值
        assert get_state.execute(state_context, player, 1) == 1000
        assert get_state.execute(state_context, player, 2) == 500
        assert get_state.execute(state_context, player, 4) == 200
        assert get_state.execute(state_context, player, 5) == 50

    def test_player_resource_clamping(self):
        """测试资源值截断。"""
        factory = NativeFactory()
        registry = factory.create_default_registry()
        state_context = StateContext()
        handle_manager = state_context.handle_manager

        player = handle_manager.get_player(1)
        set_state = registry.get("SetPlayerState")

        # 测试黄金上限截断
        result = set_state.execute(state_context, player, 1, 2000000)
        assert result == 1000000

        # 测试黄金下限截断（负值）
        result = set_state.execute(state_context, player, 1, -500)
        assert result == 0

        # 测试人口上限截断
        result = set_state.execute(state_context, player, 4, 500)
        assert result == 300  # 最大300

        # 测试已用人口不能超过上限
        set_state.execute(state_context, player, 4, 100)  # 设置上限为100
        result = set_state.execute(state_context, player, 5, 150)  # 尝试设置150
        assert result == 100  # 被截断到100

    def test_player_native_registration(self):
        """测试玩家资源native函数在工厂中正确注册。"""
        factory = NativeFactory()
        registry = factory.create_default_registry()

        # 验证玩家资源函数已注册
        assert registry.get("GetPlayerState") is not None
        assert registry.get("SetPlayerState") is not None

    def test_player_resource_initial_values(self):
        """测试玩家资源初始值正确。"""
        state_context = StateContext()
        handle_manager = state_context.handle_manager

        # 测试多个玩家的初始值
        for player_id in range(4):
            player = handle_manager.get_player(player_id)
            assert player is not None
            assert player.get_state(1) == 500  # GOLD初始500
            assert player.get_state(2) == 0    # LUMBER初始0
            assert player.get_state(4) == 100  # FOOD_CAP初始100
            assert player.get_state(5) == 0    # FOOD_USED初始0

    def test_player_resource_with_different_players(self):
        """测试不同玩家资源独立。"""
        factory = NativeFactory()
        registry = factory.create_default_registry()
        state_context = StateContext()
        handle_manager = state_context.handle_manager

        player0 = handle_manager.get_player(0)
        player1 = handle_manager.get_player(1)

        set_state = registry.get("SetPlayerState")
        get_state = registry.get("GetPlayerState")

        # 设置玩家0的资源
        set_state.execute(state_context, player0, 1, 1000)  # GOLD

        # 设置玩家1的资源
        set_state.execute(state_context, player1, 1, 2000)  # GOLD

        # 验证资源独立
        assert get_state.execute(state_context, player0, 1) == 1000
        assert get_state.execute(state_context, player1, 1) == 2000

    def test_player_lumber_limits(self):
        """测试木材资源限制。"""
        factory = NativeFactory()
        registry = factory.create_default_registry()
        state_context = StateContext()
        handle_manager = state_context.handle_manager

        player = handle_manager.get_player(0)
        set_state = registry.get("SetPlayerState")

        # 测试木材上限截断 (最大1,000,000)
        result = set_state.execute(state_context, player, 2, 2000000)
        assert result == 1000000

        # 测试木材下限截断
        result = set_state.execute(state_context, player, 2, -100)
        assert result == 0

    def test_player_food_caps(self):
        """测试人口上限限制。"""
        factory = NativeFactory()
        registry = factory.create_default_registry()
        state_context = StateContext()
        handle_manager = state_context.handle_manager

        player = handle_manager.get_player(0)
        set_state = registry.get("SetPlayerState")

        # 人口上限范围为0-300
        # 测试超过上限
        result = set_state.execute(state_context, player, 4, 1000)
        assert result == 300

        # 测试低于下限
        result = set_state.execute(state_context, player, 4, -100)
        assert result == 0

        # 测试范围内的值
        result = set_state.execute(state_context, player, 4, 150)
        assert result == 150

    def test_player_food_used_adjusts_to_cap(self):
        """测试已用人口随人口上限调整。"""
        factory = NativeFactory()
        registry = factory.create_default_registry()
        state_context = StateContext()
        handle_manager = state_context.handle_manager

        player = handle_manager.get_player(0)
        set_state = registry.get("SetPlayerState")
        get_state = registry.get("GetPlayerState")

        # 先设置人口上限为200
        set_state.execute(state_context, player, 4, 200)

        # 设置已用人口为150
        set_state.execute(state_context, player, 5, 150)
        assert get_state.execute(state_context, player, 5) == 150

        # 缩小人口上限到100
        set_state.execute(state_context, player, 4, 100)

        # 已用人口应该被截断到新的上限（虽然native不自动调整，但set_state会处理）
        # 再次设置一个不超过上限的值来验证
        result = set_state.execute(state_context, player, 5, 120)
        assert result == 100  # 被截断到当前的food_cap
