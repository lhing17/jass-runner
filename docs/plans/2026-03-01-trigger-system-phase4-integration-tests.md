# JASS触发器系统实施计划 - 阶段4：集成测试和示例

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 创建完整的集成测试和示例JASS脚本，验证触发器系统的端到端功能。

**Architecture:** 编写集成测试覆盖完整触发器流程（创建→注册事件→添加条件/动作→触发事件→验证执行），并提供可运行的JASS示例脚本。

**Tech Stack:** Python 3.8+, pytest, 完整JASS Runner工具链

---

### Task 1: 创建基础集成测试

**Files:**
- Create: `tests/integration/test_trigger_system.py`

**Step 1: Write the failing test**

```python
"""触发器系统集成测试。"""

import pytest
from jass_runner.natives.state import StateContext
from jass_runner.trigger.event_types import (
    EVENT_UNIT_DEATH,
    EVENT_PLAYER_DEFEAT,
    EVENT_GAME_TIMER_EXPIRED,
)


class TestTriggerSystemIntegration:
    """触发器系统集成测试类。"""

    def test_complete_trigger_flow(self):
        """测试完整的触发器流程。"""
        # 创建状态上下文
        context = StateContext()

        # 创建触发器
        trigger_id = context.trigger_manager.create_trigger()

        # 记录执行
        executions = []

        def test_action():
            executions.append("action_executed")

        def true_condition():
            executions.append("condition_checked")
            return True

        # 注册事件、条件和动作
        context.trigger_manager.register_event(trigger_id, EVENT_UNIT_DEATH, None)
        trigger = context.trigger_manager.get_trigger(trigger_id)
        trigger.add_condition(true_condition)
        trigger.add_action(test_action)

        # 创建并杀死单位
        unit_id = context.handle_manager.create_unit("hfoo", 0, 100.0, 200.0, 270.0)
        context.handle_manager.kill_unit(unit_id)

        # 验证执行顺序
        assert "condition_checked" in executions
        assert "action_executed" in executions

    def test_trigger_with_false_condition(self):
        """测试条件为False时动作不执行。"""
        context = StateContext()

        trigger_id = context.trigger_manager.create_trigger()

        action_executed = []

        def test_action():
            action_executed.append(True)

        def false_condition():
            return False

        # 注册事件、条件和动作
        context.trigger_manager.register_event(trigger_id, EVENT_UNIT_DEATH, None)
        trigger = context.trigger_manager.get_trigger(trigger_id)
        trigger.add_condition(false_condition)
        trigger.add_action(test_action)

        # 创建并杀死单位
        unit_id = context.handle_manager.create_unit("hfoo", 0, 100.0, 200.0, 270.0)
        context.handle_manager.kill_unit(unit_id)

        # 验证动作未执行
        assert len(action_executed) == 0

    def test_disabled_trigger_does_not_execute(self):
        """测试禁用的触发器不执行。"""
        context = StateContext()

        trigger_id = context.trigger_manager.create_trigger()

        action_executed = []

        def test_action():
            action_executed.append(True)

        # 注册事件和动作
        context.trigger_manager.register_event(trigger_id, EVENT_UNIT_DEATH, None)
        trigger = context.trigger_manager.get_trigger(trigger_id)
        trigger.add_action(test_action)

        # 禁用触发器
        context.trigger_manager.disable_trigger(trigger_id)

        # 创建并杀死单位
        unit_id = context.handle_manager.create_unit("hfoo", 0, 100.0, 200.0, 270.0)
        context.handle_manager.kill_unit(unit_id)

        # 验证动作未执行
        assert len(action_executed) == 0

    def test_multiple_triggers_same_event(self):
        """测试多个触发器注册同一事件。"""
        context = StateContext()

        trigger_id1 = context.trigger_manager.create_trigger()
        trigger_id2 = context.trigger_manager.create_trigger()

        executions = []

        def action1():
            executions.append("action1")

        def action2():
            executions.append("action2")

        # 为两个触发器注册同一事件
        context.trigger_manager.register_event(trigger_id1, EVENT_UNIT_DEATH, None)
        context.trigger_manager.register_event(trigger_id2, EVENT_UNIT_DEATH, None)

        trigger1 = context.trigger_manager.get_trigger(trigger_id1)
        trigger2 = context.trigger_manager.get_trigger(trigger_id2)
        trigger1.add_action(action1)
        trigger2.add_action(action2)

        # 创建并杀死单位
        unit_id = context.handle_manager.create_unit("hfoo", 0, 100.0, 200.0, 270.0)
        context.handle_manager.kill_unit(unit_id)

        # 验证两个动作都执行
        assert "action1" in executions
        assert "action2" in executions

    def test_trigger_destroy_removes_event_handler(self):
        """测试销毁触发器后事件不再触发。"""
        context = StateContext()

        trigger_id = context.trigger_manager.create_trigger()

        action_executed = []

        def test_action():
            action_executed.append(True)

        # 注册事件和动作
        context.trigger_manager.register_event(trigger_id, EVENT_UNIT_DEATH, None)
        trigger = context.trigger_manager.get_trigger(trigger_id)
        trigger.add_action(test_action)

        # 销毁触发器
        context.trigger_manager.destroy_trigger(trigger_id)

        # 创建并杀死单位
        unit_id = context.handle_manager.create_unit("hfoo", 0, 100.0, 200.0, 270.0)
        context.handle_manager.kill_unit(unit_id)

        # 验证动作未执行
        assert len(action_executed) == 0
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/integration/test_trigger_system.py::TestTriggerSystemIntegration::test_complete_trigger_flow -v`
Expected: FAIL (如果HandleManager还没有kill_unit方法)

**Step 3: 确保前置条件满足**

如果测试失败是因为前置条件未满足，需要先完成阶段3的实现。

**Step 4: Run test to verify it passes**

Run: `pytest tests/integration/test_trigger_system.py::TestTriggerSystemIntegration::test_complete_trigger_flow -v`
Expected: PASS

**Step 5: Commit**

```bash
git add tests/integration/test_trigger_system.py
git commit -m "test(trigger): add basic trigger system integration tests"
```

---

### Task 2: 创建Native函数集成测试

**Files:**
- Create: `tests/integration/test_trigger_natives.py`

**Step 1: Write the failing test**

```python
"""触发器native函数集成测试。"""

import pytest
from jass_runner.natives.factory import NativeFactory
from jass_runner.natives.state import StateContext
from jass_runner.trigger.event_types import EVENT_UNIT_DEATH


class TestTriggerNativesIntegration:
    """触发器native函数集成测试类。"""

    @pytest.fixture
    def setup(self):
        """创建测试环境。"""
        self.state_context = StateContext()
        self.registry = NativeFactory.create_default_registry()
        return self.state_context, self.registry

    def test_create_trigger_native_integration(self, setup):
        """测试CreateTrigger native函数集成。"""
        state_context, registry = setup

        create_trigger = registry.get_native("CreateTrigger")
        trigger_id = create_trigger.execute(state_context)

        # 验证触发器已创建
        assert trigger_id is not None
        assert trigger_id.startswith("trigger_")

        # 验证可以通过管理器获取
        trigger = state_context.trigger_manager.get_trigger(trigger_id)
        assert trigger is not None
        assert trigger.trigger_id == trigger_id

    def test_enable_disable_trigger_native_integration(self, setup):
        """测试EnableTrigger/DisableTrigger native函数集成。"""
        state_context, registry = setup

        # 创建触发器
        create_trigger = registry.get_native("CreateTrigger")
        trigger_id = create_trigger.execute(state_context)

        # 验证初始状态
        is_enabled = registry.get_native("IsTriggerEnabled")
        assert is_enabled.execute(state_context, trigger_id) is True

        # 禁用触发器
        disable_trigger = registry.get_native("DisableTrigger")
        disable_trigger.execute(state_context, trigger_id)

        # 验证已禁用
        assert is_enabled.execute(state_context, trigger_id) is False

        # 启用触发器
        enable_trigger = registry.get_native("EnableTrigger")
        enable_trigger.execute(state_context, trigger_id)

        # 验证已启用
        assert is_enabled.execute(state_context, trigger_id) is True

    def test_trigger_add_action_native_integration(self, setup):
        """测试TriggerAddAction native函数集成。"""
        state_context, registry = setup

        # 创建触发器
        create_trigger = registry.get_native("CreateTrigger")
        trigger_id = create_trigger.execute(state_context)

        # 定义动作函数
        action_executed = []

        def test_action():
            action_executed.append(True)

        # 添加动作
        add_action = registry.get_native("TriggerAddAction")
        action_handle = add_action.execute(state_context, trigger_id, test_action)

        # 验证动作已添加
        assert action_handle is not None

        # 手动执行动作验证
        trigger = state_context.trigger_manager.get_trigger(trigger_id)
        trigger.execute_actions({})

        assert len(action_executed) == 1

    def test_trigger_add_condition_native_integration(self, setup):
        """测试TriggerAddCondition native函数集成。"""
        state_context, registry = setup

        # 创建触发器
        create_trigger = registry.get_native("CreateTrigger")
        trigger_id = create_trigger.execute(state_context)

        # 定义条件函数
        def true_condition():
            return True

        # 添加条件
        add_condition = registry.get_native("TriggerAddCondition")
        condition_handle = add_condition.execute(state_context, trigger_id, true_condition)

        # 验证条件已添加
        assert condition_handle is not None

        # 评估条件
        evaluate = registry.get_native("TriggerEvaluate")
        result = evaluate.execute(state_context, trigger_id)

        assert result is True

    def test_trigger_register_unit_event_native_integration(self, setup):
        """测试TriggerRegisterUnitEvent native函数集成。"""
        state_context, registry = setup

        # 创建触发器
        create_trigger = registry.get_native("CreateTrigger")
        trigger_id = create_trigger.execute(state_context)

        # 注册单位死亡事件
        register_event = registry.get_native("TriggerRegisterUnitEvent")
        event_handle = register_event.execute(state_context, trigger_id, EVENT_UNIT_DEATH, None)

        # 验证事件已注册
        assert event_handle is not None

        # 添加动作
        action_executed = []

        def test_action():
            action_executed.append(True)

        add_action = registry.get_native("TriggerAddAction")
        add_action.execute(state_context, trigger_id, test_action)

        # 创建并杀死单位
        unit_id = state_context.handle_manager.create_unit("hfoo", 0, 100.0, 200.0, 270.0)
        state_context.handle_manager.kill_unit(unit_id)

        # 验证动作已执行
        assert len(action_executed) == 1

    def test_destroy_trigger_native_integration(self, setup):
        """测试DestroyTrigger native函数集成。"""
        state_context, registry = setup

        # 创建触发器
        create_trigger = registry.get_native("CreateTrigger")
        trigger_id = create_trigger.execute(state_context)

        # 验证触发器存在
        assert state_context.trigger_manager.get_trigger(trigger_id) is not None

        # 销毁触发器
        destroy_trigger = registry.get_native("DestroyTrigger")
        destroy_trigger.execute(state_context, trigger_id)

        # 验证触发器已销毁
        assert state_context.trigger_manager.get_trigger(trigger_id) is None
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/integration/test_trigger_natives.py::TestTriggerNativesIntegration::test_create_trigger_native_integration -v`
Expected: FAIL (如果NativeFactory还没有注册触发器函数)

**Step 3: 确保前置条件满足**

如果测试失败是因为前置条件未满足，需要先完成阶段2的实现。

**Step 4: Run test to verify it passes**

Run: `pytest tests/integration/test_trigger_natives.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add tests/integration/test_trigger_natives.py
git commit -m "test(trigger): add trigger natives integration tests"
```

---

### Task 3: 创建计时器事件集成测试

**Files:**
- Create: `tests/integration/test_trigger_timer.py`

**Step 1: Write the failing test**

```python
"""触发器计时器事件集成测试。"""

import pytest
from jass_runner.natives.state import StateContext
from jass_runner.timer.system import TimerSystem
from jass_runner.trigger.event_types import EVENT_GAME_TIMER_EXPIRED


class TestTriggerTimerIntegration:
    """触发器计时器事件集成测试类。"""

    def test_timer_expire_triggers_event(self):
        """测试计时器到期触发事件。"""
        # 创建状态上下文和计时器系统
        state_context = StateContext()
        timer_system = TimerSystem()
        timer_system.set_trigger_manager(state_context.trigger_manager)

        # 创建触发器
        trigger_id = state_context.trigger_manager.create_trigger()

        # 记录执行
        action_executed = []

        def test_action():
            action_executed.append(True)

        # 注册计时器过期事件
        state_context.trigger_manager.register_event(
            trigger_id, EVENT_GAME_TIMER_EXPIRED, None
        )
        trigger = state_context.trigger_manager.get_trigger(trigger_id)
        trigger.add_action(test_action)

        # 创建并启动计时器
        timer_id = timer_system.create_timer(1.0, False)
        timer_system.start_timer(timer_id)

        # 更新计时器使其到期
        timer_system.update(1.0)

        # 验证动作已执行
        assert len(action_executed) == 1

    def test_timer_expire_with_filter(self):
        """测试特定计时器过滤。"""
        state_context = StateContext()
        timer_system = TimerSystem()
        timer_system.set_trigger_manager(state_context.trigger_manager)

        # 创建两个触发器
        trigger_id1 = state_context.trigger_manager.create_trigger()
        trigger_id2 = state_context.trigger_manager.create_trigger()

        executions = []

        def action1():
            executions.append("action1")

        def action2():
            executions.append("action2")

        # 创建两个计时器
        timer_id1 = timer_system.create_timer(1.0, False)
        timer_id2 = timer_system.create_timer(1.0, False)

        # 为触发器1注册特定计时器事件
        state_context.trigger_manager.register_event(
            trigger_id1, EVENT_GAME_TIMER_EXPIRED, {"timer_id": timer_id1}
        )
        trigger1 = state_context.trigger_manager.get_trigger(trigger_id1)
        trigger1.add_action(action1)

        # 为触发器2注册通用计时器事件
        state_context.trigger_manager.register_event(
            trigger_id2, EVENT_GAME_TIMER_EXPIRED, None
        )
        trigger2 = state_context.trigger_manager.get_trigger(trigger_id2)
        trigger2.add_action(action2)

        # 启动并更新计时器1
        timer_system.start_timer(timer_id1)
        timer_system.update(1.0)

        # 验证两个动作都执行（因为触发器2监听所有计时器事件）
        assert "action1" in executions
        assert "action2" in executions

    def test_periodic_timer_triggers_multiple_times(self):
        """测试周期性计时器多次触发。"""
        state_context = StateContext()
        timer_system = TimerSystem()
        timer_system.set_trigger_manager(state_context.trigger_manager)

        # 创建触发器
        trigger_id = state_context.trigger_manager.create_trigger()

        # 记录执行次数
        execution_count = [0]

        def count_action():
            execution_count[0] += 1

        # 注册事件
        state_context.trigger_manager.register_event(
            trigger_id, EVENT_GAME_TIMER_EXPIRED, None
        )
        trigger = state_context.trigger_manager.get_trigger(trigger_id)
        trigger.add_action(count_action)

        # 创建并启动周期性计时器
        timer_id = timer_system.create_timer(1.0, True)
        timer_system.start_timer(timer_id)

        # 更新计时器多次
        timer_system.update(1.0)  # 第一次触发
        timer_system.update(1.0)  # 第二次触发
        timer_system.update(1.0)  # 第三次触发

        # 验证触发了3次
        assert execution_count[0] == 3
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/integration/test_trigger_timer.py::TestTriggerTimerIntegration::test_timer_expire_triggers_event -v`
Expected: FAIL (如果TimerSystem还没有集成TriggerManager)

**Step 3: 确保前置条件满足**

如果测试失败是因为前置条件未满足，需要先完成阶段3的实现。

**Step 4: Run test to verify it passes**

Run: `pytest tests/integration/test_trigger_timer.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add tests/integration/test_trigger_timer.py
git commit -m "test(trigger): add timer event integration tests"
```

---

### Task 4: 创建示例JASS脚本

**Files:**
- Create: `examples/trigger_basic.j`
- Create: `examples/trigger_unit_death.j`
- Create: `examples/trigger_timer.j`

**Step 1: Write the example files**

```jass
// examples/trigger_basic.j
// 基础触发器示例

function onUnitDeath takes nothing returns nothing
    // 当单位死亡时输出消息
    call DisplayTextToPlayer(GetLocalPlayer(), 0, 0, "A unit has died!")
endfunction

function main takes nothing returns nothing
    local trigger t = CreateTrigger()

    // 注册单位死亡事件
    call TriggerRegisterUnitEvent(t, EVENT_UNIT_DEATH, null)

    // 添加动作
    call TriggerAddAction(t, function onUnitDeath)

    // 现在当任意单位死亡时，将输出消息
    call DisplayTextToPlayer(GetLocalPlayer(), 0, 0, "Trigger system initialized!")
endfunction
```

```jass
// examples/trigger_unit_death.j
// 单位死亡事件处理示例

globals
    integer deathCount = 0
endglobals

function conditionIsEnemyUnit takes nothing returns boolean
    // 条件：检查是否是敌方单位
    // 实际实现中应该检查单位所属玩家
    return true
endfunction

function actionCountDeath takes nothing returns nothing
    set deathCount = deathCount + 1
    call DisplayTextToPlayer(GetLocalPlayer(), 0, 0, "Unit death count: " + I2S(deathCount))
endfunction

function main takes nothing returns nothing
    local trigger t = CreateTrigger()

    // 注册玩家单位死亡事件
    call TriggerRegisterPlayerUnitEvent(t, Player(0), EVENT_PLAYER_UNIT_DEATH, null)

    // 添加条件
    call TriggerAddCondition(t, function conditionIsEnemyUnit)

    // 添加动作
    call TriggerAddAction(t, function actionCountDeath)

    call DisplayTextToPlayer(GetLocalPlayer(), 0, 0, "Death counter initialized!")
endfunction
```

```jass
// examples/trigger_timer.j
// 计时器触发器示例

globals
    integer tickCount = 0
    timer gameTimer = null
    trigger timerTrigger = null
endglobals

function onTimerTick takes nothing returns nothing
    set tickCount = tickCount + 1
    call DisplayTextToPlayer(GetLocalPlayer(), 0, 0, "Tick: " + I2S(tickCount))

    // 10秒后停止
    if tickCount >= 10 then
        call DisableTrigger(timerTrigger)
        call DisplayTextToPlayer(GetLocalPlayer(), 0, 0, "Timer stopped after 10 ticks!")
    endif
endfunction

function main takes nothing returns nothing
    set timerTrigger = CreateTrigger()

    // 创建计时器
    set gameTimer = CreateTimer()
    call TimerStart(gameTimer, 1.0, true, null)

    // 注册计时器事件
    call TriggerRegisterTimerEvent(timerTrigger, 1.0, true)

    // 添加动作
    call TriggerAddAction(timerTrigger, function onTimerTick)

    call DisplayTextToPlayer(GetLocalPlayer(), 0, 0, "Timer trigger started!")
endfunction
```

**Step 2: 创建示例运行脚本**

```python
# examples/run_trigger_examples.py
"""触发器示例运行脚本。"""

import sys
import os

# 添加src到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from jass_runner.vm.jass_vm import JassVM


def run_example(jass_file):
    """运行JASS示例文件。"""
    print(f"\n{'='*60}")
    print(f"Running: {jass_file}")
    print('='*60)

    try:
        with open(jass_file, 'r', encoding='utf-8') as f:
            code = f.read()

        vm = JassVM()
        result = vm.execute(code)

        if result.success:
            print("✓ Execution successful")
            if result.output:
                print(f"Output: {result.output}")
        else:
            print(f"✗ Execution failed: {result.error}")

    except FileNotFoundError:
        print(f"✗ File not found: {jass_file}")
    except Exception as e:
        print(f"✗ Error: {e}")


def main():
    """主函数。"""
    examples_dir = os.path.dirname(__file__)

    examples = [
        'trigger_basic.j',
        'trigger_unit_death.j',
        'trigger_timer.j',
    ]

    print("JASS Trigger System Examples")
    print("=" * 60)

    for example in examples:
        example_path = os.path.join(examples_dir, example)
        run_example(example_path)

    print(f"\n{'='*60}")
    print("All examples completed!")
    print('='*60)


if __name__ == "__main__":
    main()
```

**Step 3: Run the example script**

Run: `python examples/run_trigger_examples.py`
Expected: 示例运行（可能部分功能还未完全实现）

**Step 4: Commit**

```bash
git add examples/trigger_basic.j examples/trigger_unit_death.j examples/trigger_timer.j examples/run_trigger_examples.py
git commit -m "feat(trigger): add example JASS scripts for trigger system"
```

---

### Task 5: 更新trigger模块导出

**Files:**
- Modify: `src/jass_runner/trigger/__init__.py`

**Step 1: Write the failing test**

```python
"""添加到 tests/trigger/test_trigger_imports.py """


def test_trigger_module_exports_trigger_class():
    """测试trigger模块导出Trigger类。"""
    from jass_runner.trigger import Trigger
    from jass_runner.trigger.trigger import Trigger as DirectTrigger

    assert Trigger is DirectTrigger


def test_trigger_module_exports_manager():
    """测试trigger模块导出TriggerManager。"""
    from jass_runner.trigger import TriggerManager
    from jass_runner.trigger.manager import TriggerManager as DirectManager

    assert TriggerManager is DirectManager
```

**Step 2: Run test to verify it passes**

Run: `pytest tests/trigger/test_trigger_imports.py -v`
Expected: PASS (已经在阶段1中实现)

**Step 3: Commit**

如果测试已经通过，无需额外提交。

---

### Task 6: 运行阶段4完整测试套件

**Files:**
- Test: 所有阶段4相关测试文件

**Step 1: 运行所有集成测试**

Run: `pytest tests/integration/test_trigger_system.py tests/integration/test_trigger_natives.py tests/integration/test_trigger_timer.py -v`
Expected: 所有测试通过

**Step 2: 验证测试覆盖率**

Run: `pytest --cov=src/jass_runner/trigger --cov=src/jass_runner/natives/trigger_natives --cov-report=term-missing tests/integration/`
Expected: 显示覆盖率报告，集成测试覆盖率达到良好水平

**Step 3: 运行完整项目测试确保无回归**

Run: `pytest tests/ -v`
Expected: 所有现有测试通过，无回归

**Step 4: 提交最终状态**

```bash
git add .
git commit -m "feat(trigger): complete phase 4 - integration tests and examples"
```

---

## 阶段4完成标准

1. **基础集成测试**：完整的触发器流程测试（创建→注册→条件→动作→触发）
2. **Native函数集成测试**：20个native函数的端到端测试
3. **计时器事件测试**：计时器到期触发事件的完整测试
4. **示例JASS脚本**：
   - `trigger_basic.j` - 基础触发器示例
   - `trigger_unit_death.j` - 单位死亡事件示例
   - `trigger_timer.j` - 计时器触发器示例
5. **示例运行脚本**：`run_trigger_examples.py`用于运行所有示例
6. **完整测试覆盖**：集成测试覆盖所有主要使用场景
7. **无回归**：所有现有测试通过

## 项目完成总结

触发器系统实现完成，包含：

### 核心组件（阶段1）
- Trigger类：事件、条件、动作管理
- TriggerManager类：生命周期管理和事件分发
- EventTypes：12个标准事件类型定义

### Native函数（阶段2）
- 生命周期管理：5个函数
- 动作管理：3个函数
- 条件管理：4个函数
- 事件注册：6个函数
- 事件清理：1个函数
- 总计：20个native函数

### 系统集成（阶段3）
- StateContext集成TriggerManager
- HandleManager触发单位死亡事件
- TimerSystem触发计时器事件
- ExecutionContext暴露TriggerManager

### 测试和示例（阶段4）
- 基础集成测试
- Native函数集成测试
- 计时器事件集成测试
- 3个示例JASS脚本

---

**计划完成！**

四个阶段的实施计划已全部创建：
1. `docs/plans/2026-03-01-trigger-system-phase1-core.md`
2. `docs/plans/2026-03-01-trigger-system-phase2-natives.md`
3. `docs/plans/2026-03-01-trigger-system-phase3-integration.md`
4. `docs/plans/2026-03-01-trigger-system-phase4-integration-tests.md`
