"""触发器计时器事件集成测试。

此模块包含触发器系统与计时器系统的集成测试，
验证计时器到期事件能够正确触发触发器动作。
"""

import pytest
from jass_runner.natives.state import StateContext
from jass_runner.timer.system import TimerSystem
from jass_runner.trigger.event_types import EVENT_GAME_TIMER_EXPIRED


class TestTriggerTimerIntegration:
    """触发器计时器事件集成测试类。"""

    def test_timer_expire_triggers_event(self):
        """测试计时器到期触发事件。

        验证流程：
        1. 创建StateContext和TimerSystem
        2. 设置TimerSystem的trigger_manager
        3. 创建触发器并注册计时器过期事件
        4. 创建并启动计时器
        5. 更新计时器使其到期
        6. 验证动作执行
        """
        # 准备
        state_context = StateContext()
        timer_system = TimerSystem()
        timer_system.set_trigger_manager(state_context.trigger_manager)

        trigger_manager = state_context.trigger_manager

        # 创建触发器
        trigger_id = trigger_manager.create_trigger()
        trigger = trigger_manager.get_trigger(trigger_id)

        # 标记动作执行
        action_executed = []

        # 添加动作
        def action_func(state_context):
            action_executed.append(True)

        trigger.add_action(action_func)

        # 注册计时器过期事件
        trigger_manager.register_event(
            trigger_id, EVENT_GAME_TIMER_EXPIRED, None
        )

        # 创建并启动计时器
        timer_id = timer_system.create_timer()
        timer = timer_system.get_timer(timer_id)
        timer.start(1.0, False, lambda: None)  # 1秒后到期，非周期性

        # 执行：更新计时器使其到期
        timer_system.update(1.0)

        # 验证：动作被执行
        assert len(action_executed) == 1, "计时器到期应该触发动作"

    def test_multiple_timers_trigger_event(self):
        """测试多个计时器都触发事件。

        验证流程：
        1. 创建StateContext和TimerSystem
        2. 创建触发器
        3. 创建两个计时器
        4. 为触发器注册通用计时器事件
        5. 启动两个计时器
        6. 更新计时器使其到期
        7. 验证动作被执行两次（每个计时器一次）
        """
        # 准备
        state_context = StateContext()
        timer_system = TimerSystem()
        timer_system.set_trigger_manager(state_context.trigger_manager)

        trigger_manager = state_context.trigger_manager

        # 创建触发器
        trigger_id = trigger_manager.create_trigger()
        trigger = trigger_manager.get_trigger(trigger_id)

        # 标记动作执行次数
        action_count = []

        # 添加动作
        def action_func(state_context):
            action_count.append(1)

        trigger.add_action(action_func)

        # 注册通用计时器事件
        trigger_manager.register_event(
            trigger_id, EVENT_GAME_TIMER_EXPIRED, None
        )

        # 创建两个计时器
        timer_id_1 = timer_system.create_timer()
        timer_id_2 = timer_system.create_timer()

        # 启动两个计时器
        timer_1 = timer_system.get_timer(timer_id_1)
        timer_2 = timer_system.get_timer(timer_id_2)
        timer_1.start(1.0, False, lambda: None)
        timer_2.start(1.0, False, lambda: None)

        # 执行：更新计时器使其到期
        timer_system.update(1.0)

        # 验证：动作被执行了两次（每个计时器一次）
        assert len(action_count) == 2, "两个计时器到期应该触发两次动作"

    def test_periodic_timer_triggers_multiple_times(self):
        """测试周期性计时器多次触发。

        验证流程：
        1. 创建StateContext和TimerSystem
        2. 创建触发器并注册事件
        3. 创建周期性计时器
        4. 更新计时器多次
        5. 验证触发多次
        """
        # 准备
        state_context = StateContext()
        timer_system = TimerSystem()
        timer_system.set_trigger_manager(state_context.trigger_manager)

        trigger_manager = state_context.trigger_manager

        # 创建触发器
        trigger_id = trigger_manager.create_trigger()
        trigger = trigger_manager.get_trigger(trigger_id)

        # 标记动作执行次数
        action_count = []

        # 添加动作
        def action_func(state_context):
            action_count.append(1)

        trigger.add_action(action_func)

        # 注册计时器过期事件
        trigger_manager.register_event(
            trigger_id, EVENT_GAME_TIMER_EXPIRED, None
        )

        # 创建周期性计时器
        timer_id = timer_system.create_timer()
        timer = timer_system.get_timer(timer_id)
        timer.start(1.0, True, lambda: None)  # 1秒周期，周期性

        # 执行：更新计时器多次使其多次到期
        timer_system.update(1.0)  # 第一次到期
        timer_system.update(1.0)  # 第二次到期
        timer_system.update(1.0)  # 第三次到期

        # 验证：动作被执行了3次
        assert len(action_count) == 3, "周期性计时器应该触发多次"

    def test_multiple_triggers_with_same_timer_event(self):
        """测试多个触发器监听同一计时器事件。

        验证流程：
        1. 创建StateContext和TimerSystem
        2. 创建两个触发器
        3. 为两个触发器注册计时器事件
        4. 创建并启动计时器
        5. 更新计时器使其到期
        6. 验证两个触发器的动作都执行
        """
        # 准备
        state_context = StateContext()
        timer_system = TimerSystem()
        timer_system.set_trigger_manager(state_context.trigger_manager)

        trigger_manager = state_context.trigger_manager

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

        # 为两个触发器注册计时器事件
        trigger_manager.register_event(
            trigger_id_1, EVENT_GAME_TIMER_EXPIRED, None
        )
        trigger_manager.register_event(
            trigger_id_2, EVENT_GAME_TIMER_EXPIRED, None
        )

        # 创建并启动计时器
        timer_id = timer_system.create_timer()
        timer = timer_system.get_timer(timer_id)
        timer.start(1.0, False, lambda: None)

        # 执行：更新计时器使其到期
        timer_system.update(1.0)

        # 验证：两个触发器的动作都执行了
        assert len(action_1_executed) == 1, "触发器1的动作应该被执行"
        assert len(action_2_executed) == 1, "触发器2的动作应该被执行"

    def test_timer_event_with_condition(self):
        """测试计时器事件与条件结合。

        验证流程：
        1. 创建StateContext和TimerSystem
        2. 创建触发器并注册事件
        3. 添加条件（返回False）
        4. 创建并启动计时器
        5. 更新计时器使其到期
        6. 验证动作未执行
        """
        # 准备
        state_context = StateContext()
        timer_system = TimerSystem()
        timer_system.set_trigger_manager(state_context.trigger_manager)

        trigger_manager = state_context.trigger_manager

        # 创建触发器
        trigger_id = trigger_manager.create_trigger()
        trigger = trigger_manager.get_trigger(trigger_id)

        # 标记动作执行
        action_executed = []

        # 添加条件（返回False）
        def condition_func(state_context):
            return False

        trigger.add_condition(condition_func)

        # 添加动作
        def action_func(state_context):
            action_executed.append(True)

        trigger.add_action(action_func)

        # 注册计时器过期事件
        trigger_manager.register_event(
            trigger_id, EVENT_GAME_TIMER_EXPIRED, None
        )

        # 创建并启动计时器
        timer_id = timer_system.create_timer()
        timer = timer_system.get_timer(timer_id)
        timer.start(1.0, False, lambda: None)

        # 执行：更新计时器使其到期
        timer_system.update(1.0)

        # 验证：动作未执行（因为条件返回False）
        assert len(action_executed) == 0, "条件失败时不应该执行动作"
