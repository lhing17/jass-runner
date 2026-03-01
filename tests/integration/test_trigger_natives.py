"""触发器Native函数集成测试。

此模块包含触发器相关Native函数的端到端集成测试，
验证Native函数与StateContext、TriggerManager的完整集成。
"""

import pytest
import logging
from io import StringIO

from jass_runner.natives.state import StateContext
from jass_runner.natives.factory import NativeFactory
from jass_runner.trigger.event_types import EVENT_UNIT_DEATH


class TestTriggerNativesIntegration:
    """触发器Native函数集成测试类。"""

    @pytest.fixture
    def state_context(self):
        """创建StateContext fixture。"""
        return StateContext()

    @pytest.fixture
    def native_factory(self):
        """创建NativeFactory fixture。"""
        return NativeFactory()

    @pytest.fixture
    def registry(self, native_factory):
        """创建包含默认Native函数的注册表。"""
        return native_factory.create_default_registry()

    def test_create_trigger_native_integration(self, state_context, registry):
        """测试CreateTrigger native函数。

        验证流程：
        1. 使用NativeFactory创建registry
        2. 执行CreateTrigger native函数
        3. 验证触发器ID格式
        4. 验证可以通过trigger_manager获取触发器
        """
        # 准备
        create_trigger_native = registry.get("CreateTrigger")
        assert create_trigger_native is not None, "CreateTrigger应该存在于注册表"

        # 执行
        trigger_id = create_trigger_native.execute(state_context)

        # 验证
        assert trigger_id is not None, "CreateTrigger应该返回有效的触发器ID"
        assert trigger_id.startswith("trigger_"), "触发器ID应该以'trigger_'开头"

        # 验证可以通过trigger_manager获取触发器
        trigger = state_context.trigger_manager.get_trigger(trigger_id)
        assert trigger is not None, "应该可以通过trigger_manager获取触发器"
        assert trigger.trigger_id == trigger_id, "触发器ID应该匹配"

    def test_enable_disable_trigger_native_integration(self, state_context, registry):
        """测试启用/禁用触发器函数。

        验证流程：
        1. 创建触发器
        2. 使用IsTriggerEnabled检查状态
        3. 使用DisableTrigger禁用
        4. 使用EnableTrigger启用
        """
        # 准备
        create_trigger = registry.get("CreateTrigger")
        is_trigger_enabled = registry.get("IsTriggerEnabled")
        disable_trigger = registry.get("DisableTrigger")
        enable_trigger = registry.get("EnableTrigger")

        # 创建触发器
        trigger_id = create_trigger.execute(state_context)
        assert trigger_id is not None

        # 验证：默认启用状态
        enabled = is_trigger_enabled.execute(state_context, trigger_id)
        assert enabled is True, "新创建的触发器应该默认启用"

        # 执行：禁用触发器
        result = disable_trigger.execute(state_context, trigger_id)

        # 验证：已禁用
        enabled = is_trigger_enabled.execute(state_context, trigger_id)
        assert enabled is False, "禁用后触发器应该为禁用状态"

        # 执行：启用触发器
        result = enable_trigger.execute(state_context, trigger_id)

        # 验证：已启用
        enabled = is_trigger_enabled.execute(state_context, trigger_id)
        assert enabled is True, "启用后触发器应该为启用状态"

    def test_trigger_add_action_native_integration(self, state_context, registry):
        """测试为触发器添加动作。

        验证流程：
        1. 创建触发器
        2. 使用TriggerAddAction添加动作
        3. 验证动作已添加
        """
        # 准备
        create_trigger = registry.get("CreateTrigger")
        add_action = registry.get("TriggerAddAction")

        trigger_id = create_trigger.execute(state_context)
        trigger = state_context.trigger_manager.get_trigger(trigger_id)

        # 标记动作执行
        action_executed = []

        def action_func(state_context):
            action_executed.append(True)

        # 执行：添加动作
        action_handle = add_action.execute(state_context, trigger_id, action_func)

        # 验证
        assert action_handle is not None, "添加动作应该返回有效的handle"
        assert action_handle.startswith("action_"), "动作handle应该以'action_'开头"

        # 手动执行触发器动作以验证
        trigger.execute_actions(state_context)
        assert len(action_executed) == 1, "动作应该被执行一次"

    def test_trigger_add_condition_native_integration(self, state_context, registry):
        """测试为触发器添加条件。

        验证流程：
        1. 创建触发器
        2. 使用TriggerAddCondition添加条件
        3. 直接通过Trigger评估条件
        """
        # 准备
        create_trigger = registry.get("CreateTrigger")
        add_condition = registry.get("TriggerAddCondition")

        trigger_id = create_trigger.execute(state_context)
        trigger = state_context.trigger_manager.get_trigger(trigger_id)

        # 添加返回True的条件
        def condition_true(state_context):
            return True

        # 执行：添加条件
        condition_handle = add_condition.execute(state_context, trigger_id, condition_true)

        # 验证
        assert condition_handle is not None, "添加条件应该返回有效的handle"
        assert condition_handle.startswith("condition"), "条件handle应该以'condition'开头"

        # 通过Trigger直接评估条件
        result = trigger.evaluate_conditions(state_context)
        assert result is True, "条件应该评估为True"

        # 测试添加返回False的条件
        def condition_false(state_context):
            return False

        # 清空之前的条件并添加新的
        trigger.clear_conditions()
        add_condition.execute(state_context, trigger_id, condition_false)

        # 评估条件
        result = trigger.evaluate_conditions(state_context)
        assert result is False, "条件应该评估为False"

    def test_trigger_register_unit_event_native_integration(self, state_context, registry):
        """测试注册单位事件。

        验证流程：
        1. 创建触发器
        2. 使用TriggerRegisterUnitEvent注册单位死亡事件
        3. 添加动作
        4. 杀死单位
        5. 验证动作执行
        """
        # 准备
        create_trigger = registry.get("CreateTrigger")
        register_unit_event = registry.get("TriggerRegisterUnitEvent")
        add_action = registry.get("TriggerAddAction")

        # 创建单位
        unit = state_context.handle_manager.create_unit("hfoo", 0, 100.0, 200.0, 0.0)

        # 创建触发器
        trigger_id = create_trigger.execute(state_context)
        trigger = state_context.trigger_manager.get_trigger(trigger_id)

        # 标记动作执行
        action_executed = []

        def action_func(state_context):
            action_executed.append(True)

        # 注册单位死亡事件
        add_action.execute(state_context, trigger_id, action_func)
        event_handle = register_unit_event.execute(
            state_context, trigger_id, EVENT_UNIT_DEATH
        )

        assert event_handle is not None, "注册事件应该返回有效的handle"

        # 执行：杀死单位
        state_context.handle_manager.kill_unit(unit.id)

        # 验证：动作被执行
        assert len(action_executed) == 1, "单位死亡时动作应该被执行一次"

    def test_destroy_trigger_native_integration(self, state_context, registry):
        """测试销毁触发器。

        验证流程：
        1. 创建触发器
        2. 验证存在
        3. 使用DestroyTrigger销毁
        4. 验证已销毁
        """
        # 准备
        create_trigger = registry.get("CreateTrigger")
        destroy_trigger = registry.get("DestroyTrigger")

        # 创建触发器
        trigger_id = create_trigger.execute(state_context)

        # 验证：触发器存在
        trigger = state_context.trigger_manager.get_trigger(trigger_id)
        assert trigger is not None, "创建的触发器应该存在"

        # 执行：销毁触发器
        destroy_trigger.execute(state_context, trigger_id)

        # 验证：触发器已销毁
        trigger = state_context.trigger_manager.get_trigger(trigger_id)
        assert trigger is None, "销毁后触发器应该不存在"
