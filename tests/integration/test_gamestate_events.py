"""游戏状态事件集成测试。

此模块包含游戏状态事件的端到端集成测试，
验证从GameStateManager到Trigger的完整事件流程。
"""

import pytest
from jass_runner.natives.state import StateContext
from jass_runner.types.gamestate import FGameState
from jass_runner.types.limitop import LimitOp
from jass_runner.trigger.event_types import EVENT_GAME_STATE_LIMIT


class TestGameStateEventsIntegration:
    """游戏状态事件集成测试类。"""

    def test_time_of_day_event_triggers(self):
        """测试 TIME_OF_DAY 事件触发。

        验证流程：
        1. 创建StateContext
        2. 创建触发器
        3. 注册游戏状态事件（TIME_OF_DAY >= 12.0）
        4. 推进时间到中午（12小时）
        5. 验证动作执行
        """
        # 准备
        context = StateContext()
        trigger_manager = context.trigger_manager
        game_state_manager = context.game_state_manager

        # 创建触发器
        trigger_id = trigger_manager.create_trigger()
        trigger = trigger_manager.get_trigger(trigger_id)

        # 标记动作是否被执行
        action_executed = []

        # 添加动作
        def action_func(state_context):
            action_executed.append(True)

        trigger.add_action(action_func)

        # 注册游戏状态事件：当时间到达12.0（中午）时触发
        # 使用GREATER_THAN_OR_EQUAL操作符
        event_handle = game_state_manager.register_state_listener(
            trigger_id,
            FGameState.TIME_OF_DAY,
            LimitOp.GREATER_THAN_OR_EQUAL,
            12.0
        )

        # 验证监听器已注册
        assert event_handle is not None
        assert event_handle.startswith("state_listener_")

        # 当前帧为0，时间是0.0（午夜）
        assert game_state_manager.get_float_state(FGameState.TIME_OF_DAY) == 0.0

        # 推进时间到中午：12小时 = 4500帧（9000帧 = 24小时）
        # 4500帧 = 12小时
        game_state_manager.update(4500)

        # 验证动作被执行
        assert len(action_executed) == 1, "动作应该被执行一次"

        # 验证当前时间
        current_time = game_state_manager.get_float_state(FGameState.TIME_OF_DAY)
        assert 11.9 <= current_time <= 12.1, f"当前时间应该约为12.0，实际是{current_time}"

    def test_dawn_event_with_blizzard_constant(self):
        """测试黎明事件（6.0）。

        验证使用EQUAL操作符检测黎明（6:00）的事件触发。
        """
        # 准备
        context = StateContext()
        trigger_manager = context.trigger_manager
        game_state_manager = context.game_state_manager

        # 创建触发器
        trigger_id = trigger_manager.create_trigger()
        trigger = trigger_manager.get_trigger(trigger_id)

        # 记录事件数据
        captured_event_data = []

        # 添加动作，捕获事件数据
        def action_func(state_context):
            captured_event_data.append(state_context.get("event_data", {}))

        trigger.add_action(action_func)

        # 注册游戏状态事件：当时间等于6.0（黎明）时触发
        event_handle = game_state_manager.register_state_listener(
            trigger_id,
            FGameState.TIME_OF_DAY,
            LimitOp.EQUAL,
            6.0
        )

        # 验证监听器已注册
        assert event_handle is not None

        # 推进时间到黎明：6小时 = 2250帧
        game_state_manager.update(2250)

        # 验证动作被执行
        assert len(captured_event_data) == 1, "动作应该被执行一次"

        # 验证事件数据
        event_data = captured_event_data[0]
        assert event_data.get("trigger_id") == trigger_id
        assert event_data.get("state_id") == FGameState.TIME_OF_DAY
        # 时间应该接近6.0（使用epsilon比较）
        assert 5.9 <= event_data.get("value", 0) <= 6.1

    def test_multiple_listeners_same_time(self):
        """测试多监听器同时触发。

        验证当多个监听器注册到同一时间时，都会触发。
        """
        # 准备
        context = StateContext()
        trigger_manager = context.trigger_manager
        game_state_manager = context.game_state_manager

        # 创建两个触发器
        trigger_id_1 = trigger_manager.create_trigger()
        trigger_id_2 = trigger_manager.create_trigger()
        trigger_1 = trigger_manager.get_trigger(trigger_id_1)
        trigger_2 = trigger_manager.get_trigger(trigger_id_2)

        # 记录动作执行
        action_1_executed = []
        action_2_executed = []

        # 为第一个触发器添加动作
        def action_func_1(state_context):
            action_1_executed.append(True)

        trigger_1.add_action(action_func_1)

        # 为第二个触发器添加动作
        def action_func_2(state_context):
            action_2_executed.append(True)

        trigger_2.add_action(action_func_2)

        # 注册两个监听器到同一时间（中午12:00）
        event_handle_1 = game_state_manager.register_state_listener(
            trigger_id_1,
            FGameState.TIME_OF_DAY,
            LimitOp.GREATER_THAN_OR_EQUAL,
            12.0
        )

        event_handle_2 = game_state_manager.register_state_listener(
            trigger_id_2,
            FGameState.TIME_OF_DAY,
            LimitOp.GREATER_THAN_OR_EQUAL,
            12.0
        )

        # 验证两个监听器都已注册
        assert event_handle_1 is not None
        assert event_handle_2 is not None
        assert event_handle_1 != event_handle_2

        # 推进时间到中午
        game_state_manager.update(4500)

        # 验证两个动作都被执行
        assert len(action_1_executed) == 1, "触发器1的动作应该被执行"
        assert len(action_2_executed) == 1, "触发器2的动作应该被执行"

    def test_listener_triggered_only_once(self):
        """测试监听器只触发一次。

        验证当条件满足后，监听器不会再次触发。
        """
        # 准备
        context = StateContext()
        trigger_manager = context.trigger_manager
        game_state_manager = context.game_state_manager

        # 创建触发器
        trigger_id = trigger_manager.create_trigger()
        trigger = trigger_manager.get_trigger(trigger_id)

        # 记录动作执行次数
        action_count = []

        # 添加动作
        def action_func(state_context):
            action_count.append(len(action_count) + 1)

        trigger.add_action(action_func)

        # 注册游戏状态事件
        game_state_manager.register_state_listener(
            trigger_id,
            FGameState.TIME_OF_DAY,
            LimitOp.GREATER_THAN_OR_EQUAL,
            6.0
        )

        # 推进时间到黎明（6小时）
        game_state_manager.update(2250)

        # 验证动作被执行一次
        assert len(action_count) == 1

        # 继续推进时间（再过6小时到中午）
        game_state_manager.update(2250)

        # 验证动作仍然只执行一次（不会重复触发）
        assert len(action_count) == 1, "监听器不应该重复触发"

    def test_different_limit_ops(self):
        """测试不同的比较操作符。

        验证LESS_THAN、GREATER_THAN等操作符的正确性。
        """
        # 准备
        context = StateContext()
        trigger_manager = context.trigger_manager
        game_state_manager = context.game_state_manager

        # 创建触发器 - 使用LESS_THAN检测午夜前
        trigger_id = trigger_manager.create_trigger()
        trigger = trigger_manager.get_trigger(trigger_id)

        action_executed = []

        def action_func(state_context):
            action_executed.append(True)

        trigger.add_action(action_func)

        # 注册事件：当时间小于1.0（凌晨1点前）时触发
        game_state_manager.register_state_listener(
            trigger_id,
            FGameState.TIME_OF_DAY,
            LimitOp.LESS_THAN,
            1.0
        )

        # 当前时间是0.0，应该立即触发
        game_state_manager.update(0)

        # 验证动作被执行（因为0.0 < 1.0）
        assert len(action_executed) == 1, "LESS_THAN条件应该立即满足"

    def test_game_state_manager_with_trigger_manager_integration(self):
        """测试GameStateManager与TriggerManager的集成。

        验证通过StateContext的完整集成流程。
        """
        # 准备
        context = StateContext()
        trigger_manager = context.trigger_manager
        game_state_manager = context.game_state_manager

        # 验证两个管理器已正确连接
        assert game_state_manager._trigger_manager is trigger_manager

        # 创建触发器并添加动作
        trigger_id = trigger_manager.create_trigger()
        trigger = trigger_manager.get_trigger(trigger_id)

        captured_values = []

        def action_func(state_context):
            event_data = state_context.get("event_data", {})
            captured_values.append(event_data.get("value"))

        trigger.add_action(action_func)

        # 注册状态监听器
        game_state_manager.register_state_listener(
            trigger_id,
            FGameState.TIME_OF_DAY,
            LimitOp.GREATER_THAN_OR_EQUAL,
            18.0  # 傍晚6点
        )

        # 推进时间到傍晚6点：18小时 = 6750帧
        game_state_manager.update(6750)

        # 验证动作被执行并捕获了正确的时间值
        assert len(captured_values) == 1
        assert 17.9 <= captured_values[0] <= 18.1
