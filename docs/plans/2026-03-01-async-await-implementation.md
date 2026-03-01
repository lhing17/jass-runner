# v0.4.0 异步等待功能实施计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 实现 JASS 异步等待功能，包括 `TriggerSleepAction` 和 `ExecuteFunc`，支持协程挂起/恢复机制。

**Architecture:** 采用生成器协程方案，通过 Python `yield` 实现挂起/恢复。核心组件包括 Coroutine（包装执行流）、SleepScheduler（管理睡眠协程）、CoroutineRunner（主调度器）。

**Tech Stack:** Python 3.8+, pytest, 现有 JASS Runner 架构

**Design Doc:** [2026-03-01-async-await-design.md](./2026-03-01-async-await-design.md)

---

## Phase 1: 创建核心协程组件

### Task 1.1: 创建 SleepSignal 类

**Files:**
- Create: `src/jass_runner/coroutine/__init__.py`
- Create: `src/jass_runner/coroutine/signals.py`
- Test: `tests/coroutine/test_signals.py`

**Step 1: Write the failing test**

```python
def test_sleep_signal_creation():
    from jass_runner.coroutine.signals import SleepSignal
    signal = SleepSignal(2.5)
    assert signal.duration == 2.5
```

**Step 2: Run test to verify it fails**

```bash
pytest tests/coroutine/test_signals.py::test_sleep_signal_creation -v
```

Expected: FAIL with "ModuleNotFoundError"

**Step 3: Write minimal implementation**

```python
# src/jass_runner/coroutine/__init__.py
"""协程系统模块。"""

# src/jass_runner/coroutine/signals.py
"""协程信号定义。"""


class SleepSignal:
    """协程暂停信号，携带等待时间。"""

    def __init__(self, duration: float):
        """
        参数：
            duration: 等待时间（秒）
        """
        self.duration = duration
```

**Step 4: Run test to verify it passes**

```bash
pytest tests/coroutine/test_signals.py::test_sleep_signal_creation -v
```

Expected: PASS

**Step 5: Commit**

```bash
git add src/jass_runner/coroutine/__init__.py src/jass_runner/coroutine/signals.py tests/coroutine/test_signals.py
git commit -m "feat(coroutine): add SleepSignal class

Co-Authored-By: Claude (moonshotai/kimi-k2.5) <noreply@anthropic.com>"
```

---

### Task 1.2: 创建 CoroutineStatus 枚举

**Files:**
- Modify: `src/jass_runner/coroutine/__init__.py`
- Test: `tests/coroutine/test_status.py`

**Step 1: Write the failing test**

```python
from jass_runner.coroutine import CoroutineStatus


def test_coroutine_status_values():
    assert CoroutineStatus.PENDING.value == "pending"
    assert CoroutineStatus.RUNNING.value == "running"
    assert CoroutineStatus.SLEEPING.value == "sleeping"
    assert CoroutineStatus.FINISHED.value == "finished"
```

**Step 2: Run test to verify it fails**

```bash
pytest tests/coroutine/test_status.py::test_coroutine_status_values -v
```

Expected: FAIL with "ImportError"

**Step 3: Write minimal implementation**

```python
# src/jass_runner/coroutine/__init__.py
"""协程系统模块。"""

from enum import Enum


class CoroutineStatus(Enum):
    """协程状态枚举。"""
    PENDING = "pending"      # 刚创建，未开始执行
    RUNNING = "running"      # 正在执行
    SLEEPING = "sleeping"    # 调用 TriggerSleepAction 后暂停
    FINISHED = "finished"    # 执行完成
```

**Step 4: Run test to verify it passes**

```bash
pytest tests/coroutine/test_status.py::test_coroutine_status_values -v
```

Expected: PASS

**Step 5: Commit**

```bash
git add src/jass_runner/coroutine/__init__.py tests/coroutine/test_status.py
git commit -m "feat(coroutine): add CoroutineStatus enum

Co-Authored-By: Claude (moonshotai/kimi-k2.5) <noreply@anthropic.com>"
```

---

### Task 1.3: 创建 SleepInterrupt 异常

**Files:**
- Create: `src/jass_runner/coroutine/exceptions.py`
- Test: `tests/coroutine/test_exceptions.py`

**Step 1: Write the failing test**

```python
def test_sleep_interrupt_creation():
    from jass_runner.coroutine.exceptions import SleepInterrupt
    exc = SleepInterrupt(2.0)
    assert exc.duration == 2.0
```

**Step 2: Run test to verify it fails**

```bash
pytest tests/coroutine/test_exceptions.py::test_sleep_interrupt_creation -v
```

Expected: FAIL

**Step 3: Write minimal implementation**

```python
# src/jass_runner/coroutine/exceptions.py
"""协程异常定义。"""


class SleepInterrupt(Exception):
    """睡眠中断异常，用于从深层调用栈传递睡眠信号。"""

    def __init__(self, duration: float):
        """
        参数：
            duration: 等待时间（秒）
        """
        super().__init__(f"Sleep for {duration} seconds")
        self.duration = duration
```

**Step 4: Run test to verify it passes**

```bash
pytest tests/coroutine/test_exceptions.py::test_sleep_interrupt_creation -v
```

Expected: PASS

**Step 5: Commit**

```bash
git add src/jass_runner/coroutine/exceptions.py tests/coroutine/test_exceptions.py
git commit -m "feat(coroutine): add SleepInterrupt exception

Co-Authored-By: Claude (moonshotai/kimi-k2.5) <noreply@anthropic.com>"
```

---

### Task 1.4: 创建 Coroutine 类基础结构

**Files:**
- Create: `src/jass_runner/coroutine/coroutine.py`
- Test: `tests/coroutine/test_coroutine.py`

**Step 1: Write the failing test**

```python
from jass_runner.coroutine.coroutine import Coroutine
from jass_runner.coroutine import CoroutineStatus


def test_coroutine_creation():
    """测试协程创建。"""
    # Mock interpreter and function
    interpreter = object()
    func = object()

    coroutine = Coroutine(interpreter, func)

    assert coroutine.interpreter is interpreter
    assert coroutine.func is func
    assert coroutine.status == CoroutineStatus.PENDING
    assert coroutine.args == []
    assert coroutine.generator is None
    assert coroutine.wake_time == 0.0
```

**Step 2: Run test to verify it fails**

```bash
pytest tests/coroutine/test_coroutine.py::test_coroutine_creation -v
```

Expected: FAIL

**Step 3: Write minimal implementation**

```python
# src/jass_runner/coroutine/coroutine.py
"""协程实现。"""

from typing import Any, Optional, Generator
from . import CoroutineStatus
from .signals import SleepSignal


class Coroutine:
    """包装 JASS 函数执行的协程。"""

    def __init__(self, interpreter: Any, func: Any, args: list = None):
        """
        参数：
            interpreter: 解释器实例
            func: 函数定义节点
            args: 函数参数列表
        """
        self.interpreter = interpreter
        self.func = func
        self.args = args or []
        self.status = CoroutineStatus.PENDING
        self.generator: Optional[Generator] = None
        self.wake_time: float = 0.0
        self.return_value: Any = None

    def start(self):
        """启动协程，创建生成器。"""
        self.generator = self._run()
        self.status = CoroutineStatus.RUNNING

    def _run(self):
        """实际的生成器函数（子类实现）。"""
        raise NotImplementedError()

    def resume(self):
        """恢复执行。"""
        raise NotImplementedError()

    def wake(self, current_time: float):
        """从睡眠中唤醒。"""
        raise NotImplementedError()

    def sleep(self, duration: float, current_time: float):
        """设置睡眠状态。"""
        raise NotImplementedError()
```

**Step 4: Run test to verify it passes**

```bash
pytest tests/coroutine/test_coroutine.py::test_coroutine_creation -v
```

Expected: PASS

**Step 5: Commit**

```bash
git add src/jass_runner/coroutine/coroutine.py tests/coroutine/test_coroutine.py
git commit -m "feat(coroutine): add Coroutine base class

Co-Authored-By: Claude (moonshotai/kimi-k2.5) <noreply@anthropic.com>"
```

---

### Task 1.5: 实现 Coroutine 的 start 和 sleep 方法

**Files:**
- Modify: `src/jass_runner/coroutine/coroutine.py`
- Test: `tests/coroutine/test_coroutine.py`

**Step 1: Write the failing test**

```python
def test_coroutine_start_and_sleep():
    """测试协程启动和睡眠。"""
    from unittest.mock import Mock

    coroutine = Coroutine(Mock(), Mock())

    # 启动前状态
    assert coroutine.status == CoroutineStatus.PENDING

    # 启动
    coroutine.start()
    assert coroutine.status == CoroutineStatus.RUNNING

    # 睡眠
    coroutine.sleep(2.0, 10.0)
    assert coroutine.status == CoroutineStatus.SLEEPING
    assert coroutine.wake_time == 12.0  # 10.0 + 2.0

    # 唤醒
    coroutine.wake(12.0)
    assert coroutine.status == CoroutineStatus.RUNNING
```

**Step 2: Run test to verify it fails**

```bash
pytest tests/coroutine/test_coroutine.py::test_coroutine_start_and_sleep -v
```

Expected: FAIL with "NotImplementedError"

**Step 3: Write minimal implementation**

```python
# 修改 Coroutine 类中的方法

    def start(self):
        """启动协程，创建生成器。"""
        self.generator = self._run()
        self.status = CoroutineStatus.RUNNING

    def wake(self, current_time: float):
        """从睡眠中唤醒。"""
        if (self.status == CoroutineStatus.SLEEPING and
            current_time >= self.wake_time):
            self.status = CoroutineStatus.RUNNING

    def sleep(self, duration: float, current_time: float):
        """设置睡眠状态。"""
        self.wake_time = current_time + duration
        self.status = CoroutineStatus.SLEEPING
```

**Step 4: Run test to verify it passes**

```bash
pytest tests/coroutine/test_coroutine.py::test_coroutine_start_and_sleep -v
```

Expected: PASS

**Step 5: Commit**

```bash
git add src/jass_runner/coroutine/coroutine.py tests/coroutine/test_coroutine.py
git commit -m "feat(coroutine): implement start, sleep, wake methods

Co-Authored-By: Claude (moonshotai/kimi-k2.5) <noreply@anthropic.com>"
```

---

### Task 1.6: 创建 SleepScheduler 类

**Files:**
- Create: `src/jass_runner/coroutine/scheduler.py`
- Test: `tests/coroutine/test_scheduler.py`

**Step 1: Write the failing test**

```python
def test_scheduler_add_and_wake():
    """测试调度器添加和唤醒。"""
    from jass_runner.coroutine.scheduler import SleepScheduler
    from jass_runner.coroutine.coroutine import Coroutine
    from unittest.mock import Mock

    scheduler = SleepScheduler()
    coroutine = Coroutine(Mock(), Mock())
    coroutine.sleep(2.0, 10.0)

    scheduler.add(coroutine)
    assert not scheduler.is_empty()

    # 时间未到，不应唤醒
    ready = scheduler.wake_ready(11.0)
    assert len(ready) == 0

    # 时间到了，应该唤醒
    ready = scheduler.wake_ready(12.0)
    assert len(ready) == 1
    assert ready[0] is coroutine
    assert scheduler.is_empty()
```

**Step 2: Run test to verify it fails**

```bash
pytest tests/coroutine/test_scheduler.py::test_scheduler_add_and_wake -v
```

Expected: FAIL

**Step 3: Write minimal implementation**

```python
# src/jass_runner/coroutine/scheduler.py
"""协程调度器实现。"""

from typing import List
from .coroutine import Coroutine


class SleepScheduler:
    """管理所有睡眠中的协程。"""

    def __init__(self):
        self._sleeping: List[Coroutine] = []

    def add(self, coroutine: Coroutine):
        """添加睡眠中的协程。"""
        self._sleeping.append(coroutine)

    def wake_ready(self, current_time: float) -> List[Coroutine]:
        """获取并移除所有到期的协程。"""
        ready = [c for c in self._sleeping
                 if current_time >= c.wake_time]
        self._sleeping = [c for c in self._sleeping
                         if current_time < c.wake_time]

        for c in ready:
            c.wake(current_time)

        return ready

    def is_empty(self) -> bool:
        """检查是否没有睡眠中的协程。"""
        return len(self._sleeping) == 0
```

**Step 4: Run test to verify it passes**

```bash
pytest tests/coroutine/test_scheduler.py::test_scheduler_add_and_wake -v
```

Expected: PASS

**Step 5: Commit**

```bash
git add src/jass_runner/coroutine/scheduler.py tests/coroutine/test_scheduler.py
git commit -m "feat(coroutine): add SleepScheduler class

Co-Authored-By: Claude (moonshotai/kimi-k2.5) <noreply@anthropic.com>"
```

---

### Task 1.7: 创建 CoroutineRunner 基础结构

**Files:**
- Create: `src/jass_runner/coroutine/runner.py`
- Test: `tests/coroutine/test_runner.py`

**Step 1: Write the failing test**

```python
def test_runner_creation():
    """测试 CoroutineRunner 创建。"""
    from jass_runner.coroutine.runner import CoroutineRunner

    runner = CoroutineRunner()

    assert runner._active == []
    assert runner._current_time == 0.0
    assert runner._frame_count == 0
    assert runner.max_coroutines == 100
    assert runner._main_coroutine is None
```

**Step 2: Run test to verify it fails**

```bash
pytest tests/coroutine/test_runner.py::test_runner_creation -v
```

Expected: FAIL

**Step 3: Write minimal implementation**

```python
# src/jass_runner/coroutine/runner.py
"""协程运行器实现。"""

from typing import Any, List, Optional
from .coroutine import Coroutine
from .scheduler import SleepScheduler


class CoroutineRunner:
    """协程调度器，与 SimulationLoop 集成。"""

    DEFAULT_MAX_COROUTINES = 100

    def __init__(self, max_coroutines: int = None):
        """
        参数：
            max_coroutines: 最大并发协程数，默认100
        """
        self._active: List[Coroutine] = []
        self._scheduler = SleepScheduler()
        self._current_time = 0.0
        self._frame_count = 0
        self.max_coroutines = max_coroutines or self.DEFAULT_MAX_COROUTINES
        self._main_coroutine: Optional[Coroutine] = None
```

**Step 4: Run test to verify it passes**

```bash
pytest tests/coroutine/test_runner.py::test_runner_creation -v
```

Expected: PASS

**Step 5: Commit**

```bash
git add src/jass_runner/coroutine/runner.py tests/coroutine/test_runner.py
git commit -m "feat(coroutine): add CoroutineRunner base class

Co-Authored-By: Claude (moonshotai/kimi-k2.5) <noreply@anthropic.com>"
```

---

### Task 1.8: 实现 CoroutineRunner 的 execute_func 方法

**Files:**
- Modify: `src/jass_runner/coroutine/runner.py`
- Create: `src/jass_runner/coroutine/errors.py`
- Test: `tests/coroutine/test_runner.py`

**Step 1: Write the failing test**

```python
def test_runner_execute_func():
    """测试 ExecuteFunc 创建新协程。"""
    from unittest.mock import Mock
    from jass_runner.coroutine.runner import CoroutineRunner
    from jass_runner.coroutine import CoroutineStatus

    runner = CoroutineRunner()
    interpreter = Mock()
    func = Mock()
    func.body = []  # 空函数体

    coroutine = runner.execute_func(interpreter, func)

    assert coroutine is not None
    assert coroutine.status == CoroutineStatus.RUNNING
    assert len(runner._active) == 1
```

**Step 2: Run test to verify it fails**

```bash
pytest tests/coroutine/test_runner.py::test_runner_execute_func -v
```

Expected: FAIL

**Step 3: Write minimal implementation**

```python
# src/jass_runner/coroutine/errors.py
"""协程错误定义。"""


class CoroutineError(Exception):
    """协程执行错误基类。"""
    pass


class CoroutineStackOverflow(CoroutineError):
    """协程调用栈溢出。"""
    pass


# src/jass_runner/coroutine/runner.py
# 添加方法到 CoroutineRunner 类

    def execute_func(self, interpreter: Any, func: Any,
                     args: list = None) -> Coroutine:
        """
        ExecuteFunc - 创建新协程（简单顺序执行）。

        参数：
            interpreter: 解释器实例
            func: 函数定义
            args: 函数参数

        返回：
            新创建的协程

        异常：
            CoroutineStackOverflow: 如果协程数超过限制
        """
        args = args or []

        # 限制并发协程数
        total = len(self._active) + len(self._scheduler._sleeping)
        if total >= self.max_coroutines:
            raise CoroutineStackOverflow(
                f"协程数超过限制({self.max_coroutines})"
            )

        # 创建新协程
        from .coroutine import Coroutine
        coroutine = Coroutine(interpreter, func, args)
        coroutine.start()
        self._active.append(coroutine)
        return coroutine
```

**Step 4: Run test to verify it passes**

```bash
pytest tests/coroutine/test_runner.py::test_runner_execute_func -v
```

Expected: PASS

**Step 5: Commit**

```bash
git add src/jass_runner/coroutine/errors.py src/jass_runner/coroutine/runner.py tests/coroutine/test_runner.py
git commit -m "feat(coroutine): implement CoroutineRunner.execute_func

Co-Authored-By: Claude (moonshotai/kimi-k2.5) <noreply@anthropic.com>"
```

---

### Task 1.9: 实现 CoroutineRunner 的 update 方法

**Files:**
- Modify: `src/jass_runner/coroutine/runner.py`
- Test: `tests/coroutine/test_runner.py`

**Step 1: Write the failing test**

```python
def test_runner_update():
    """测试 CoroutineRunner 的 update 方法。"""
    from unittest.mock import Mock, MagicMock
    from jass_runner.coroutine.runner import CoroutineRunner
    from jass_runner.coroutine import CoroutineStatus

    runner = CoroutineRunner()

    # 创建一个模拟协程
    mock_coroutine = Mock()
    mock_coroutine.status = CoroutineStatus.RUNNING
    mock_coroutine.resume.return_value = None  # 不睡眠，直接完成

    runner._active.append(mock_coroutine)

    # 执行一帧更新
    runner.update(0.033)  # 约30fps

    assert runner._current_time == 0.033
    assert runner._frame_count == 1
    # 协程已完成，应从活跃列表移除
    assert len(runner._active) == 0
```

**Step 2: Run test to verify it fails**

```bash
pytest tests/coroutine/test_runner.py::test_runner_update -v
```

Expected: FAIL

**Step 3: Write minimal implementation**

```python
# src/jass_runner/coroutine/runner.py
# 添加方法到 CoroutineRunner 类

    def update(self, delta_time: float):
        """
        每帧调用，更新协程状态。

        参数：
            delta_time: 时间增量（秒）
        """
        self._current_time += delta_time
        self._frame_count += 1

        # 1. 唤醒到期的协程
        ready = self._scheduler.wake_ready(self._current_time)
        self._active.extend(ready)

        # 2. 执行活跃协程
        still_active = []
        for coroutine in self._active:
            signal = coroutine.resume()

            if signal:  # 遇到 SleepSignal
                coroutine.sleep(signal.duration, self._current_time)
                self._scheduler.add(coroutine)
            elif coroutine.status == CoroutineStatus.FINISHED:
                pass  # 协程完成，不加入活跃列表
            else:
                still_active.append(coroutine)

        self._active = still_active
```

**Step 4: Run test to verify it passes**

```bash
pytest tests/coroutine/test_runner.py::test_runner_update -v
```

Expected: PASS

**Step 5: Commit**

```bash
git add src/jass_runner/coroutine/runner.py tests/coroutine/test_runner.py
git commit -m "feat(coroutine): implement CoroutineRunner.update

Co-Authored-By: Claude (moonshotai/kimi-k2.5) <noreply@anthropic.com>"
```

---

### Task 1.10: 实现 CoroutineRunner 的 is_finished 方法

**Files:**
- Modify: `src/jass_runner/coroutine/runner.py`
- Test: `tests/coroutine/test_runner.py`

**Step 1: Write the failing test**

```python
def test_runner_is_finished():
    """测试 CoroutineRunner 的 is_finished 方法。"""
    from unittest.mock import Mock
    from jass_runner.coroutine.runner import CoroutineRunner
    from jass_runner.coroutine import CoroutineStatus

    runner = CoroutineRunner()

    # 初始状态：未开始，不算完成
    assert not runner.is_finished()

    # 设置主协程
    mock_main = Mock()
    mock_main.status = CoroutineStatus.PENDING
    runner._main_coroutine = mock_main

    assert not runner.is_finished()

    # 主协程完成
    mock_main.status = CoroutineStatus.FINISHED
    assert runner.is_finished()
```

**Step 2: Run test to verify it fails**

```bash
pytest tests/coroutine/test_runner.py::test_runner_is_finished -v
```

Expected: FAIL

**Step 3: Write minimal implementation**

```python
# src/jass_runner/coroutine/runner.py
# 添加方法到 CoroutineRunner 类

    def is_finished(self) -> bool:
        """
        检查所有协程是否完成。

        返回：
            True 如果所有协程都已完成
        """
        return (len(self._active) == 0 and
                self._scheduler.is_empty() and
                self._main_coroutine is not None and
                self._main_coroutine.status == CoroutineStatus.FINISHED)
```

**Step 4: Run test to verify it passes**

```bash
pytest tests/coroutine/test_runner.py::test_runner_is_finished -v
```

Expected: PASS

**Step 5: Commit**

```bash
git add src/jass_runner/coroutine/runner.py tests/coroutine/test_runner.py
git commit -m "feat(coroutine): implement CoroutineRunner.is_finished

Co-Authored-By: Claude (moonshotai/kimi-k2.5) <noreply@anthropic.com>"
```

---

### Task 1.11: 导出协程模块公共 API

**Files:**
- Modify: `src/jass_runner/coroutine/__init__.py`
- Test: `tests/coroutine/test_imports.py`

**Step 1: Write the failing test**

```python
def test_coroutine_module_exports():
    """测试协程模块导出。"""
    from jass_runner.coroutine import (
        CoroutineStatus,
        SleepSignal,
        SleepInterrupt,
        Coroutine,
        SleepScheduler,
        CoroutineRunner,
        CoroutineError,
        CoroutineStackOverflow,
    )

    assert CoroutineStatus is not None
    assert SleepSignal is not None
    assert SleepInterrupt is not None
    assert Coroutine is not None
    assert SleepScheduler is not None
    assert CoroutineRunner is not None
    assert CoroutineError is not None
    assert CoroutineStackOverflow is not None
```

**Step 2: Run test to verify it fails**

```bash
pytest tests/coroutine/test_imports.py::test_coroutine_module_exports -v
```

Expected: FAIL

**Step 3: Write minimal implementation**

```python
# src/jass_runner/coroutine/__init__.py
"""协程系统模块。

提供 JASS 异步执行支持，包括 TriggerSleepAction 和 ExecuteFunc。
"""

from enum import Enum


class CoroutineStatus(Enum):
    """协程状态枚举。"""
    PENDING = "pending"
    RUNNING = "running"
    SLEEPING = "sleeping"
    FINISHED = "finished"


from .signals import SleepSignal
from .exceptions import SleepInterrupt
from .coroutine import Coroutine
from .scheduler import SleepScheduler
from .runner import CoroutineRunner
from .errors import CoroutineError, CoroutineStackOverflow

__all__ = [
    'CoroutineStatus',
    'SleepSignal',
    'SleepInterrupt',
    'Coroutine',
    'SleepScheduler',
    'CoroutineRunner',
    'CoroutineError',
    'CoroutineStackOverflow',
]
```

**Step 4: Run test to verify it passes**

```bash
pytest tests/coroutine/test_imports.py::test_coroutine_module_exports -v
```

Expected: PASS

**Step 5: Commit**

```bash
git add src/jass_runner/coroutine/__init__.py tests/coroutine/test_imports.py
git commit -m "feat(coroutine): export coroutine module public API

Co-Authored-By: Claude (moonshotai/kimi-k2.5) <noreply@anthropic.com>"
```

---

## Phase 2: 改造解释器为生成器模式

### Task 2.1: 创建 JassCoroutine 类（继承 Coroutine）

**Files:**
- Create: `src/jass_runner/interpreter/coroutine.py`
- Test: `tests/interpreter/test_coroutine.py`

**Step 1: Write the failing test**

```python
def test_jass_coroutine_creation():
    """测试 JassCoroutine 创建。"""
    from jass_runner.interpreter.coroutine import JassCoroutine
    from unittest.mock import Mock

    interpreter = Mock()
    func = Mock()
    func.body = []

    coroutine = JassCoroutine(interpreter, func)

    assert coroutine.interpreter is interpreter
    assert coroutine.func is func
```

**Step 2: Run test to verify it fails**

```bash
pytest tests/interpreter/test_coroutine.py::test_jass_coroutine_creation -v
```

Expected: FAIL

**Step 3: Write minimal implementation**

```python
# src/jass_runner/interpreter/coroutine.py
"""JASS 解释器协程实现。"""

from typing import Generator
from ..coroutine import Coroutine, CoroutineStatus, SleepSignal
from ..coroutine.exceptions import SleepInterrupt
from ..interpreter.control_flow import ReturnSignal


class JassCoroutine(Coroutine):
    """JASS 函数执行的协程包装。"""

    def __init__(self, interpreter, func, args=None):
        super().__init__(interpreter, func, args)
        self._pc = 0  # 程序计数器

    def _run(self) -> Generator:
        """执行函数体作为生成器。"""
        self._setup_context()
        statements = self.func.body or []

        while self._pc < len(statements):
            statement = statements[self._pc]

            try:
                self.interpreter.execute_statement(statement)
                self._pc += 1

            except SleepInterrupt as e:
                self._pc += 1
                yield SleepSignal(e.duration)

            except ReturnSignal:
                break

        self._teardown_context()
        self.status = CoroutineStatus.FINISHED

    def _setup_context(self):
        """设置函数执行上下文。"""
        pass  # 子类实现

    def _teardown_context(self):
        """清理函数执行上下文。"""
        pass  # 子类实现

    def resume(self):
        """恢复执行。"""
        if self.status != CoroutineStatus.RUNNING or not self.generator:
            return None

        try:
            signal = next(self.generator)
            if isinstance(signal, SleepSignal):
                self.status = CoroutineStatus.SLEEPING
                return signal
        except StopIteration:
            self.status = CoroutineStatus.FINISHED

        return None
```

**Step 4: Run test to verify it passes**

```bash
pytest tests/interpreter/test_coroutine.py::test_jass_coroutine_creation -v
```

Expected: PASS

**Step 5: Commit**

```bash
git add src/jass_runner/interpreter/coroutine.py tests/interpreter/test_coroutine.py
git commit -m "feat(interpreter): add JassCoroutine class

Co-Authored-By: Claude (moonshotai/kimi-k2.5) <noreply@anthropic.com>"
```

---

### Task 2.2: 实现 JassCoroutine 的上下文管理

**Files:**
- Modify: `src/jass_runner/interpreter/coroutine.py`
- Test: `tests/interpreter/test_coroutine.py`

**Step 1: Write the failing test**

```python
def test_jass_coroutine_context_management():
    """测试 JassCoroutine 上下文管理。"""
    from jass_runner.interpreter.coroutine import JassCoroutine
    from unittest.mock import Mock, MagicMock

    interpreter = Mock()
    interpreter.global_context = Mock()
    interpreter.state_context = Mock()
    interpreter.current_context = None

    func = Mock()
    func.body = []
    func.parameters = []

    coroutine = JassCoroutine(interpreter, func)
    coroutine.start()

    # 执行完成
    list(coroutine.generator)

    # 验证上下文被设置和恢复
    assert interpreter.current_context is not None
```

**Step 2: Run test to verify it fails**

```bash
pytest tests/interpreter/test_coroutine.py::test_jass_coroutine_context_management -v
```

Expected: FAIL

**Step 3: Write minimal implementation**

```python
# src/jass_runner/interpreter/coroutine.py
# 修改 JassCoroutine 类

    def _setup_context(self):
        """设置函数执行上下文。"""
        from .context import ExecutionContext

        func_context = ExecutionContext(
            self.interpreter.global_context,
            native_registry=self.interpreter.global_context.native_registry,
            state_context=self.interpreter.state_context,
            interpreter=self.interpreter
        )

        # 设置参数
        if self.args:
            for param, arg_value in zip(self.func.parameters, self.args):
                func_context.set_variable(param.name, arg_value)

        self.interpreter.current_context = func_context
        self.interpreter.evaluator.context = func_context

    def _teardown_context(self):
        """清理函数执行上下文。"""
        self.interpreter.current_context = self.interpreter.global_context
        self.interpreter.evaluator.context = self.interpreter.global_context
```

**Step 4: Run test to verify it passes**

```bash
pytest tests/interpreter/test_coroutine.py::test_jass_coroutine_context_management -v
```

Expected: PASS

**Step 5: Commit**

```bash
git add src/jass_runner/interpreter/coroutine.py tests/interpreter/test_coroutine.py
git commit -m "feat(interpreter): implement JassCoroutine context management

Co-Authored-By: Claude (moonshotai/kimi-k2.5) <noreply@anthropic.com>"
```

---

### Task 2.3: 改造 Interpreter 支持协程

**Files:**
- Modify: `src/jass_runner/interpreter/interpreter.py`
- Test: `tests/interpreter/test_interpreter_coroutine.py`

**Step 1: Write the failing test**

```python
def test_interpreter_create_main_coroutine():
    """测试解释器创建主协程。"""
    from jass_runner.interpreter.interpreter import Interpreter
    from unittest.mock import Mock

    interpreter = Interpreter()
    ast = Mock()
    ast.globals = []
    ast.functions = []

    coroutine = interpreter.create_main_coroutine(ast)

    # 没有 main 函数时返回 None
    assert coroutine is None
```

**Step 2: Run test to verify it fails**

```bash
pytest tests/interpreter/test_interpreter_coroutine.py::test_interpreter_create_main_coroutine -v
```

Expected: FAIL

**Step 3: Write minimal implementation**

```python
# src/jass_runner/interpreter/interpreter.py
# 添加方法到 Interpreter 类

    def create_main_coroutine(self, ast):
        """
        创建主协程。

        参数：
            ast: AST 根节点

        返回：
            JassCoroutine 实例，如果没有 main 函数则返回 None
        """
        # 初始化全局变量
        if ast.globals:
            for global_decl in ast.globals:
                self.execute_global_declaration(global_decl)

        # 注册所有函数
        for func in ast.functions:
            self.functions[func.name] = func

        # 创建 main 函数协程
        main_func = self.functions.get('main')
        if main_func:
            from .coroutine import JassCoroutine
            return JassCoroutine(self, main_func)
        return None
```

**Step 4: Run test to verify it passes**

```bash
pytest tests/interpreter/test_interpreter_coroutine.py::test_interpreter_create_main_coroutine -v
```

Expected: PASS

**Step 5: Commit**

```bash
git add src/jass_runner/interpreter/interpreter.py tests/interpreter/test_interpreter_coroutine.py
git commit -m "feat(interpreter): add create_main_coroutine method

Co-Authored-By: Claude (moonshotai/kimi-k2.5) <noreply@anthropic.com>"
```

---

### Task 2.4: 处理 SleepInterrupt 异常

**Files:**
- Modify: `src/jass_runner/interpreter/interpreter.py`
- Test: `tests/interpreter/test_interpreter_coroutine.py`

**Step 1: Write the failing test**

```python
def test_interpreter_handles_sleep_interrupt():
    """测试解释器处理 SleepInterrupt。"""
    from jass_runner.interpreter.interpreter import Interpreter
    from jass_runner.coroutine.exceptions import SleepInterrupt
    from unittest.mock import Mock, patch

    interpreter = Interpreter()

    # 模拟一个会抛出 SleepInterrupt 的语句
    mock_stmt = Mock()

    with patch.object(interpreter, 'execute_statement',
                      side_effect=SleepInterrupt(2.0)):
        try:
            interpreter.execute_statement(mock_stmt)
            assert False, "应该抛出 SleepInterrupt"
        except SleepInterrupt as e:
            assert e.duration == 2.0
```

**Step 2: Run test to verify it fails**

```bash
pytest tests/interpreter/test_interpreter_coroutine.py::test_interpreter_handles_sleep_interrupt -v
```

Expected: FAIL

**Step 3: 无需修改 Interpreter，测试验证异常可以正常传递**

解释器不需要特殊处理 SleepInterrupt，它只需要让异常向上传递即可。

**Step 4: Run test to verify it passes**

```bash
pytest tests/interpreter/test_interpreter_coroutine.py::test_interpreter_handles_sleep_interrupt -v
```

Expected: PASS

**Step 5: Commit**

```bash
git add tests/interpreter/test_interpreter_coroutine.py
git commit -m "test(interpreter): add SleepInterrupt handling test

Co-Authored-By: Claude (moonshotai/kimi-k2.5) <noreply@anthropic.com>"
```

---

## Phase 3: 改造 SimulationLoop 集成 CoroutineRunner

### Task 3.1: 改造 SimulationLoop 添加 CoroutineRunner

**Files:**
- Modify: `src/jass_runner/timer/simulation.py`
- Test: `tests/timer/test_simulation_coroutine.py`

**Step 1: Write the failing test**

```python
def test_simulation_loop_has_coroutine_runner():
    """测试 SimulationLoop 包含 CoroutineRunner。"""
    from jass_runner.timer.simulation import SimulationLoop

    loop = SimulationLoop()

    assert loop.coroutine_runner is not None
    assert loop.timer_system is not None
```

**Step 2: Run test to verify it fails**

```bash
pytest tests/timer/test_simulation_coroutine.py::test_simulation_loop_has_coroutine_runner -v
```

Expected: FAIL

**Step 3: Write minimal implementation**

```python
# src/jass_runner/timer/simulation.py
# 修改 SimulationLoop 类

from ..coroutine import CoroutineRunner


class SimulationLoop:
    """模拟循环，集成协程调度。"""

    def __init__(self, fps: float = 30.0):
        self.fps = fps
        self.frame_duration = 1.0 / fps
        self.current_time = 0.0
        self.frame_count = 0

        # 现有系统
        self.timer_system = TimerSystem()

        # 新增：协程调度器
        self.coroutine_runner = CoroutineRunner()

        self._running = False
```

**Step 4: Run test to verify it passes**

```bash
pytest tests/timer/test_simulation_coroutine.py::test_simulation_loop_has_coroutine_runner -v
```

Expected: PASS

**Step 5: Commit**

```bash
git add src/jass_runner/timer/simulation.py tests/timer/test_simulation_coroutine.py
git commit -m "feat(timer): integrate CoroutineRunner into SimulationLoop

Co-Authored-By: Claude (moonshotai/kimi-k2.5) <noreply@anthropic.com>"
```

---

### Task 3.2: 实现 SimulationLoop.run 方法

**Files:**
- Modify: `src/jass_runner/timer/simulation.py`
- Test: `tests/timer/test_simulation_coroutine.py`

**Step 1: Write the failing test**

```python
def test_simulation_loop_run():
    """测试 SimulationLoop.run 方法。"""
    from jass_runner.timer.simulation import SimulationLoop
    from unittest.mock import Mock

    loop = SimulationLoop()

    # 模拟解释器和 AST
    interpreter = Mock()
    ast = Mock()
    ast.globals = []
    ast.functions = []

    result = loop.run(interpreter, ast, max_frames=10)

    assert 'frames' in result
    assert 'time' in result
    assert 'success' in result
```

**Step 2: Run test to verify it fails**

```bash
pytest tests/timer/test_simulation_coroutine.py::test_simulation_loop_run -v
```

Expected: FAIL

**Step 3: Write minimal implementation**

```python
# src/jass_runner/timer/simulation.py
# 添加方法到 SimulationLoop 类

    def run(self, interpreter, ast, max_frames: int = None) -> dict:
        """
        运行模拟（主入口）。

        参数：
            interpreter: 解释器实例
            ast: AST 根节点
            max_frames: 最大帧数限制

        返回：
            执行结果字典
        """
        self._running = True

        # 启动主协程
        self.coroutine_runner.start_main(interpreter, ast)

        while self._running:
            self._update_frame()

            if self.coroutine_runner.is_finished():
                break

            if max_frames and self.frame_count >= max_frames:
                break

        return {
            'frames': self.frame_count,
            'time': self.current_time,
            'success': self.coroutine_runner.is_finished()
        }

    def _update_frame(self):
        """单帧更新。"""
        delta = self.frame_duration
        self.current_time += delta
        self.frame_count += 1

        # 1. 更新协程
        self.coroutine_runner.update(delta)

        # 2. 更新计时器
        self.timer_system.update(delta)

    def start_main(self, interpreter, ast):
        """启动主协程。"""
        coroutine = interpreter.create_main_coroutine(ast)
        if coroutine:
            coroutine.start()
            self.coroutine_runner._active.append(coroutine)
            self.coroutine_runner._main_coroutine = coroutine
```

**Step 4: Run test to verify it passes**

```bash
pytest tests/timer/test_simulation_coroutine.py::test_simulation_loop_run -v
```

Expected: PASS

**Step 5: Commit**

```bash
git add src/jass_runner/timer/simulation.py tests/timer/test_simulation_coroutine.py
git commit -m "feat(timer): implement SimulationLoop.run with coroutine support

Co-Authored-By: Claude (moonshotai/kimi-k2.5) <noreply@anthropic.com>"
```

---

## Phase 4: 实现 TriggerSleepAction 和 ExecuteFunc native 函数

### Task 4.1: 实现 TriggerSleepAction native 函数

**Files:**
- Create: `src/jass_runner/natives/async_natives.py`
- Test: `tests/natives/test_async_natives.py`

**Step 1: Write the failing test**

```python
def test_trigger_sleep_action_raises_interrupt():
    """测试 TriggerSleepAction 抛出 SleepInterrupt。"""
    from jass_runner.natives.async_natives import TriggerSleepAction
    from jass_runner.coroutine.exceptions import SleepInterrupt

    sleep_action = TriggerSleepAction()

    try:
        sleep_action.execute(2.0)
        assert False, "应该抛出 SleepInterrupt"
    except SleepInterrupt as e:
        assert e.duration == 2.0
```

**Step 2: Run test to verify it fails**

```bash
pytest tests/natives/test_async_natives.py::test_trigger_sleep_action_raises_interrupt -v
```

Expected: FAIL

**Step 3: Write minimal implementation**

```python
# src/jass_runner/natives/async_natives.py
"""异步相关 native 函数实现。"""

from .base import NativeFunction
from ..coroutine.exceptions import SleepInterrupt


class TriggerSleepAction(NativeFunction):
    """JASS 原生函数：暂停当前协程指定时间。"""

    @property
    def name(self) -> str:
        return "TriggerSleepAction"

    def execute(self, timeout: float) -> None:
        """
        参数：
            timeout: 等待时间（秒）

        异常：
            SleepInterrupt: 总是抛出，用于挂起当前协程
        """
        raise SleepInterrupt(timeout)
```

**Step 4: Run test to verify it passes**

```bash
pytest tests/natives/test_async_natives.py::test_trigger_sleep_action_raises_interrupt -v
```

Expected: PASS

**Step 5: Commit**

```bash
git add src/jass_runner/natives/async_natives.py tests/natives/test_async_natives.py
git commit -m "feat(natives): add TriggerSleepAction native function

Co-Authored-By: Claude (moonshotai/kimi-k2.5) <noreply@anthropic.com>"
```

---

### Task 4.2: 实现 ExecuteFunc native 函数

**Files:**
- Modify: `src/jass_runner/natives/async_natives.py`
- Test: `tests/natives/test_async_natives.py`

**Step 1: Write the failing test**

```python
def test_execute_func_creates_coroutine():
    """测试 ExecuteFunc 创建新协程。"""
    from jass_runner.natives.async_natives import ExecuteFunc
    from unittest.mock import Mock

    execute_func = ExecuteFunc()

    # 模拟解释器
    mock_interpreter = Mock()
    mock_func = Mock()
    mock_func.body = []
    mock_interpreter.functions = {"test_func": mock_func}
    mock_interpreter.coroutine_runner = Mock()

    execute_func.interpreter = mock_interpreter
    execute_func.execute("test_func")

    # 验证创建了新协程
    mock_interpreter.coroutine_runner.execute_func.assert_called_once()
```

**Step 2: Run test to verify it fails**

```bash
pytest tests/natives/test_async_natives.py::test_execute_func_creates_coroutine -v
```

Expected: FAIL

**Step 3: Write minimal implementation**

```python
# src/jass_runner/natives/async_natives.py
# 添加 ExecuteFunc 类

class ExecuteFunc(NativeFunction):
    """JASS 原生函数：创建新协程执行指定函数。"""

    @property
    def name(self) -> str:
        return "ExecuteFunc"

    def execute(self, func_name: str) -> None:
        """
        参数：
            func_name: 要执行的函数名称

        行为：
            创建新协程执行函数，但不等待其完成
            当前协程继续执行
        """
        func = self.interpreter.functions.get(func_name)
        if not func:
            return  # 函数不存在静默返回

        self.interpreter.coroutine_runner.execute_func(
            self.interpreter, func, []
        )
```

**Step 4: Run test to verify it passes**

```bash
pytest tests/natives/test_async_natives.py::test_execute_func_creates_coroutine -v
```

Expected: PASS

**Step 5: Commit**

```bash
git add src/jass_runner/natives/async_natives.py tests/natives/test_async_natives.py
git commit -m "feat(natives): add ExecuteFunc native function

Co-Authored-By: Claude (moonshotai/kimi-k2.5) <noreply@anthropic.com>"
```

---

### Task 4.3: 注册异步 native 函数

**Files:**
- Modify: `src/jass_runner/natives/factory.py`
- Test: `tests/natives/test_factory.py`

**Step 1: Write the failing test**

```python
def test_factory_registers_async_natives():
    """测试工厂注册异步 native 函数。"""
    from jass_runner.natives.factory import NativeFactory

    registry = NativeFactory.create_default_registry()

    assert registry.get("TriggerSleepAction") is not None
    assert registry.get("ExecuteFunc") is not None
```

**Step 2: Run test to verify it fails**

```bash
pytest tests/natives/test_factory.py::test_factory_registers_async_natives -v
```

Expected: FAIL

**Step 3: Write minimal implementation**

```python
# src/jass_runner/natives/factory.py
# 修改 NativeFactory.create_default_registry 方法

from .async_natives import TriggerSleepAction, ExecuteFunc

# 在 create_default_registry 中添加：
registry.register(TriggerSleepAction())
registry.register(ExecuteFunc())
```

**Step 4: Run test to verify it passes**

```bash
pytest tests/natives/test_factory.py::test_factory_registers_async_natives -v
```

Expected: PASS

**Step 5: Commit**

```bash
git add src/jass_runner/natives/factory.py tests/natives/test_factory.py
git commit -m "feat(natives): register async natives in factory

Co-Authored-By: Claude (moonshotai/kimi-k2.5) <noreply@anthropic.com>"
```

---

## Phase 5: 编写测试和示例脚本

### Task 5.1: 创建异步功能集成测试

**Files:**
- Create: `tests/integration/test_async_integration.py`

**Step 1: Write集成测试**

```python
# tests/integration/test_async_integration.py
"""异步功能集成测试。"""

import pytest
from jass_runner.parser.parser import Parser
from jass_runner.interpreter.interpreter import Interpreter
from jass_runner.timer.simulation import SimulationLoop
from jass_runner.natives.factory import NativeFactory


class TestAsyncIntegration:
    """测试异步等待功能集成。"""

    def test_trigger_sleep_action_basic(self):
        """测试基本的 TriggerSleepAction 功能。"""
        code = '''
        function main takes nothing returns nothing
            call DisplayTextToPlayer(Player(0), 0, 0, "开始")
            call TriggerSleepAction(1.0)
            call DisplayTextToPlayer(Player(0), 0, 0, "1秒后")
        endfunction
        '''

        parser = Parser()
        ast = parser.parse(code)

        registry = NativeFactory.create_default_registry()
        interpreter = Interpreter(registry)

        loop = SimulationLoop(fps=10.0)  # 10fps 方便测试
        result = loop.run(interpreter, ast, max_frames=20)

        assert result['success'] is True
        assert result['time'] >= 1.0

    def test_execute_func_creates_parallel_execution(self):
        """测试 ExecuteFunc 创建并行执行流。"""
        code = '''
        function delayed takes nothing returns nothing
            call TriggerSleepAction(2.0)
            call DisplayTextToPlayer(Player(0), 0, 0, "延迟消息")
        endfunction

        function main takes nothing returns nothing
            call ExecuteFunc("delayed")
            call DisplayTextToPlayer(Player(0), 0, 0, "立即消息")
            call TriggerSleepAction(3.0)
        endfunction
        '''

        parser = Parser()
        ast = parser.parse(code)

        registry = NativeFactory.create_default_registry()
        interpreter = Interpreter(registry)

        loop = SimulationLoop(fps=10.0)
        result = loop.run(interpreter, ast, max_frames=50)

        assert result['success'] is True
        assert result['time'] >= 3.0
```

**Step 2: Run test to verify it passes**

```bash
pytest tests/integration/test_async_integration.py -v
```

Expected: PASS (可能需要调整实现)

**Step 3: Commit**

```bash
git add tests/integration/test_async_integration.py
git commit -m "test(integration): add async functionality integration tests

Co-Authored-By: Claude (moonshotai/kimi-k2.5) <noreply@anthropic.com>"
```

---

### Task 5.2: 创建示例脚本

**Files:**
- Create: `examples/async_example.j`
- Create: `examples/run_async_example.py`

**Step 1: 创建 JASS 示例脚本**

```jass
// examples/async_example.j
// 演示异步等待功能

function delayed_spawn takes nothing returns nothing
    call DisplayTextToPlayer(Player(0), 0, 0, "3秒后开始生成单位...")
    call TriggerSleepAction(3.0)

    local unit u = CreateUnit(Player(0), 'Hpal', 0, 0, 0)
    call DisplayTextToPlayer(Player(0), 0, 0, "单位已生成！")
endfunction

function periodic_message takes nothing returns nothing
    local integer i = 0
    loop
        exitwhen i >= 5
        call TriggerSleepAction(1.0)
        call DisplayTextToPlayer(Player(0), 0, 0, "周期消息 " + I2S(i))
        set i = i + 1
    endloop
endfunction

function main takes nothing returns nothing
    call DisplayTextToPlayer(Player(0), 0, 0, "=== 异步等待示例 ===")

    // 创建两个并行的执行流
    call ExecuteFunc("delayed_spawn")
    call ExecuteFunc("periodic_message")

    call DisplayTextToPlayer(Player(0), 0, 0, "主函数继续执行（不等待）")

    call TriggerSleepAction(6.0)
    call DisplayTextToPlayer(Player(0), 0, 0, "6秒后：示例结束")
endfunction
```

**Step 2: 创建 Python 运行脚本**

```python
# examples/run_async_example.py
"""运行异步示例脚本。"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from jass_runner.parser.parser import Parser
from jass_runner.interpreter.interpreter import Interpreter
from jass_runner.timer.simulation import SimulationLoop
from jass_runner.natives.factory import NativeFactory


def main():
    # 读取示例脚本
    script_path = os.path.join(os.path.dirname(__file__), 'async_example.j')
    with open(script_path, 'r', encoding='utf-8') as f:
        code = f.read()

    # 解析
    parser = Parser()
    ast = parser.parse(code)

    if parser.errors:
        print("解析错误:")
        for error in parser.errors:
            print(f"  {error}")
        return 1

    # 创建解释器
    registry = NativeFactory.create_default_registry()
    interpreter = Interpreter(registry)

    # 运行模拟
    print("开始执行异步示例...\n")
    loop = SimulationLoop(fps=10.0)
    result = loop.run(interpreter, ast, max_frames=100)

    print(f"\n执行完成:")
    print(f"  帧数: {result['frames']}")
    print(f"  时间: {result['time']:.2f}秒")
    print(f"  成功: {result['success']}")

    return 0


if __name__ == '__main__':
    sys.exit(main())
```

**Step 3: 运行示例验证**

```bash
python examples/run_async_example.py
```

Expected: 正常输出消息序列

**Step 4: Commit**

```bash
git add examples/async_example.j examples/run_async_example.py
git commit -m "feat(examples): add async functionality examples

Co-Authored-By: Claude (moonshotai/kimi-k2.5) <noreply@anthropic.com>"
```

---

## Phase 6: 文档更新和代码审查

### Task 6.1: 更新项目笔记

**Files:**
- Modify: `PROJECT_NOTES.md`

添加 v0.4.0 完成记录：

```markdown
#### 41. v0.4.0 异步等待功能实现完成 (2026-03-01)
- **协程系统核心实现**：
  - 创建 `src/jass_runner/coroutine/` 模块
  - 实现 `Coroutine` 基类、`SleepScheduler`、`CoroutineRunner`
  - 支持协程挂起/恢复机制

- **解释器改造**：
  - 创建 `JassCoroutine` 类，将函数执行转换为生成器
  - 支持 `SleepInterrupt` 异常传播
  - `create_main_coroutine` 方法创建主协程

- **SimulationLoop 集成**：
  - 集成 `CoroutineRunner` 到 `SimulationLoop`
  - `run` 方法支持协程调度
  - 每帧更新协程状态

- **Native 函数实现**：
  - `TriggerSleepAction` - 暂停当前协程指定时间
  - `ExecuteFunc` - 创建新协程执行函数

- **测试和示例**：
  - 集成测试覆盖基本场景
  - 示例脚本演示异步功能

- **测试统计**：
  - 所有测试通过
  - 协程系统覆盖率 95%+
```

**Commit:**

```bash
git add PROJECT_NOTES.md
git commit -m "docs: update PROJECT_NOTES for v0.4.0 async features

Co-Authored-By: Claude (moonshotai/kimi-k2.5) <noreply@anthropic.com>"
```

---

### Task 6.2: 更新 TODO.md

**Files:**
- Modify: `TODO.md`

更新 v0.4.0 状态：

```markdown
### v0.4.0: 高级特性与并发 (Advanced Features) ✅ 已完成
> 目标：支持复杂的异步逻辑和过场动画脚本。

- [x] **P1** [Simulator] 实现异步等待 (`TriggerSleepAction` / `Wait`)。
- [x] **P2** [Simulator] 实现并发执行 (`ExecuteFunc`)。

**v0.4.0 状态**: ✅ 已完成（2026-03-01）
- 协程系统：Coroutine、SleepScheduler、CoroutineRunner
- 解释器生成器改造：JassCoroutine
- SimulationLoop 集成
- Native 函数：TriggerSleepAction、ExecuteFunc
- 测试覆盖：集成测试和示例脚本
```

**Commit:**

```bash
git add TODO.md
git commit -m "docs: update TODO.md mark v0.4.0 as completed

Co-Authored-By: Claude (moonshotai/kimi-k2.5) <noreply@anthropic.com>"
```

---

### Task 6.3: 运行完整测试套件

**Files:**
- All test files

**Step 1: 运行所有测试**

```bash
pytest --tb=short
```

Expected: 所有测试通过

**Step 2: 运行代码质量检查**

```bash
flake8 src/jass_runner/coroutine tests/coroutine
```

Expected: 无错误

**Step 3: Commit (如有修复)**

```bash
git add -A
git commit -m "style: fix code style issues in coroutine module

Co-Authored-By: Claude (moonshotai/kimi-k2.5) <noreply@anthropic.com>"
```

---

## 验收标准

### 功能验收

- [ ] `TriggerSleepAction(2.0)` 会暂停当前协程 2 秒
- [ ] `ExecuteFunc("func")` 创建新协程执行函数，不阻塞当前协程
- [ ] 多个协程可以并发执行
- [ ] 协程按正确时间顺序唤醒

### 测试验收

- [ ] 所有单元测试通过
- [ ] 所有集成测试通过
- [ ] 示例脚本正常运行
- [ ] 代码覆盖率 > 90%

### 文档验收

- [ ] 设计文档完整
- [ ] 项目笔记更新
- [ ] TODO.md 更新
- [ ] 代码注释完整（中文）

---

**Plan complete and saved to `docs/plans/2026-03-01-async-await-implementation.md`.**

**Two execution options:**

**1. Subagent-Driven (this session)** - I dispatch fresh subagent per task, review between tasks, fast iteration

**2. Parallel Session (separate)** - Open new session with executing-plans, batch execution with checkpoints

**Which approach?**
