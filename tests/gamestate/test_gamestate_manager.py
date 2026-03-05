"""GameStateManager测试模块。

此模块包含GameStateManager类的单元测试，
验证游戏状态管理功能，包括日夜循环和状态监听器。
"""

import pytest


class TestGameStateManager:
    """测试GameStateManager类的功能。"""

    def test_initial_time_is_zero(self):
        """测试初始时间为0帧。"""
        from jass_runner.gamestate.manager import GameStateManager

        manager = GameStateManager()

        assert manager.current_frame == 0

    def test_update_advances_time(self):
        """测试update方法推进时间。"""
        from jass_runner.gamestate.manager import GameStateManager

        manager = GameStateManager()
        manager.update(100)

        assert manager.current_frame == 100

    def test_time_of_day_calculation(self):
        """测试时间计算（日夜循环）。"""
        from jass_runner.gamestate.manager import GameStateManager
        from jass_runner.types.gamestate import FGameState

        manager = GameStateManager()
        # 9000帧 = 24小时，4500帧 = 12:00（中午）
        manager.update(4500)

        time_of_day = manager.get_float_state(FGameState.TIME_OF_DAY)
        assert time_of_day == 12.0

    def test_time_of_day_cycles(self):
        """测试时间循环（超过24小时后归零）。"""
        from jass_runner.gamestate.manager import GameStateManager
        from jass_runner.types.gamestate import FGameState

        manager = GameStateManager()
        # 推进超过一个周期（9000帧 = 24小时）
        manager.update(13500)  # 1.5个周期 = 36小时

        time_of_day = manager.get_float_state(FGameState.TIME_OF_DAY)
        # 36 % 24 = 12小时
        assert time_of_day == 12.0

    def test_register_state_listener(self):
        """测试注册状态监听器。"""
        from jass_runner.gamestate.manager import GameStateManager
        from jass_runner.types.gamestate import FGameState
        from jass_runner.types.limitop import LimitOp

        manager = GameStateManager()
        handle = manager.register_state_listener(
            FGameState.TIME_OF_DAY,
            LimitOp.GREATER_THAN_OR_EQUAL,
            6.0
        )

        assert handle is not None
        assert isinstance(handle, str)

    def test_state_listener_triggers_event(self):
        """测试状态监听器在时间满足条件时触发事件。"""
        from jass_runner.gamestate.manager import GameStateManager
        from jass_runner.types.gamestate import FGameState
        from jass_runner.types.limitop import LimitOp

        triggered_events = []

        # 模拟TriggerManager类
        class MockTriggerManager:
            def fire_event(self, event_type, event_data):
                triggered_events.append((event_type, event_data))

        manager = GameStateManager(trigger_manager=MockTriggerManager())

        # 注册监听器：当时间 >= 6:00时触发
        manager.register_state_listener(
            FGameState.TIME_OF_DAY,
            LimitOp.GREATER_THAN_OR_EQUAL,
            6.0
        )

        # 推进时间到6:00（2250帧）
        manager.update(2250)

        # 验证事件被触发
        assert len(triggered_events) == 1
        assert triggered_events[0][0] == "game_state_limit"
        assert triggered_events[0][1]["state_id"] == FGameState.TIME_OF_DAY

    def test_state_listener_triggers_only_once(self):
        """测试状态监听器只触发一次。"""
        from jass_runner.gamestate.manager import GameStateManager
        from jass_runner.types.gamestate import FGameState
        from jass_runner.types.limitop import LimitOp

        triggered_events = []

        # 模拟TriggerManager类
        class MockTriggerManager:
            def fire_event(self, event_type, event_data):
                triggered_events.append((event_type, event_data))

        manager = GameStateManager(trigger_manager=MockTriggerManager())

        # 注册监听器：当时间 >= 6:00时触发
        manager.register_state_listener(
            FGameState.TIME_OF_DAY,
            LimitOp.GREATER_THAN_OR_EQUAL,
            6.0
        )

        # 推进时间到6:00（2250帧）
        manager.update(2250)

        # 验证事件被触发一次
        assert len(triggered_events) == 1

        # 继续推进时间
        manager.update(1000)

        # 验证事件没有再次触发
        assert len(triggered_events) == 1
