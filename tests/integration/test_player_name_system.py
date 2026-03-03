"""玩家名称系统集成测试。"""

import pytest
from src.jass_runner.natives.factory import NativeFactory
from src.jass_runner.natives.state import StateContext


class TestPlayerNameSystem:
    """测试玩家名称系统完整流程。"""

    def test_player_name_workflow(self):
        """测试玩家名称获取和设置的完整流程。"""
        factory = NativeFactory()
        registry = factory.create_default_registry()
        state_context = StateContext()

        # 创建玩家（通过 handle_manager）
        player = state_context.handle_manager.get_player(0)

        # 获取默认名称
        get_name = registry.get("GetPlayerName")
        assert get_name.execute(state_context, player) == "玩家0"

        # 设置新名称
        set_name = registry.get("SetPlayerName")
        set_name.execute(state_context, player, "张三")

        # 验证新名称
        assert get_name.execute(state_context, player) == "张三"
