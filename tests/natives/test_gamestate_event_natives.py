"""GameState 事件注册 native 函数测试。

此模块包含 TriggerRegisterGameStateEvent native 函数的单元测试。
"""

import pytest
from unittest.mock import Mock

from jass_runner.natives.gamestate_event_natives import TriggerRegisterGameStateEvent
from jass_runner.types.gamestate import FGameState
from jass_runner.types.limitop import LimitOp


class TestTriggerRegisterGameStateEvent:
    """测试 TriggerRegisterGameStateEvent native 函数。"""

    def test_name_is_correct(self):
        """测试函数名称正确。"""
        native = TriggerRegisterGameStateEvent()
        assert native.name == "TriggerRegisterGameStateEvent"

    def test_execute_registers_listener(self):
        """测试执行时注册监听器。"""
        native = TriggerRegisterGameStateEvent()

        mock_state_context = Mock()
        mock_gamestate_manager = Mock()
        mock_gamestate_manager.register_state_listener.return_value = "event_001"
        mock_state_context.game_state_manager = mock_gamestate_manager

        result = native.execute(
            mock_state_context,
            "trigger_001",
            FGameState.TIME_OF_DAY,
            LimitOp.EQUAL,
            6.0
        )

        assert result == "event_001"
        mock_gamestate_manager.register_state_listener.assert_called_once_with(
            "trigger_001",
            FGameState.TIME_OF_DAY,
            LimitOp.EQUAL,
            6.0
        )

    def test_execute_without_game_state_manager(self):
        """测试没有 game_state_manager 时返回 None。"""
        native = TriggerRegisterGameStateEvent()

        mock_state_context = Mock()
        # 不设置 game_state_manager
        del mock_state_context.game_state_manager

        result = native.execute(
            mock_state_context,
            "trigger_001",
            FGameState.TIME_OF_DAY,
            LimitOp.EQUAL,
            6.0
        )

        assert result is None

    def test_execute_with_none_state_context(self):
        """测试 state_context 为 None 时返回 None。"""
        native = TriggerRegisterGameStateEvent()

        result = native.execute(
            None,
            "trigger_001",
            FGameState.TIME_OF_DAY,
            LimitOp.EQUAL,
            6.0
        )

        assert result is None
