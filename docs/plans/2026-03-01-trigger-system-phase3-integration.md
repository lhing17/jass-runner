# JASS触发器系统实施计划 - 阶段3：系统集成

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 将触发器系统与HandleManager、TimerSystem和ExecutionContext集成，实现完整的事件触发流程。

**Architecture:** 在StateContext中添加TriggerManager，修改HandleManager在关键操作（如KillUnit）时触发事件，修改TimerSystem在计时器到期时触发事件。

**Tech Stack:** Python 3.8+, pytest, 现有StateContext、HandleManager、TimerSystem

---

### Task 1: 在StateContext中集成TriggerManager

**Files:**
- Modify: `src/jass_runner/natives/state.py`
- Test: `tests/natives/test_state.py`

**Step 1: Write the failing test**

```python
"""添加到 tests/natives/test_state.py """


def test_state_context_has_trigger_manager():
    """测试StateContext包含TriggerManager。"""
    from jass_runner.natives.state import StateContext
    from jass_runner.trigger.manager import TriggerManager

    context = StateContext()

    # 验证TriggerManager存在
    assert hasattr(context, 'trigger_manager')
    assert isinstance(context.trigger_manager, TriggerManager)


def test_state_context_trigger_manager_integration():
    """测试StateContext中TriggerManager的集成功能。"""
    from jass_runner.natives.state import StateContext
    from jass_runner.trigger.event_types import EVENT_UNIT_DEATH

    context = StateContext()

    # 创建触发器
    trigger_id = context.trigger_manager.create_trigger()

    # 记录动作执行
    action_executed = []

    def test_action():
        action_executed.append(True)

    # 注册事件和动作
    context.trigger_manager.register_event(trigger_id, EVENT_UNIT_DEATH, None)
    trigger = context.trigger_manager.get_trigger(trigger_id)
    trigger.add_action(test_action)

    # 触发事件
    context.trigger_manager.fire_event(EVENT_UNIT_DEATH, {"unit_id": "unit_001"})

    # 验证动作已执行
    assert len(action_executed) == 1
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/natives/test_state.py::test_state_context_has_trigger_manager -v`
Expected: FAIL with "AttributeError: 'StateContext' object has no attribute 'trigger_manager'"

**Step 3: Write minimal implementation**

```python
"""修改 src/jass_runner/natives/state.py """

from typing import Dict
from .manager import HandleManager
from ..trigger.manager import TriggerManager


class StateContext:
    """状态上下文，管理全局和局部状态。

    采用混合方案：
    - 全局状态（handle引用）由HandleManager管理
    - 局部状态（临时变量）由ExecutionContext管理
    - 触发器系统由TriggerManager管理
    """

    def __init__(self):
        self.handle_manager = HandleManager()
        self.trigger_manager = TriggerManager()
        self.global_vars = {}  # 全局变量存储
        self.local_stores = {}  # 上下文局部存储

    def get_context_store(self, context_id: str) -> Dict:
        """获取指定上下文的局部存储。"""
        if context_id not in self.local_stores:
            self.local_stores[context_id] = {}
        return self.local_stores[context_id]
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/natives/test_state.py::test_state_context_has_trigger_manager -v`
Expected: PASS

**Step 5: Commit**

```bash
git add tests/natives/test_state.py src/jass_runner/natives/state.py
git commit -m "feat(trigger): integrate TriggerManager into StateContext"
```

---

### Task 2: 修改KillUnit触发单位死亡事件

**Files:**
- Modify: `src/jass_runner/natives/manager.py`
- Test: `tests/natives/test_manager.py`

**Step 1: Write the failing test**

```python
"""添加到 tests/natives/test_manager.py """

from unittest.mock import Mock


def test_kill_unit_triggers_death_event():
    """测试KillUnit触发单位死亡事件。"""
    from jass_runner.natives.manager import HandleManager
    from jass_runner.trigger.event_types import EVENT_UNIT_DEATH

    manager = HandleManager()

    # 创建模拟的trigger_manager
    mock_trigger_manager = Mock()
    manager._trigger_manager = mock_trigger_manager

    # 创建单位
    unit_id = manager.create_unit("hfoo", 0, 100.0, 200.0, 270.0)

    # 杀死单位
    result = manager.kill_unit(unit_id)

    # 验证事件被触发
    assert result is True
    mock_trigger_manager.fire_event.assert_called_once()
    call_args = mock_trigger_manager.fire_event.call_args
    assert call_args[0][0] == EVENT_UNIT_DEATH
    assert call_args[0][1]["unit_id"] == unit_id


def test_kill_unit_without_trigger_manager():
    """测试KillUnit在没有trigger_manager时不报错。"""
    from jass_runner.natives.manager import HandleManager

    manager = HandleManager()

    # 不设置trigger_manager
    manager._trigger_manager = None

    # 创建并杀死单位
    unit_id = manager.create_unit("hfoo", 0, 100.0, 200.0, 270.0)
    result = manager.kill_unit(unit_id)

    # 验证正常执行
    assert result is True
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/natives/test_manager.py::test_kill_unit_triggers_death_event -v`
Expected: FAIL with "AttributeError: 'HandleManager' object has no attribute 'kill_unit'" (或类似错误)

**Step 3: Write minimal implementation**

```python
"""修改 src/jass_runner/natives/manager.py """

class HandleManager:
    """集中式handle管理器。

    负责所有handle的生命周期管理。
    """

    def __init__(self):
        self._handles: Dict[str, Handle] = {}
        self._type_index: Dict[str, List[str]] = {}
        self._next_id = 1
        self._trigger_manager = None  # 将在集成时设置

    def set_trigger_manager(self, trigger_manager):
        """设置触发器管理器。

        参数：
            trigger_manager: TriggerManager实例
        """
        self._trigger_manager = trigger_manager

    def kill_unit(self, unit_id: str) -> bool:
        """杀死单位并触发死亡事件。

        参数：
            unit_id: 单位ID

        返回：
            是否成功杀死
        """
        unit = self.get_unit(unit_id)
        if not unit:
            return False

        # 销毁单位
        unit.destroy()

        # 触发单位死亡事件
        if self._trigger_manager:
            from ..trigger.event_types import EVENT_UNIT_DEATH
            self._trigger_manager.fire_event(EVENT_UNIT_DEATH, {
                "unit_id": unit_id,
                "unit_type": unit.unit_type if unit else None
            })

        return True
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/natives/test_manager.py::test_kill_unit_triggers_death_event -v`
Expected: PASS

**Step 5: Commit**

```bash
git add tests/natives/test_manager.py src/jass_runner/natives/manager.py
git commit -m "feat(trigger): add kill_unit method with death event trigger"
```

---

### Task 3: 修改StateContext连接HandleManager和TriggerManager

**Files:**
- Modify: `src/jass_runner/natives/state.py`
- Test: `tests/natives/test_state.py`

**Step 1: Write the failing test**

```python
"""添加到 tests/natives/test_state.py """


def test_state_context_connects_managers():
    """测试StateContext正确连接HandleManager和TriggerManager。"""
    from jass_runner.natives.state import StateContext
    from jass_runner.trigger.event_types import EVENT_UNIT_DEATH

    context = StateContext()

    # 创建触发器并注册单位死亡事件
    trigger_id = context.trigger_manager.create_trigger()

    action_executed = []

    def test_action():
        action_executed.append(True)

    context.trigger_manager.register_event(trigger_id, EVENT_UNIT_DEATH, None)
    trigger = context.trigger_manager.get_trigger(trigger_id)
    trigger.add_action(test_action)

    # 创建并杀死单位（通过HandleManager）
    unit_id = context.handle_manager.create_unit("hfoo", 0, 100.0, 200.0, 270.0)

    # 杀死单位应该触发事件
    context.handle_manager.kill_unit(unit_id)

    # 验证动作已执行
    assert len(action_executed) == 1
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/natives/test_state.py::test_state_context_connects_managers -v`
Expected: FAIL (因为HandleManager还没有自动连接到TriggerManager)

**Step 3: Write minimal implementation**

```python
"""修改 src/jass_runner/natives/state.py """

class StateContext:
    """状态上下文，管理全局和局部状态。

    采用混合方案：
    - 全局状态（handle引用）由HandleManager管理
    - 局部状态（临时变量）由ExecutionContext管理
    - 触发器系统由TriggerManager管理
    """

    def __init__(self):
        self.handle_manager = HandleManager()
        self.trigger_manager = TriggerManager()
        self.global_vars = {}  # 全局变量存储
        self.local_stores = {}  # 上下文局部存储

        # 连接HandleManager和TriggerManager
        self.handle_manager.set_trigger_manager(self.trigger_manager)

    def get_context_store(self, context_id: str) -> Dict:
        """获取指定上下文的局部存储。"""
        if context_id not in self.local_stores:
            self.local_stores[context_id] = {}
        return self.local_stores[context_id]
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/natives/test_state.py::test_state_context_connects_managers -v`
Expected: PASS

**Step 5: Commit**

```bash
git add tests/natives/test_state.py src/jass_runner/natives/state.py
git commit -m "feat(trigger): connect HandleManager to TriggerManager in StateContext"
```

---

### Task 4: 修改TimerSystem支持触发器事件

**Files:**
- Modify: `src/jass_runner/timer/timer.py` 和 `src/jass_runner/timer/system.py`
- Test: `tests/timer/test_timer.py`

**Step 1: Write the failing test**

```python
"""添加到 tests/timer/test_timer.py """

from unittest.mock import Mock


def test_timer_triggers_event_on_expire():
    """测试计时器到期时触发事件。"""
    from jass_runner.timer.timer import Timer
    from jass_runner.trigger.event_types import EVENT_GAME_TIMER_EXPIRED

    # 创建模拟的trigger_manager
    mock_trigger_manager = Mock()

    # 创建计时器
    timer = Timer("timer_001", 1.0, False)
    timer.set_trigger_manager(mock_trigger_manager)

    # 模拟计时器到期
    timer.update(1.0)

    # 验证事件被触发
    mock_trigger_manager.fire_event.assert_called_once()
    call_args = mock_trigger_manager.fire_event.call_args
    assert call_args[0][0] == EVENT_GAME_TIMER_EXPIRED
    assert call_args[0][1]["timer_id"] == "timer_001"


def test_timer_without_trigger_manager():
    """测试计时器在没有trigger_manager时不报错。"""
    from jass_runner.timer.timer import Timer

    # 创建计时器，不设置trigger_manager
    timer = Timer("timer_001", 1.0, False)

    # 模拟计时器到期
    timer.update(1.0)  # 不应抛出异常

    # 验证正常执行
    assert True
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/timer/test_timer.py::test_timer_triggers_event_on_expire -v`
Expected: FAIL with "AttributeError" (因为Timer还没有set_trigger_manager方法)

**Step 3: Write minimal implementation**

```python
"""修改 src/jass_runner/timer/timer.py """

from typing import Callable, Optional


class Timer:
    """计时器类。

    管理单个计时器的状态和回调。
    """

    def __init__(self, timer_id: str, interval: float, periodic: bool = False):
        """初始化计时器。

        参数：
            timer_id: 计时器唯一标识符
            interval: 间隔时间（秒）
            periodic: 是否周期性触发
        """
        self.timer_id = timer_id
        self.interval = interval
        self.periodic = periodic
        self._elapsed = 0.0
        self._fired = False
        self._paused = False
        self.callback: Optional[Callable] = None
        self._trigger_manager = None

    def set_trigger_manager(self, trigger_manager):
        """设置触发器管理器。

        参数：
            trigger_manager: TriggerManager实例
        """
        self._trigger_manager = trigger_manager

    def update(self, delta_time: float):
        """更新计时器状态。

        参数：
            delta_time: 经过的时间（秒）
        """
        if self._paused or self._fired:
            return

        self._elapsed += delta_time

        if self._elapsed >= self.interval:
            self._fired = True

            # 执行回调
            if self.callback:
                self.callback()

            # 触发计时器事件
            if self._trigger_manager:
                from ..trigger.event_types import EVENT_GAME_TIMER_EXPIRED
                self._trigger_manager.fire_event(EVENT_GAME_TIMER_EXPIRED, {
                    "timer_id": self.timer_id
                })

            # 如果是周期性计时器，重置状态
            if self.periodic:
                self._elapsed = 0.0
                self._fired = False
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/timer/test_timer.py::test_timer_triggers_event_on_expire -v`
Expected: PASS

**Step 5: Commit**

```bash
git add tests/timer/test_timer.py src/jass_runner/timer/timer.py
git commit -m "feat(trigger): add timer event trigger on expire"
```

---

### Task 5: 修改TimerSystem连接TriggerManager

**Files:**
- Modify: `src/jass_runner/timer/system.py`
- Test: `tests/timer/test_system.py`

**Step 1: Write the failing test**

```python
"""添加到 tests/timer/test_system.py """

from unittest.mock import Mock


def test_timer_system_set_trigger_manager():
    """测试TimerSystem设置TriggerManager。"""
    from jass_runner.timer.system import TimerSystem

    system = TimerSystem()
    mock_trigger_manager = Mock()

    # 设置trigger_manager
    system.set_trigger_manager(mock_trigger_manager)

    # 验证已设置
    assert system._trigger_manager == mock_trigger_manager


def test_timer_system_creates_timers_with_trigger_manager():
    """测试TimerSystem创建的计时器带有TriggerManager。"""
    from jass_runner.timer.system import TimerSystem
    from jass_runner.trigger.event_types import EVENT_GAME_TIMER_EXPIRED

    system = TimerSystem()
    mock_trigger_manager = Mock()

    system.set_trigger_manager(mock_trigger_manager)

    # 创建计时器
    timer_id = system.create_timer(1.0, False)

    # 启动计时器
    system.start_timer(timer_id)

    # 更新计时器使其到期
    system.update(1.0)

    # 验证事件被触发
    mock_trigger_manager.fire_event.assert_called_once()
    call_args = mock_trigger_manager.fire_event.call_args
    assert call_args[0][0] == EVENT_GAME_TIMER_EXPIRED
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/timer/test_system.py::test_timer_system_set_trigger_manager -v`
Expected: FAIL with "AttributeError" (因为TimerSystem还没有set_trigger_manager方法)

**Step 3: Write minimal implementation**

```python
"""修改 src/jass_runner/timer/system.py """

from typing import Dict, Optional
from .timer import Timer


class TimerSystem:
    """计时器系统。

    管理多个计时器的创建、更新和销毁。
    """

    def __init__(self):
        """初始化计时器系统。"""
        self._timers: Dict[str, Timer] = {}
        self._next_id = 1
        self._trigger_manager = None

    def set_trigger_manager(self, trigger_manager):
        """设置触发器管理器。

        参数：
            trigger_manager: TriggerManager实例
        """
        self._trigger_manager = trigger_manager

    def _generate_timer_id(self) -> str:
        """生成唯一的计时器ID。"""
        timer_id = f"timer_{self._next_id}"
        self._next_id += 1
        return timer_id

    def create_timer(self, interval: float, periodic: bool = False) -> str:
        """创建新计时器。

        参数：
            interval: 间隔时间（秒）
            periodic: 是否周期性

        返回：
            计时器ID
        """
        timer_id = self._generate_timer_id()
        timer = Timer(timer_id, interval, periodic)

        # 设置trigger_manager
        if self._trigger_manager:
            timer.set_trigger_manager(self._trigger_manager)

        self._timers[timer_id] = timer
        return timer_id

    # ... 其他现有方法保持不变 ...
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/timer/test_system.py::test_timer_system_set_trigger_manager -v`
Expected: PASS

**Step 5: Commit**

```bash
git add tests/timer/test_system.py src/jass_runner/timer/system.py
git commit -m "feat(trigger): integrate TriggerManager into TimerSystem"
```

---

### Task 6: 修改ExecutionContext集成StateContext的TriggerManager

**Files:**
- Modify: `src/jass_runner/interpreter/context.py`
- Test: `tests/interpreter/test_context.py`

**Step 1: Write the failing test**

```python
"""添加到 tests/interpreter/test_context.py """


def test_execution_context_access_trigger_manager():
    """测试ExecutionContext可以访问TriggerManager。"""
    from jass_runner.interpreter.context import ExecutionContext
    from jass_runner.natives.state import StateContext
    from jass_runner.trigger.manager import TriggerManager

    # 创建StateContext
    state_context = StateContext()

    # 创建ExecutionContext
    exec_context = ExecutionContext(state_context=state_context)

    # 验证可以访问trigger_manager
    assert hasattr(exec_context, 'trigger_manager')
    assert isinstance(exec_context.trigger_manager, TriggerManager)


def test_execution_context_trigger_manager_integration():
    """测试ExecutionContext中TriggerManager的集成功能。"""
    from jass_runner.interpreter.context import ExecutionContext
    from jass_runner.natives.state import StateContext
    from jass_runner.trigger.event_types import EVENT_PLAYER_DEFEAT

    state_context = StateContext()
    exec_context = ExecutionContext(state_context=state_context)

    # 创建触发器并注册事件
    trigger_id = exec_context.trigger_manager.create_trigger()

    action_executed = []

    def test_action():
        action_executed.append(True)

    exec_context.trigger_manager.register_event(trigger_id, EVENT_PLAYER_DEFEAT, None)
    trigger = exec_context.trigger_manager.get_trigger(trigger_id)
    trigger.add_action(test_action)

    # 触发事件
    exec_context.trigger_manager.fire_event(EVENT_PLAYER_DEFEAT, {"player_id": 0})

    # 验证动作已执行
    assert len(action_executed) == 1
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/interpreter/test_context.py::test_execution_context_access_trigger_manager -v`
Expected: FAIL with "AttributeError" (因为ExecutionContext还没有trigger_manager属性)

**Step 3: Write minimal implementation**

```python
"""修改 src/jass_runner/interpreter/context.py """

from typing import Any, Dict, Optional
from ..natives.registry import NativeRegistry
from ..natives.state import StateContext


class ExecutionContext:
    """执行上下文。

    管理变量作用域和native函数注册表。
    """

    def __init__(self, parent: Optional['ExecutionContext'] = None,
                 native_registry: Optional[NativeRegistry] = None,
                 state_context: Optional[StateContext] = None):
        """初始化执行上下文。

        参数：
            parent: 父上下文（用于函数调用栈）
            native_registry: native函数注册表
            state_context: 状态上下文
        """
        self._variables: Dict[str, Any] = {}
        self._parent = parent
        self._native_registry = native_registry
        self._state_context = state_context

    @property
    def trigger_manager(self):
        """获取触发器管理器。"""
        if self._state_context:
            return self._state_context.trigger_manager
        return None

    # ... 其他现有方法保持不变 ...
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/interpreter/test_context.py::test_execution_context_access_trigger_manager -v`
Expected: PASS

**Step 5: Commit**

```bash
git add tests/interpreter/test_context.py src/jass_runner/interpreter/context.py
git commit -m "feat(trigger): expose TriggerManager through ExecutionContext"
```

---

### Task 7: 运行阶段3完整测试套件

**Files:**
- Test: 所有阶段3相关测试文件

**Step 1: 运行所有集成相关测试**

Run: `pytest tests/natives/test_state.py tests/natives/test_manager.py tests/timer/test_timer.py tests/timer/test_system.py tests/interpreter/test_context.py -v`
Expected: 所有测试通过

**Step 2: 验证测试覆盖率**

Run: `pytest --cov=src/jass_runner --cov-report=term-missing tests/natives/test_state.py tests/natives/test_manager.py tests/timer/test_timer.py tests/timer/test_system.py tests/interpreter/test_context.py`
Expected: 显示覆盖率报告

**Step 3: 运行完整项目测试确保无回归**

Run: `pytest tests/ -v`
Expected: 所有现有测试通过，无回归

**Step 4: 提交最终状态**

```bash
git add .
git commit -m "feat(trigger): complete phase 3 - system integration"
```

---

## 阶段3完成标准

1. **StateContext集成**：TriggerManager集成到StateContext中
2. **HandleManager集成**：KillUnit方法触发单位死亡事件
3. **Manager连接**：HandleManager和TriggerManager在StateContext中正确连接
4. **Timer集成**：计时器到期时触发事件
5. **TimerSystem集成**：TimerSystem支持设置TriggerManager
6. **ExecutionContext集成**：通过ExecutionContext可以访问TriggerManager
7. **完整测试覆盖**：所有集成功能都有单元测试
8. **无回归**：所有现有测试通过

## 下一阶段

阶段4将创建集成测试和示例JASS脚本。
计划保存为：`docs/plans/2026-03-01-trigger-system-phase4-integration-tests.md`
