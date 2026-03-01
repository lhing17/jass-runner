"""Trigger类测试模块。

测试JASS触发器系统中Trigger类的功能，
包括事件、条件和动作的增删改查管理。
"""

import pytest
from unittest.mock import Mock


class TestTriggerCreation:
    """测试Trigger类的创建和基本属性。"""

    def test_trigger_creation_with_id(self):
        """测试Trigger创建时设置trigger_id属性。"""
        from jass_runner.trigger.trigger import Trigger

        trigger = Trigger("test_trigger_001")

        assert trigger.trigger_id == "test_trigger_001"

    def test_trigger_default_enabled(self):
        """测试Trigger默认启用状态为True。"""
        from jass_runner.trigger.trigger import Trigger

        trigger = Trigger("test_trigger_001")

        assert trigger.enabled is True

    def test_trigger_disabled(self):
        """测试Trigger可以设置为禁用状态。"""
        from jass_runner.trigger.trigger import Trigger

        trigger = Trigger("test_trigger_001")
        trigger.enabled = False

        assert trigger.enabled is False


class TestTriggerActions:
    """测试Trigger类的动作管理功能。"""

    def test_add_action_returns_handle(self):
        """测试添加动作返回正确格式的handle。"""
        from jass_runner.trigger.trigger import Trigger

        trigger = Trigger("test_trigger_001")
        action_func = Mock()

        handle = trigger.add_action(action_func)

        assert handle.startswith("action_")
        assert len(handle) == 15  # "action_" + 8位uuid

    def test_remove_action_success(self):
        """测试移除指定动作成功。"""
        from jass_runner.trigger.trigger import Trigger

        trigger = Trigger("test_trigger_001")
        action_func = Mock()

        handle = trigger.add_action(action_func)
        result = trigger.remove_action(handle)

        assert result is True
        assert len(trigger.actions) == 0

    def test_remove_action_not_found(self):
        """测试移除不存在的动作返回False。"""
        from jass_runner.trigger.trigger import Trigger

        trigger = Trigger("test_trigger_001")

        result = trigger.remove_action("action_nonexistent")

        assert result is False

    def test_clear_actions(self):
        """测试清空所有动作。"""
        from jass_runner.trigger.trigger import Trigger

        trigger = Trigger("test_trigger_001")
        action_func1 = Mock()
        action_func2 = Mock()

        trigger.add_action(action_func1)
        trigger.add_action(action_func2)
        trigger.clear_actions()

        assert len(trigger.actions) == 0

    def test_multiple_actions_tracking(self):
        """测试可以添加多个动作并跟踪。"""
        from jass_runner.trigger.trigger import Trigger

        trigger = Trigger("test_trigger_001")
        action_func1 = Mock()
        action_func2 = Mock()

        handle1 = trigger.add_action(action_func1)
        handle2 = trigger.add_action(action_func2)

        assert len(trigger.actions) == 2
        assert handle1 != handle2


class TestTriggerConditions:
    """测试Trigger类的条件管理功能。"""

    def test_add_condition_returns_handle(self):
        """测试添加条件返回正确格式的handle。"""
        from jass_runner.trigger.trigger import Trigger

        trigger = Trigger("test_trigger_001")
        condition_func = Mock(return_value=True)

        handle = trigger.add_condition(condition_func)

        assert handle.startswith("condition_")
        assert len(handle) == 18  # "condition_" + 8位uuid

    def test_remove_condition_success(self):
        """测试移除指定条件成功。"""
        from jass_runner.trigger.trigger import Trigger

        trigger = Trigger("test_trigger_001")
        condition_func = Mock(return_value=True)

        handle = trigger.add_condition(condition_func)
        result = trigger.remove_condition(handle)

        assert result is True
        assert len(trigger.conditions) == 0

    def test_remove_condition_not_found(self):
        """测试移除不存在的条件返回False。"""
        from jass_runner.trigger.trigger import Trigger

        trigger = Trigger("test_trigger_001")

        result = trigger.remove_condition("condition_nonexistent")

        assert result is False

    def test_clear_conditions(self):
        """测试清空所有条件。"""
        from jass_runner.trigger.trigger import Trigger

        trigger = Trigger("test_trigger_001")
        condition_func1 = Mock(return_value=True)
        condition_func2 = Mock(return_value=True)

        trigger.add_condition(condition_func1)
        trigger.add_condition(condition_func2)
        trigger.clear_conditions()

        assert len(trigger.conditions) == 0


class TestTriggerEvents:
    """测试Trigger类的事件注册功能。"""

    def test_register_event_returns_handle(self):
        """测试注册事件返回正确格式的handle。"""
        from jass_runner.trigger.trigger import Trigger

        trigger = Trigger("test_trigger_001")

        handle = trigger.register_event("unit_death", None)

        assert handle.startswith("event_")
        assert len(handle) == 14  # "event_" + 8位uuid

    def test_register_event_with_filter(self):
        """测试注册事件附带过滤器数据。"""
        from jass_runner.trigger.trigger import Trigger

        trigger = Trigger("test_trigger_001")
        filter_data = {"player_id": 1, "unit_type": "footman"}

        handle = trigger.register_event("player_unit_death", filter_data)

        assert handle.startswith("event_")
        assert len(trigger.events) == 1

    def test_clear_events(self):
        """测试清空所有事件。"""
        from jass_runner.trigger.trigger import Trigger

        trigger = Trigger("test_trigger_001")

        trigger.register_event("unit_death", None)
        trigger.register_event("unit_damaged", {"damage_type": "magic"})
        trigger.clear_events()

        assert len(trigger.events) == 0


class TestTriggerEvaluation:
    """测试Trigger类的条件评估和动作执行功能。"""

    def test_evaluate_conditions_no_conditions(self):
        """测试无条件时evaluate_conditions返回True。"""
        from jass_runner.trigger.trigger import Trigger

        trigger = Trigger("test_trigger_001")
        state_context = {"event_data": {}}

        result = trigger.evaluate_conditions(state_context)

        assert result is True

    def test_evaluate_conditions_all_pass(self):
        """测试所有条件通过时返回True。"""
        from jass_runner.trigger.trigger import Trigger

        trigger = Trigger("test_trigger_001")
        condition1 = Mock(return_value=True)
        condition2 = Mock(return_value=True)

        trigger.add_condition(condition1)
        trigger.add_condition(condition2)

        state_context = {"event_data": {"unit_id": 123}}
        result = trigger.evaluate_conditions(state_context)

        assert result is True
        condition1.assert_called_once_with(state_context)
        condition2.assert_called_once_with(state_context)

    def test_evaluate_conditions_one_fails(self):
        """测试任一条件失败时返回False。"""
        from jass_runner.trigger.trigger import Trigger

        trigger = Trigger("test_trigger_001")
        condition1 = Mock(return_value=True)
        condition2 = Mock(return_value=False)
        condition3 = Mock(return_value=True)

        trigger.add_condition(condition1)
        trigger.add_condition(condition2)
        trigger.add_condition(condition3)

        state_context = {"event_data": {"unit_id": 123}}
        result = trigger.evaluate_conditions(state_context)

        assert result is False
        condition1.assert_called_once()
        condition2.assert_called_once()
        # 第三个条件不应该被调用，因为第二个失败了
        condition3.assert_not_called()

    def test_execute_actions_sequential(self):
        """测试动作按添加顺序执行。"""
        from jass_runner.trigger.trigger import Trigger

        trigger = Trigger("test_trigger_001")
        execution_order = []

        def action1(ctx):
            execution_order.append(1)

        def action2(ctx):
            execution_order.append(2)

        def action3(ctx):
            execution_order.append(3)

        trigger.add_action(action1)
        trigger.add_action(action2)
        trigger.add_action(action3)

        state_context = {"event_data": {}}
        trigger.execute_actions(state_context)

        assert execution_order == [1, 2, 3]

    def test_execute_actions_with_exception_continues(self):
        """测试动作异常时不中断执行。"""
        from jass_runner.trigger.trigger import Trigger

        trigger = Trigger("test_trigger_001")
        execution_order = []

        def action1(ctx):
            execution_order.append(1)

        def action2_raises(ctx):
            execution_order.append(2)
            raise ValueError("Test exception")

        def action3(ctx):
            execution_order.append(3)

        trigger.add_action(action1)
        trigger.add_action(action2_raises)
        trigger.add_action(action3)

        state_context = {"event_data": {}}
        # 不应该抛出异常
        trigger.execute_actions(state_context)

        assert execution_order == [1, 2, 3]  # 所有动作都应被执行

    def test_execute_actions_passes_context(self):
        """测试动作执行时传递状态上下文。"""
        from jass_runner.trigger.trigger import Trigger

        trigger = Trigger("test_trigger_001")
        received_contexts = []

        def action1(ctx):
            received_contexts.append(ctx)

        def action2(ctx):
            received_contexts.append(ctx)

        trigger.add_action(action1)
        trigger.add_action(action2)

        state_context = {"event_data": {"unit_id": 456}, "player_id": 1}
        trigger.execute_actions(state_context)

        assert len(received_contexts) == 2
        assert received_contexts[0]["event_data"]["unit_id"] == 456
        assert received_contexts[1]["player_id"] == 1
