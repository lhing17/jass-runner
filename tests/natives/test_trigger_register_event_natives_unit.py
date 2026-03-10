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
        from jass_runner.natives.event_handles import PlayerUnitEvent
        from jass_runner.trigger.event_types import EVENT_PLAYER_UNIT_DEATH

        mock_state_context.trigger_manager.register_event.return_value = "event_ghi789"

        native = TriggerRegisterPlayerUnitEvent()
        assert native.name == "TriggerRegisterPlayerUnitEvent"

        event = PlayerUnitEvent("playerunitevent_001", EVENT_PLAYER_UNIT_DEATH)
        result = native.execute(mock_state_context, "trigger_0", 0, event, None)

        assert result == "event_ghi789"
        mock_state_context.trigger_manager.register_event.assert_called_once()
        call_args = mock_state_context.trigger_manager.register_event.call_args
        assert call_args[0][0] == "trigger_0"
        assert call_args[0][2]["player_id"] == 0

    def test_register_player_unit_event_invalid_trigger(self, mock_state_context):
        """测试注册玩家单位事件到不存在的触发器返回None。"""
        from jass_runner.natives.trigger_register_event_natives import TriggerRegisterPlayerUnitEvent
        from jass_runner.natives.event_handles import PlayerUnitEvent
        from jass_runner.trigger.event_types import EVENT_PLAYER_UNIT_DEATH

        mock_state_context.trigger_manager.register_event.return_value = None

        native = TriggerRegisterPlayerUnitEvent()
        event = PlayerUnitEvent("playerunitevent_001", EVENT_PLAYER_UNIT_DEATH)
        result = native.execute(mock_state_context, "trigger_invalid", 0, event, None)

        assert result is None


class TestTriggerRegisterUnitEvent:
    """测试 TriggerRegisterUnitEvent 原生函数。"""

    def test_register_unit_event_returns_event_handle(self, mock_state_context):
        """测试 TriggerRegisterUnitEvent 返回事件handle。"""
        from jass_runner.natives.trigger_register_event_natives import TriggerRegisterUnitEvent
        from jass_runner.natives.event_handles import UnitEvent
        from jass_runner.trigger.event_types import EVENT_UNIT_DEATH

        mock_state_context.trigger_manager.register_event.return_value = "event_jkl012"

        native = TriggerRegisterUnitEvent()
        assert native.name == "TriggerRegisterUnitEvent"

        event = UnitEvent("unitevent_001", EVENT_UNIT_DEATH)
        result = native.execute(mock_state_context, "trigger_0", event, None)

        assert result == "event_jkl012"
        mock_state_context.trigger_manager.register_event.assert_called_once()
        call_args = mock_state_context.trigger_manager.register_event.call_args
        assert call_args[0][0] == "trigger_0"

    def test_register_unit_event_invalid_trigger(self, mock_state_context):
        """测试注册单位事件到不存在的触发器返回None。"""
        from jass_runner.natives.trigger_register_event_natives import TriggerRegisterUnitEvent
        from jass_runner.natives.event_handles import UnitEvent
        from jass_runner.trigger.event_types import EVENT_UNIT_DEATH

        mock_state_context.trigger_manager.register_event.return_value = None

        native = TriggerRegisterUnitEvent()
        event = UnitEvent("unitevent_001", EVENT_UNIT_DEATH)
        result = native.execute(mock_state_context, "trigger_invalid", event, None)

        assert result is None


class TestTriggerRegisterPlayerEvent:
    """测试 TriggerRegisterPlayerEvent 原生函数。"""

    def test_register_player_event_returns_event_handle(self, mock_state_context):
        """测试 TriggerRegisterPlayerEvent 返回事件handle。"""
        from jass_runner.natives.trigger_register_event_natives import TriggerRegisterPlayerEvent
        from jass_runner.natives.event_handles import PlayerEvent
        from jass_runner.trigger.event_types import EVENT_PLAYER_DEFEAT

        mock_state_context.trigger_manager.register_event.return_value = "event_mno345"

        native = TriggerRegisterPlayerEvent()
        assert native.name == "TriggerRegisterPlayerEvent"

        event = PlayerEvent("playerevent_001", EVENT_PLAYER_DEFEAT)
        result = native.execute(mock_state_context, "trigger_0", 0, event)

        assert result == "event_mno345"
        mock_state_context.trigger_manager.register_event.assert_called_once()
        call_args = mock_state_context.trigger_manager.register_event.call_args
        assert call_args[0][0] == "trigger_0"
        assert call_args[0][2]["player_id"] == 0

    def test_register_player_event_invalid_trigger(self, mock_state_context):
        """测试注册玩家事件到不存在的触发器返回None。"""
        from jass_runner.natives.trigger_register_event_natives import TriggerRegisterPlayerEvent
        from jass_runner.natives.event_handles import PlayerEvent
        from jass_runner.trigger.event_types import EVENT_PLAYER_DEFEAT

        mock_state_context.trigger_manager.register_event.return_value = None

        native = TriggerRegisterPlayerEvent()
        event = PlayerEvent("playerevent_001", EVENT_PLAYER_DEFEAT)
        result = native.execute(mock_state_context, "trigger_invalid", 0, event)

        assert result is None


class TestTriggerRegisterGameEvent:
    """测试 TriggerRegisterGameEvent 原生函数。"""

    def test_register_game_event_returns_event_handle(self, mock_state_context):
        """测试 TriggerRegisterGameEvent 返回事件handle。"""
        from jass_runner.natives.trigger_register_event_natives import TriggerRegisterGameEvent
        from jass_runner.natives.event_handles import GameEvent
        from jass_runner.trigger.event_types import EVENT_GAME_TIMER_EXPIRED

        mock_state_context.trigger_manager.register_event.return_value = "event_pqr678"

        native = TriggerRegisterGameEvent()
        assert native.name == "TriggerRegisterGameEvent"

        event = GameEvent("gameevent_001", EVENT_GAME_TIMER_EXPIRED)
        result = native.execute(mock_state_context, "trigger_0", event)

        assert result == "event_pqr678"
        mock_state_context.trigger_manager.register_event.assert_called_once()
        call_args = mock_state_context.trigger_manager.register_event.call_args
        assert call_args[0][0] == "trigger_0"

    def test_register_game_event_invalid_trigger(self, mock_state_context):
        """测试注册游戏事件到不存在的触发器返回None。"""
        from jass_runner.natives.trigger_register_event_natives import TriggerRegisterGameEvent
        from jass_runner.natives.event_handles import GameEvent
        from jass_runner.trigger.event_types import EVENT_GAME_TIMER_EXPIRED

        mock_state_context.trigger_manager.register_event.return_value = None

        native = TriggerRegisterGameEvent()
        event = GameEvent("gameevent_001", EVENT_GAME_TIMER_EXPIRED)
        result = native.execute(mock_state_context, "trigger_invalid", event)

        assert result is None

    def test_register_game_event_without_trigger_manager(self, mock_state_context):
        """测试没有trigger_manager时注册游戏事件返回None。"""
        from jass_runner.natives.trigger_register_event_natives import TriggerRegisterGameEvent
        from jass_runner.natives.event_handles import GameEvent
        from jass_runner.trigger.event_types import EVENT_GAME_TIMER_EXPIRED

        delattr(mock_state_context, 'trigger_manager')

        native = TriggerRegisterGameEvent()
        event = GameEvent("gameevent_001", EVENT_GAME_TIMER_EXPIRED)
        result = native.execute(mock_state_context, "trigger_0", event)

        assert result is None


class TestTriggerRegisterPlayerChatEvent:
    """测试 TriggerRegisterPlayerChatEvent 原生函数。"""

    def test_register_player_chat_event_returns_event_handle(self, mock_state_context):
        """测试 TriggerRegisterPlayerChatEvent 返回事件handle。"""
        from jass_runner.natives.trigger_register_event_natives import TriggerRegisterPlayerChatEvent

        mock_state_context.trigger_manager.register_event.return_value = "event_chat001"

        native = TriggerRegisterPlayerChatEvent()
        assert native.name == "TriggerRegisterPlayerChatEvent"

        result = native.execute(mock_state_context, "trigger_0", 0, "hello", False)

        assert result == "event_chat001"
        mock_state_context.trigger_manager.register_event.assert_called_once()
        call_args = mock_state_context.trigger_manager.register_event.call_args
        assert call_args[0][0] == "trigger_0"
        assert call_args[0][2]["player_id"] == 0
        assert call_args[0][2]["chat_message"] == "hello"
        assert call_args[0][2]["exact_match_only"] == False

    def test_register_player_chat_event_exact_match(self, mock_state_context):
        """测试 TriggerRegisterPlayerChatEvent 精确匹配模式。"""
        from jass_runner.natives.trigger_register_event_natives import TriggerRegisterPlayerChatEvent

        mock_state_context.trigger_manager.register_event.return_value = "event_chat002"

        native = TriggerRegisterPlayerChatEvent()
        result = native.execute(mock_state_context, "trigger_0", 1, "exact", True)

        assert result == "event_chat002"
        call_args = mock_state_context.trigger_manager.register_event.call_args
        assert call_args[0][2]["player_id"] == 1
        assert call_args[0][2]["chat_message"] == "exact"
        assert call_args[0][2]["exact_match_only"] == True

    def test_register_player_chat_event_invalid_trigger(self, mock_state_context):
        """测试注册玩家聊天事件到不存在的触发器返回None。"""
        from jass_runner.natives.trigger_register_event_natives import TriggerRegisterPlayerChatEvent

        mock_state_context.trigger_manager.register_event.return_value = None

        native = TriggerRegisterPlayerChatEvent()
        result = native.execute(mock_state_context, "trigger_invalid", 0, "hello", False)

        assert result is None

    def test_register_player_chat_event_without_trigger_manager(self, mock_state_context):
        """测试没有trigger_manager时注册玩家聊天事件返回None。"""
        from jass_runner.natives.trigger_register_event_natives import TriggerRegisterPlayerChatEvent

        delattr(mock_state_context, 'trigger_manager')

        native = TriggerRegisterPlayerChatEvent()
        result = native.execute(mock_state_context, "trigger_0", 0, "hello", False)

        assert result is None
