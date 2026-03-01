"""测试触发器事件注册相关的原生函数。"""

import logging
from unittest.mock import MagicMock

import pytest


@pytest.fixture
def mock_state_context():
    """创建模拟的状态上下文。"""
    context = MagicMock()
    context.trigger_manager = MagicMock()
    return context


class TestTriggerRegisterTimerEvent:
    """测试 TriggerRegisterTimerEvent 原生函数。"""

    def test_register_timer_event_returns_event_handle(self, mock_state_context):
        """测试 TriggerRegisterTimerEvent 返回事件handle。"""
        from jass_runner.natives.trigger_register_event_natives import TriggerRegisterTimerEvent

        mock_state_context.trigger_manager.register_event.return_value = "event_abc123"

        native = TriggerRegisterTimerEvent()
        assert native.name == "TriggerRegisterTimerEvent"

        result = native.execute(mock_state_context, "trigger_0", 1.0, True)

        assert result == "event_abc123"
        mock_state_context.trigger_manager.register_event.assert_called_once()
        call_args = mock_state_context.trigger_manager.register_event.call_args
        assert call_args[0][0] == "trigger_0"

    def test_register_timer_event_invalid_trigger(self, mock_state_context):
        """测试注册事件到不存在的触发器返回None。"""
        from jass_runner.natives.trigger_register_event_natives import TriggerRegisterTimerEvent

        mock_state_context.trigger_manager.register_event.return_value = None

        native = TriggerRegisterTimerEvent()
        result = native.execute(mock_state_context, "trigger_invalid", 1.0, False)

        assert result is None

    def test_register_timer_event_without_trigger_manager(self, mock_state_context):
        """测试没有trigger_manager时注册事件返回None。"""
        from jass_runner.natives.trigger_register_event_natives import TriggerRegisterTimerEvent

        delattr(mock_state_context, 'trigger_manager')

        native = TriggerRegisterTimerEvent()
        result = native.execute(mock_state_context, "trigger_0", 1.0, True)

        assert result is None


class TestTriggerRegisterTimerExpireEvent:
    """测试 TriggerRegisterTimerExpireEvent 原生函数。"""

    def test_register_timer_expire_event_returns_event_handle(self, mock_state_context):
        """测试 TriggerRegisterTimerExpireEvent 返回事件handle。"""
        from jass_runner.natives.trigger_register_event_natives import TriggerRegisterTimerExpireEvent

        mock_state_context.trigger_manager.register_event.return_value = "event_def456"

        native = TriggerRegisterTimerExpireEvent()
        assert native.name == "TriggerRegisterTimerExpireEvent"

        result = native.execute(mock_state_context, "trigger_0", "timer_0")

        assert result == "event_def456"
        mock_state_context.trigger_manager.register_event.assert_called_once()
        call_args = mock_state_context.trigger_manager.register_event.call_args
        assert call_args[0][0] == "trigger_0"
        assert call_args[0][2]["timer_id"] == "timer_0"

    def test_register_timer_expire_event_invalid_trigger(self, mock_state_context):
        """测试注册计时器过期事件到不存在的触发器返回None。"""
        from jass_runner.natives.trigger_register_event_natives import TriggerRegisterTimerExpireEvent

        mock_state_context.trigger_manager.register_event.return_value = None

        native = TriggerRegisterTimerExpireEvent()
        result = native.execute(mock_state_context, "trigger_invalid", "timer_0")

        assert result is None


class TestTriggerRegisterPlayerUnitEvent:
    """测试 TriggerRegisterPlayerUnitEvent 原生函数。"""

    def test_register_player_unit_event_returns_event_handle(self, mock_state_context):
        """测试 TriggerRegisterPlayerUnitEvent 返回事件handle。"""
        from jass_runner.natives.trigger_register_event_natives import TriggerRegisterPlayerUnitEvent

        mock_state_context.trigger_manager.register_event.return_value = "event_ghi789"

        native = TriggerRegisterPlayerUnitEvent()
        assert native.name == "TriggerRegisterPlayerUnitEvent"

        result = native.execute(mock_state_context, "trigger_0", 0, "player_unit_death", None)

        assert result == "event_ghi789"
        mock_state_context.trigger_manager.register_event.assert_called_once()
        call_args = mock_state_context.trigger_manager.register_event.call_args
        assert call_args[0][0] == "trigger_0"
        assert call_args[0][2]["player_id"] == 0

    def test_register_player_unit_event_invalid_trigger(self, mock_state_context):
        """测试注册玩家单位事件到不存在的触发器返回None。"""
        from jass_runner.natives.trigger_register_event_natives import TriggerRegisterPlayerUnitEvent

        mock_state_context.trigger_manager.register_event.return_value = None

        native = TriggerRegisterPlayerUnitEvent()
        result = native.execute(mock_state_context, "trigger_invalid", 0, "player_unit_death", None)

        assert result is None


class TestTriggerRegisterUnitEvent:
    """测试 TriggerRegisterUnitEvent 原生函数。"""

    def test_register_unit_event_returns_event_handle(self, mock_state_context):
        """测试 TriggerRegisterUnitEvent 返回事件handle。"""
        from jass_runner.natives.trigger_register_event_natives import TriggerRegisterUnitEvent

        mock_state_context.trigger_manager.register_event.return_value = "event_jkl012"

        native = TriggerRegisterUnitEvent()
        assert native.name == "TriggerRegisterUnitEvent"

        result = native.execute(mock_state_context, "trigger_0", "unit_death", None)

        assert result == "event_jkl012"
        mock_state_context.trigger_manager.register_event.assert_called_once()
        call_args = mock_state_context.trigger_manager.register_event.call_args
        assert call_args[0][0] == "trigger_0"

    def test_register_unit_event_invalid_trigger(self, mock_state_context):
        """测试注册单位事件到不存在的触发器返回None。"""
        from jass_runner.natives.trigger_register_event_natives import TriggerRegisterUnitEvent

        mock_state_context.trigger_manager.register_event.return_value = None

        native = TriggerRegisterUnitEvent()
        result = native.execute(mock_state_context, "trigger_invalid", "unit_death", None)

        assert result is None


class TestTriggerRegisterPlayerEvent:
    """测试 TriggerRegisterPlayerEvent 原生函数。"""

    def test_register_player_event_returns_event_handle(self, mock_state_context):
        """测试 TriggerRegisterPlayerEvent 返回事件handle。"""
        from jass_runner.natives.trigger_register_event_natives import TriggerRegisterPlayerEvent

        mock_state_context.trigger_manager.register_event.return_value = "event_mno345"

        native = TriggerRegisterPlayerEvent()
        assert native.name == "TriggerRegisterPlayerEvent"

        result = native.execute(mock_state_context, "trigger_0", 0, "player_defeat")

        assert result == "event_mno345"
        mock_state_context.trigger_manager.register_event.assert_called_once()
        call_args = mock_state_context.trigger_manager.register_event.call_args
        assert call_args[0][0] == "trigger_0"
        assert call_args[0][2]["player_id"] == 0

    def test_register_player_event_invalid_trigger(self, mock_state_context):
        """测试注册玩家事件到不存在的触发器返回None。"""
        from jass_runner.natives.trigger_register_event_natives import TriggerRegisterPlayerEvent

        mock_state_context.trigger_manager.register_event.return_value = None

        native = TriggerRegisterPlayerEvent()
        result = native.execute(mock_state_context, "trigger_invalid", 0, "player_defeat")

        assert result is None


class TestTriggerRegisterGameEvent:
    """测试 TriggerRegisterGameEvent 原生函数。"""

    def test_register_game_event_returns_event_handle(self, mock_state_context):
        """测试 TriggerRegisterGameEvent 返回事件handle。"""
        from jass_runner.natives.trigger_register_event_natives import TriggerRegisterGameEvent

        mock_state_context.trigger_manager.register_event.return_value = "event_pqr678"

        native = TriggerRegisterGameEvent()
        assert native.name == "TriggerRegisterGameEvent"

        result = native.execute(mock_state_context, "trigger_0", "game_timer_expired")

        assert result == "event_pqr678"
        mock_state_context.trigger_manager.register_event.assert_called_once()
        call_args = mock_state_context.trigger_manager.register_event.call_args
        assert call_args[0][0] == "trigger_0"

    def test_register_game_event_invalid_trigger(self, mock_state_context):
        """测试注册游戏事件到不存在的触发器返回None。"""
        from jass_runner.natives.trigger_register_event_natives import TriggerRegisterGameEvent

        mock_state_context.trigger_manager.register_event.return_value = None

        native = TriggerRegisterGameEvent()
        result = native.execute(mock_state_context, "trigger_invalid", "game_timer_expired")

        assert result is None

    def test_register_game_event_without_trigger_manager(self, mock_state_context):
        """测试没有trigger_manager时注册游戏事件返回None。"""
        from jass_runner.natives.trigger_register_event_natives import TriggerRegisterGameEvent

        delattr(mock_state_context, 'trigger_manager')

        native = TriggerRegisterGameEvent()
        result = native.execute(mock_state_context, "trigger_0", "game_timer_expired")

        assert result is None
