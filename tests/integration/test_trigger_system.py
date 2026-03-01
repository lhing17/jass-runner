"""触发器系统集成测试。

此模块包含触发器系统的基础集成测试，
验证从StateContext到事件分发的完整触发器流程。
"""

import pytest
from jass_runner.natives.state import StateContext
from jass_runner.trigger.event_types import EVENT_UNIT_DEATH


class TestTriggerSystemIntegration:
    """触发器系统基础集成测试类。"""

    def test_complete_trigger_flow(self):
        """测试完整的触发器流程。

        验证流程：
        1. 创建StateContext
        2. 创建触发器
        3. 注册单位死亡事件
        4. 添加条件和动作
        5. 创建并杀死单位
        6. 验证动作执行
        """
        # 准备
        context = StateContext()
        trigger_manager = context.trigger_manager

        # 创建一个单位
        unit = context.handle_manager.create_unit("hfoo", 0, 0.0, 0.0, 0.0)

        # 创建触发器
        trigger_id = trigger_manager.create_trigger()
        trigger = trigger_manager.get_trigger(trigger_id)

        # 标记动作是否被执行
        action_executed = []
        condition_passed = []

        # 添加条件（返回True，确保动作执行）
        def condition_func(state_context):
            condition_passed.append(True)
            return True

        condition_handle = trigger.add_condition(condition_func)

        # 添加动作
        def action_func(state_context):
            action_executed.append(True)

        action_handle = trigger.add_action(action_func)

        # 注册单位死亡事件
        event_handle = trigger_manager.register_event(
            trigger_id, EVENT_UNIT_DEATH, None
        )

        # 执行：杀死单位
        context.handle_manager.kill_unit(unit.id)

        # 验证
        assert len(condition_passed) == 1, "条件应该被评估一次"
        assert len(action_executed) == 1, "动作应该被执行一次"

    def test_trigger_with_false_condition(self):
        """测试条件过滤。

        验证当条件返回False时，动作不会执行。
        """
        # 准备
        context = StateContext()
        trigger_manager = context.trigger_manager

        # 创建一个单位
        unit = context.handle_manager.create_unit("hfoo", 0, 0.0, 0.0, 0.0)

        # 创建触发器
        trigger_id = trigger_manager.create_trigger()
        trigger = trigger_manager.get_trigger(trigger_id)

        # 标记动作是否被执行
        action_executed = []

        # 添加条件（返回False，阻止动作执行）
        def condition_func(state_context):
            return False

        trigger.add_condition(condition_func)

        # 添加动作
        def action_func(state_context):
            action_executed.append(True)

        trigger.add_action(action_func)

        # 注册单位死亡事件
        trigger_manager.register_event(trigger_id, EVENT_UNIT_DEATH, None)

        # 执行：杀死单位
        context.handle_manager.kill_unit(unit.id)

        # 验证：动作未执行
        assert len(action_executed) == 0, "动作不应该被执行"

    def test_disabled_trigger_does_not_execute(self):
        """测试禁用触发器。

        验证禁用状态下的触发器不会执行动作。
        """
        # 准备
        context = StateContext()
        trigger_manager = context.trigger_manager

        # 创建一个单位
        unit = context.handle_manager.create_unit("hfoo", 0, 0.0, 0.0, 0.0)

        # 创建触发器
        trigger_id = trigger_manager.create_trigger()
        trigger = trigger_manager.get_trigger(trigger_id)

        # 标记动作是否被执行
        action_executed = []

        # 添加动作
        def action_func(state_context):
            action_executed.append(True)

        trigger.add_action(action_func)

        # 注册单位死亡事件
        trigger_manager.register_event(trigger_id, EVENT_UNIT_DEATH, None)

        # 禁用触发器
        trigger_manager.disable_trigger(trigger_id)

        # 验证触发器已禁用
        assert trigger_manager.is_trigger_enabled(trigger_id) is False

        # 执行：杀死单位
        context.handle_manager.kill_unit(unit.id)

        # 验证：动作未执行
        assert len(action_executed) == 0, "禁用的触发器不应该执行动作"

    def test_multiple_triggers_same_event(self):
        """测试多触发器同一事件。

        验证当同一事件触发时，多个触发器的动作都会执行。
        """
        # 准备
        context = StateContext()
        trigger_manager = context.trigger_manager

        # 创建一个单位
        unit = context.handle_manager.create_unit("hfoo", 0, 0.0, 0.0, 0.0)

        # 创建两个触发器
        trigger_id_1 = trigger_manager.create_trigger()
        trigger_id_2 = trigger_manager.create_trigger()
        trigger_1 = trigger_manager.get_trigger(trigger_id_1)
        trigger_2 = trigger_manager.get_trigger(trigger_id_2)

        # 标记动作执行
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

        # 为两个触发器注册同一事件
        trigger_manager.register_event(trigger_id_1, EVENT_UNIT_DEATH, None)
        trigger_manager.register_event(trigger_id_2, EVENT_UNIT_DEATH, None)

        # 执行：杀死单位
        context.handle_manager.kill_unit(unit.id)

        # 验证：两个动作都执行了
        assert len(action_1_executed) == 1, "触发器1的动作应该被执行"
        assert len(action_2_executed) == 1, "触发器2的动作应该被执行"

    def test_trigger_destroy_removes_event_handler(self):
        """测试销毁触发器。

        验证销毁触发器后，它不再响应事件。
        """
        # 准备
        context = StateContext()
        trigger_manager = context.trigger_manager

        # 创建一个单位
        unit = context.handle_manager.create_unit("hfoo", 0, 0.0, 0.0, 0.0)

        # 创建触发器
        trigger_id = trigger_manager.create_trigger()
        trigger = trigger_manager.get_trigger(trigger_id)

        # 标记动作是否被执行
        action_executed = []

        # 添加动作
        def action_func(state_context):
            action_executed.append(True)

        trigger.add_action(action_func)

        # 注册单位死亡事件
        trigger_manager.register_event(trigger_id, EVENT_UNIT_DEATH, None)

        # 销毁触发器
        trigger_manager.destroy_trigger(trigger_id)

        # 执行：杀死单位
        context.handle_manager.kill_unit(unit.id)

        # 验证：动作未执行
        assert len(action_executed) == 0, "已销毁的触发器不应该执行动作"
