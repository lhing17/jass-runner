# GameState 事件系统实现计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 实现 `TriggerRegisterGameStateEvent` native 函数及相关类型支持，支持 `GAME_STATE_TIME_OF_DAY` 状态监控和日夜循环系统。

**Architecture:** 基于现有 Trigger 系统扩展，添加 LimitOp 类型、GameState 类型、GameStateManager 管理器，与 TimerSystem 集成实现每帧更新和事件触发。

**Tech Stack:** Python 3.8+, pytest, 现有 JASS Runner 框架

---

## 前置知识

### 相关文件位置
- `src/jass_runner/types/` - 类型定义目录
- `src/jass_runner/trigger/` - 触发器系统目录
- `src/jass_runner/natives/` - native 函数目录
- `src/jass_runner/natives/factory.py` - native 函数注册工厂
- `docs/plans/2026-03-05-gamestate-event-system-design.md` - 详细设计文档

### 现有代码参考
- `src/jass_runner/trigger/event_types.py` - 事件类型定义模式
- `src/jass_runner/natives/trigger_register_event_natives.py` - 事件注册 native 函数实现模式
- `src/jass_runner/natives/state.py` - StateContext 定义

---

## Task 1: 创建 LimitOp 类型定义

**Files:**
- Create: `src/jass_runner/types/limitop.py`
- Test: `tests/types/test_limitop.py`

**Step 1: 编写失败测试**

```python
"""LimitOp 类型测试。"""

import pytest
from jass_runner.types.limitop import LimitOp


class TestLimitOp:
    """测试 LimitOp 类型。"""

    def test_less_than_constant(self):
        """测试 LESS_THAN 常量值。"""
        assert LimitOp.LESS_THAN == 0

    def test_less_than_or_equal_constant(self):
        """测试 LESS_THAN_OR_EQUAL 常量值。"""
        assert LimitOp.LESS_THAN_OR_EQUAL == 1

    def test_equal_constant(self):
        """测试 EQUAL 常量值。"""
        assert LimitOp.EQUAL == 2

    def test_greater_than_or_equal_constant(self):
        """测试 GREATER_THAN_OR_EQUAL 常量值。"""
        assert LimitOp.GREATER_THAN_OR_EQUAL == 3

    def test_greater_than_constant(self):
        """测试 GREATER_THAN 常量值。"""
        assert LimitOp.GREATER_THAN == 4

    def test_not_equal_constant(self):
        """测试 NOT_EQUAL 常量值。"""
        assert LimitOp.NOT_EQUAL == 5

    def test_compare_less_than_true(self):
        """测试小于比较返回 True。"""
        assert LimitOp.compare(LimitOp.LESS_THAN, 1.0, 2.0) is True

    def test_compare_less_than_false(self):
        """测试小于比较返回 False。"""
        assert LimitOp.compare(LimitOp.LESS_THAN, 2.0, 1.0) is False

    def test_compare_equal_true(self):
        """测试等于比较返回 True。"""
        assert LimitOp.compare(LimitOp.EQUAL, 5.0, 5.0) is True

    def test_compare_equal_with_epsilon(self):
        """测试等于比较使用 epsilon 容差。"""
        assert LimitOp.compare(LimitOp.EQUAL, 5.0001, 5.0) is True
        assert LimitOp.compare(LimitOp.EQUAL, 5.1, 5.0) is False

    def test_compare_greater_than_true(self):
        """测试大于比较返回 True。"""
        assert LimitOp.compare(LimitOp.GREATER_THAN, 3.0, 2.0) is True

    def test_compare_not_equal_true(self):
        """测试不等于比较返回 True。"""
        assert LimitOp.compare(LimitOp.NOT_EQUAL, 1.0, 2.0) is True

    def test_compare_not_equal_false(self):
        """测试不等于比较返回 False。"""
        assert LimitOp.compare(LimitOp.NOT_EQUAL, 5.0, 5.0) is False

    def test_compare_invalid_opcode(self):
        """测试无效操作码返回 False。"""
        assert LimitOp.compare(99, 1.0, 2.0) is False
```

**Step 2: 运行测试验证失败**

Run: `pytest tests/types/test_limitop.py -v`
Expected: FAIL with "ModuleNotFoundError: No module named 'jass_runner.types.limitop'"

**Step 3: 编写最小实现**

```python
"""LimitOp 类型定义。

此模块定义 JASS limitop 类型和比较操作符常量。
"""


class LimitOp:
    """比较操作符类型。

    定义 JASS 中用于条件比较的操作符常量。
    """

    LESS_THAN = 0
    LESS_THAN_OR_EQUAL = 1
    EQUAL = 2
    GREATER_THAN_OR_EQUAL = 3
    GREATER_THAN = 4
    NOT_EQUAL = 5

    # 浮点数比较的 epsilon 容差
    _EPSILON = 0.001

    @staticmethod
    def compare(opcode: int, actual: float, target: float) -> bool:
        """根据操作码执行比较。

        参数：
            opcode: 比较操作符代码 (LimitOp.LESS_THAN 等)
            actual: 实际值
            target: 目标值

        返回：
            比较结果，如果条件满足返回 True
        """
        if opcode == LimitOp.LESS_THAN:
            return actual < target
        elif opcode == LimitOp.LESS_THAN_OR_EQUAL:
            return actual <= target
        elif opcode == LimitOp.EQUAL:
            return abs(actual - target) < LimitOp._EPSILON
        elif opcode == LimitOp.GREATER_THAN_OR_EQUAL:
            return actual >= target
        elif opcode == LimitOp.GREATER_THAN:
            return actual > target
        elif opcode == LimitOp.NOT_EQUAL:
            return abs(actual - target) >= LimitOp._EPSILON
        else:
            return False
```

**Step 4: 运行测试验证通过**

Run: `pytest tests/types/test_limitop.py -v`
Expected: PASS (12 tests)

**Step 5: 提交**

```bash
git add tests/types/test_limitop.py src/jass_runner/types/limitop.py
git commit -m "$(cat <<'EOF'
feat(types): 添加 LimitOp 类型定义

实现 limitop 类型和比较操作符常量，支持 LESS_THAN、EQUAL、
GREATER_THAN 等6种比较操作，使用 epsilon 容差处理浮点数比较。

Co-Authored-By: Claude (kimi-k2.5) <noreply@anthropic.com>
EOF
)"
```

---

## Task 2: 创建 GameState 类型定义

**Files:**
- Create: `src/jass_runner/types/gamestate.py`
- Test: `tests/types/test_gamestate.py`

**Step 1: 编写失败测试**

```python
"""GameState 类型测试。"""

import pytest
from jass_runner.types.gamestate import IGameState, FGameState


class TestIGameState:
    """测试 IGameState 类型。"""

    def test_divine_intervention_constant(self):
        """测试 DIVINE_INTERVENTION 常量值。"""
        assert IGameState.DIVINE_INTERVENTION == 0

    def test_disconnected_constant(self):
        """测试 DISCONNECTED 常量值。"""
        assert IGameState.DISCONNECTED == 1


class TestFGameState:
    """测试 FGameState 类型。"""

    def test_time_of_day_constant(self):
        """测试 TIME_OF_DAY 常量值。"""
        assert FGameState.TIME_OF_DAY == 2
```

**Step 2: 运行测试验证失败**

Run: `pytest tests/types/test_gamestate.py -v`
Expected: FAIL with "ModuleNotFoundError"

**Step 3: 编写最小实现**

```python
"""GameState 类型定义。

此模块定义 JASS gamestate 类型和常量。
"""


class IGameState:
    """整数类型游戏状态。

    用于表示整数值的游戏状态。
    """

    DIVINE_INTERVENTION = 0
    DISCONNECTED = 1


class FGameState:
    """浮点类型游戏状态。

    用于表示浮点数值的游戏状态。
    """

    TIME_OF_DAY = 2
```

**Step 4: 运行测试验证通过**

Run: `pytest tests/types/test_gamestate.py -v`
Expected: PASS (3 tests)

**Step 5: 提交**

```bash
git add tests/types/test_gamestate.py src/jass_runner/types/gamestate.py
git commit -m "$(cat <<'EOF'
feat(types): 添加 GameState 类型定义

实现 igamestate 和 fgamestate 类型常量，
包含 DIVINE_INTERVENTION、DISCONNECTED 和 TIME_OF_DAY。

Co-Authored-By: Claude (kimi-k2.5) <noreply@anthropic.com>
EOF
)"
```

---

## Task 3: 创建 GameStateManager

**Files:**
- Create: `src/jass_runner/gamestate/__init__.py`
- Create: `src/jass_runner/gamestate/manager.py`
- Test: `tests/gamestate/test_manager.py`

**Step 1: 编写失败测试**

```python
"""GameStateManager 测试。"""

import pytest
from unittest.mock import Mock, MagicMock

from jass_runner.gamestate.manager import GameStateManager
from jass_runner.types.gamestate import FGameState
from jass_runner.types.limitop import LimitOp


class TestGameStateManager:
    """测试 GameStateManager 功能。"""

    def test_initial_time_of_day(self):
        """测试初始时间为 0。"""
        mock_trigger_manager = Mock()
        manager = GameStateManager(mock_trigger_manager)
        assert manager.get_float_state(FGameState.TIME_OF_DAY) == 0.0

    def test_update_increases_time(self):
        """测试更新增加时间。"""
        mock_trigger_manager = Mock()
        manager = GameStateManager(mock_trigger_manager)

        # 更新一帧
        manager.update(1)
        time = manager.get_float_state(FGameState.TIME_OF_DAY)
        assert time > 0.0

    def test_time_cycles_every_9000_frames(self):
        """测试时间每 9000 帧循环一次。"""
        mock_trigger_manager = Mock()
        manager = GameStateManager(mock_trigger_manager)

        # 更新 9000 帧（一个完整周期）
        manager.update(9000)
        time_after_cycle = manager.get_float_state(FGameState.TIME_OF_DAY)

        # 应该接近 0（24小时后回到起点）
        assert time_after_cycle < 1.0

    def test_time_reaches_24_hours(self):
        """测试时间达到 24 小时。"""
        mock_trigger_manager = Mock()
        manager = GameStateManager(mock_trigger_manager)

        # 更新 4500 帧（半天）
        manager.update(4500)
        time = manager.get_float_state(FGameState.TIME_OF_DAY)

        # 应该接近 12（中午）
        assert 11.0 < time < 13.0

    def test_register_state_listener(self):
        """测试注册状态监听器。"""
        mock_trigger_manager = Mock()
        manager = GameStateManager(mock_trigger_manager)

        handle = manager.register_state_listener(
            "trigger_001",
            FGameState.TIME_OF_DAY,
            LimitOp.EQUAL,
            6.0
        )

        assert handle is not None
        assert isinstance(handle, str)

    def test_check_listeners_triggers_event(self):
        """测试监听器检查触发事件。"""
        mock_trigger_manager = Mock()
        manager = GameStateManager(mock_trigger_manager)

        # 注册一个监听器，在时间为 6.0 时触发
        manager.register_state_listener(
            "trigger_001",
            FGameState.TIME_OF_DAY,
            LimitOp.EQUAL,
            6.0
        )

        # 设置时间刚好为 6.0（模拟）
        manager._time_of_day = 6.0
        manager._check_state_listeners()

        # 验证触发事件
        mock_trigger_manager.fire_event.assert_called_once()

    def test_get_unknown_float_state_returns_zero(self):
        """测试获取未知浮点状态返回 0。"""
        mock_trigger_manager = Mock()
        manager = GameStateManager(mock_trigger_manager)

        result = manager.get_float_state(999)
        assert result == 0.0
```

**Step 2: 运行测试验证失败**

Run: `pytest tests/gamestate/test_manager.py -v`
Expected: FAIL with "ModuleNotFoundError"

**Step 3: 编写最小实现**

```python
"""GameStateManager 实现。

此模块包含游戏状态管理器，负责管理游戏状态值和日夜循环。
"""

from typing import Dict, List, Optional, Any
import logging

from jass_runner.types.gamestate import FGameState
from jass_runner.types.limitop import LimitOp

logger = logging.getLogger(__name__)


class GameStateManager:
    """游戏状态管理器。

    管理所有游戏状态的当前值，实现日夜循环逻辑，
    并在状态满足条件时触发事件。
    """

    # 5分钟 = 9000帧 (30fps)
    CYCLE_FRAMES = 9000

    def __init__(self, trigger_manager):
        """初始化游戏状态管理器。

        参数：
            trigger_manager: 触发器管理器实例
        """
        self._trigger_manager = trigger_manager
        self._float_states: Dict[int, float] = {}
        self._int_states: Dict[int, int] = {}
        self._time_of_day: float = 0.0  # 0.0 - 24.0
        self._frame_counter: int = 0

        # 监听器列表: [(trigger_id, state_id, opcode, limit_value), ...]
        self._listeners: List[tuple] = []
        self._listener_counter: int = 0

    def update(self, delta_frames: int = 1) -> None:
        """每帧调用，更新游戏状态。

        参数：
            delta_frames: 经过的帧数
        """
        # 更新帧计数器
        self._frame_counter += delta_frames

        # 计算当前时间 (0.0 - 24.0)
        self._time_of_day = (self._frame_counter % self.CYCLE_FRAMES) / self.CYCLE_FRAMES * 24.0

        # 检查注册的监听器条件
        self._check_state_listeners()

    def get_float_state(self, state_id: int) -> float:
        """获取浮点类型游戏状态值。

        参数：
            state_id: 状态ID

        返回：
            状态值，如果未设置返回 0.0
        """
        if state_id == FGameState.TIME_OF_DAY:
            return self._time_of_day
        return self._float_states.get(state_id, 0.0)

    def register_state_listener(
        self,
        trigger_id: str,
        state_id: int,
        opcode: int,
        limit_value: float
    ) -> Optional[str]:
        """注册游戏状态监听器。

        当游戏状态满足条件时，将触发对应触发器。

        参数：
            trigger_id: 触发器ID
            state_id: 游戏状态ID
            opcode: 比较操作符
            limit_value: 目标限制值

        返回：
            监听器handle，失败返回None
        """
        self._listener_counter += 1
        handle = f"gs_listener_{self._listener_counter}"

        self._listeners.append((trigger_id, state_id, opcode, limit_value))

        logger.info(
            f"[GameStateManager] Registered state listener {handle} "
            f"for trigger {trigger_id}, state={state_id}, "
            f"opcode={opcode}, limit={limit_value}"
        )

        return handle

    def _check_state_listeners(self) -> None:
        """检查所有监听器条件，触发满足条件的事件。"""
        for trigger_id, state_id, opcode, limit_value in self._listeners:
            # 获取当前状态值
            if state_id == FGameState.TIME_OF_DAY:
                current_value = self._time_of_day
            else:
                current_value = self._float_states.get(state_id, 0.0)

            # 检查条件
            if LimitOp.compare(opcode, current_value, limit_value):
                # 触发事件
                from jass_runner.trigger.event_types import EVENT_GAME_STATE_LIMIT

                event_data = {
                    "state_id": state_id,
                    "current_value": current_value,
                    "limit_value": limit_value,
                    "opcode": opcode
                }

                self._trigger_manager.fire_event(EVENT_GAME_STATE_LIMIT, event_data)

                logger.debug(
                    f"[GameStateManager] Fired EVENT_GAME_STATE_LIMIT for "
                    f"trigger {trigger_id}, state={state_id}"
                )
```

**Step 4: 运行测试验证通过**

Run: `pytest tests/gamestate/test_manager.py -v`
Expected: PASS (7 tests)

**Step 5: 提交**

```bash
git add src/jass_runner/gamestate/ tests/gamestate/
git commit -m "$(cat <<'EOF'
feat(gamestate): 添加 GameStateManager 实现

实现游戏状态管理器，包含：
- 日夜循环系统（每9000帧一个周期）
- 状态监听器注册和检查
- 与 TriggerManager 集成触发事件

Co-Authored-By: Claude (kimi-k2.5) <noreply@anthropic.com>
EOF
)"
```

---

## Task 4: 添加 EVENT_GAME_STATE_LIMIT 事件类型

**Files:**
- Modify: `src/jass_runner/trigger/event_types.py`
- Test: `tests/trigger/test_event_types.py` (已存在，添加测试)

**Step 1: 编写失败测试**

在 `tests/trigger/test_event_types.py` 中添加：

```python
def test_event_game_state_limit_defined(self):
    """测试 EVENT_GAME_STATE_LIMIT 已定义。"""
    from jass_runner.trigger.event_types import EVENT_GAME_STATE_LIMIT
    assert EVENT_GAME_STATE_LIMIT == "game_state_limit"

def test_event_game_state_limit_in_game_events(self):
    """测试 EVENT_GAME_STATE_LIMIT 在游戏事件列表中。"""
    from jass_runner.trigger.event_types import (
        EVENT_GAME_STATE_LIMIT, GAME_EVENTS
    )
    assert EVENT_GAME_STATE_LIMIT in GAME_EVENTS

def test_event_game_state_limit_in_all_events(self):
    """测试 EVENT_GAME_STATE_LIMIT 在所有事件列表中。"""
    from jass_runner.trigger.event_types import (
        EVENT_GAME_STATE_LIMIT, ALL_EVENTS
    )
    assert EVENT_GAME_STATE_LIMIT in ALL_EVENTS
```

**Step 2: 运行测试验证失败**

Run: `pytest tests/trigger/test_event_types.py::test_event_game_state_limit_defined -v`
Expected: FAIL with "ImportError: cannot import name 'EVENT_GAME_STATE_LIMIT'"

**Step 3: 修改 event_types.py**

在 `src/jass_runner/trigger/event_types.py` 的游戏事件部分添加：

```python
# 在 EVENT_GAME_TIMER_EXPIRED 后面添加
EVENT_GAME_STATE_LIMIT = "game_state_limit"
"""游戏状态达到限制条件事件 - 当游戏状态满足注册条件时触发。"""
```

同时更新 GAME_EVENTS 列表：

```python
GAME_EVENTS = [
    EVENT_GAME_TIMER_EXPIRED,
    EVENT_GAME_STATE_LIMIT,  # 添加这一行
]
```

**Step 4: 运行测试验证通过**

Run: `pytest tests/trigger/test_event_types.py -v`
Expected: PASS (原有测试 + 3个新测试)

**Step 5: 提交**

```bash
git add src/jass_runner/trigger/event_types.py tests/trigger/test_event_types.py
git commit -m "$(cat <<'EOF'
feat(trigger): 添加 EVENT_GAME_STATE_LIMIT 事件类型

添加游戏状态限制事件类型，用于 GameStateManager 触发状态条件事件。

Co-Authored-By: Claude (kimi-k2.5) <noreply@anthropic.com>
EOF
)"
```

---

## Task 5: 实现 TriggerRegisterGameStateEvent Native 函数

**Files:**
- Create: `src/jass_runner/natives/gamestate_event_natives.py`
- Test: `tests/natives/test_gamestate_event_natives.py`

**Step 1: 编写失败测试**

```python
"""GameState 事件注册 native 函数测试。"""

import pytest
from unittest.mock import Mock, MagicMock

from jass_runner.natives.gamestate_event_natives import TriggerRegisterGameStateEvent
from jass_runner.types.gamestate import FGameState
from jass_runner.types.limitop import LimitOp


class TestTriggerRegisterGameStateEvent:
    """测试 TriggerRegisterGameStateEvent native 函数。"""

    def test_name_is_correct(self):
        """测试函数名称正确。"""
        native = TriggerRegisterGameStateEvent()
        assert native.name == "TriggerRegisterGameStateEvent"

    def test_execute_registers_listener(self):
        """测试执行时注册监听器。"""
        native = TriggerRegisterGameStateEvent()

        mock_state_context = Mock()
        mock_gamestate_manager = Mock()
        mock_gamestate_manager.register_state_listener.return_value = "event_001"
        mock_state_context.game_state_manager = mock_gamestate_manager

        result = native.execute(
            mock_state_context,
            "trigger_001",
            FGameState.TIME_OF_DAY,
            LimitOp.EQUAL,
            6.0
        )

        assert result == "event_001"
        mock_gamestate_manager.register_state_listener.assert_called_once_with(
            "trigger_001",
            FGameState.TIME_OF_DAY,
            LimitOp.EQUAL,
            6.0
        )

    def test_execute_without_game_state_manager(self):
        """测试没有 game_state_manager 时返回 None。"""
        native = TriggerRegisterGameStateEvent()

        mock_state_context = Mock()
        # 不设置 game_state_manager
        del mock_state_context.game_state_manager

        result = native.execute(
            mock_state_context,
            "trigger_001",
            FGameState.TIME_OF_DAY,
            LimitOp.EQUAL,
            6.0
        )

        assert result is None

    def test_execute_with_none_state_context(self):
        """测试 state_context 为 None 时返回 None。"""
        native = TriggerRegisterGameStateEvent()

        result = native.execute(
            None,
            "trigger_001",
            FGameState.TIME_OF_DAY,
            LimitOp.EQUAL,
            6.0
        )

        assert result is None
```

**Step 2: 运行测试验证失败**

Run: `pytest tests/natives/test_gamestate_event_natives.py -v`
Expected: FAIL with "ModuleNotFoundError"

**Step 3: 编写实现**

```python
"""游戏状态事件注册相关的原生函数。

此模块包含 JASS 触发器系统中游戏状态事件注册相关的 native 函数实现。
"""

import logging

from ..natives.base import NativeFunction

logger = logging.getLogger(__name__)


class TriggerRegisterGameStateEvent(NativeFunction):
    """注册游戏状态事件的原生函数。

    当游戏状态满足指定条件时触发事件。
    示例：TriggerRegisterGameStateEvent(trg, GAME_STATE_TIME_OF_DAY, EQUAL, 6.0)
    """

    @property
    def name(self) -> str:
        """获取 native 函数的名称。

        返回：
            "TriggerRegisterGameStateEvent"
        """
        return "TriggerRegisterGameStateEvent"

    def execute(self, state_context, trigger_id: str, state_id: int,
                opcode: int, limit_value: float, *args, **kwargs):
        """执行 TriggerRegisterGameStateEvent 原生函数。

        参数：
            state_context: 状态上下文，必须包含 game_state_manager
            trigger_id: 要注册事件的触发器ID
            state_id: 游戏状态ID (如 FGameState.TIME_OF_DAY)
            opcode: 比较操作符 (如 LimitOp.EQUAL)
            limit_value: 目标限制值
            *args: 额外位置参数
            **kwargs: 关键字参数

        返回：
            事件 handle 字符串，如果注册失败则返回 None
        """
        # 检查 state_context 和 game_state_manager 存在性
        if state_context is None or not hasattr(state_context, 'game_state_manager'):
            logger.error(
                "[TriggerRegisterGameStateEvent] state_context or "
                "game_state_manager not found"
            )
            return None

        game_state_manager = state_context.game_state_manager

        result = game_state_manager.register_state_listener(
            trigger_id,
            state_id,
            opcode,
            limit_value
        )

        if result:
            logger.info(
                f"[TriggerRegisterGameStateEvent] Registered game state event "
                f"{result} (state={state_id}, opcode={opcode}, "
                f"limit={limit_value}) on trigger {trigger_id}"
            )
        else:
            logger.warning(
                f"[TriggerRegisterGameStateEvent] Failed to register game "
                f"state event on trigger {trigger_id}"
            )

        return result
```

**Step 4: 运行测试验证通过**

Run: `pytest tests/natives/test_gamestate_event_natives.py -v`
Expected: PASS (4 tests)

**Step 5: 提交**

```bash
git add src/jass_runner/natives/gamestate_event_natives.py tests/natives/test_gamestate_event_natives.py
git commit -m "$(cat <<'EOF'
feat(natives): 添加 TriggerRegisterGameStateEvent native 函数

实现游戏状态事件注册函数，支持注册 TIME_OF_DAY 等状态的条件监听。

Co-Authored-By: Claude (kimi-k2.5) <noreply@anthropic.com>
EOF
)"
```

---

## Task 6: 集成到 StateContext

**Files:**
- Modify: `src/jass_runner/natives/state.py`
- Test: `tests/natives/test_state.py` (已存在，验证修改)

**Step 1: 修改 StateContext**

在 `src/jass_runner/natives/state.py` 的 `StateContext` 类中添加：

```python
# 在 __init__ 方法中添加
from jass_runner.gamestate.manager import GameStateManager
self.game_state_manager = GameStateManager(self.trigger_manager)
```

**Step 2: 运行现有测试**

Run: `pytest tests/natives/test_state.py -v`
Expected: PASS (确保不破坏现有功能)

**Step 3: 提交**

```bash
git add src/jass_runner/natives/state.py
git commit -m "$(cat <<'EOF'
feat(natives): StateContext 集成 GameStateManager

在 StateContext 中初始化 GameStateManager，建立状态管理基础设施。

Co-Authored-By: Claude (kimi-k2.5) <noreply@anthropic.com>
EOF
)"
```

---

## Task 7: 注册 Native 函数到工厂

**Files:**
- Modify: `src/jass_runner/natives/factory.py`
- Test: 运行 `tests/natives/test_factory.py` 验证

**Step 1: 修改 factory.py**

在 `create_default_registry` 方法中添加导入和注册：

```python
# 在文件顶部导入部分添加
from .gamestate_event_natives import TriggerRegisterGameStateEvent

# 在 registry.register 调用部分添加
registry.register(TriggerRegisterGameStateEvent())
```

**Step 2: 运行测试验证**

Run: `pytest tests/natives/test_factory.py -v`
Expected: PASS

同时验证 native 函数已注册：

```python
# 临时验证脚本
python -c "
from jass_runner.natives.factory import NativeFactory
registry = NativeFactory.create_default_registry()
native = registry.get('TriggerRegisterGameStateEvent')
print(f'Native found: {native is not None}')
print(f'Native name: {native.name if native else \"N/A\"}')
"
```

Expected output:
```
Native found: True
Native name: TriggerRegisterGameStateEvent
```

**Step 3: 提交**

```bash
git add src/jass_runner/natives/factory.py
git commit -m "$(cat <<'EOF'
feat(natives): 注册 TriggerRegisterGameStateEvent 到工厂

在 NativeFactory 中注册游戏状态事件注册函数。

Co-Authored-By: Claude (kimi-k2.5) <noreply@anthropic.com>
EOF
)"
```

---

## Task 8: 创建集成测试

**Files:**
- Create: `tests/integration/test_gamestate_events.py`

**Step 1: 编写集成测试**

```python
"""GameState 事件系统集成测试。

测试完整的游戏状态事件流程：
注册触发器 -> 模拟时间推进 -> 验证事件触发
"""

import pytest
from unittest.mock import Mock

from jass_runner.natives.state import StateContext
from jass_runner.trigger.trigger import Trigger
from jass_runner.types.gamestate import FGameState
from jass_runner.types.limitop import LimitOp
from jass_runner.trigger.event_types import EVENT_GAME_STATE_LIMIT


class TestGameStateEventIntegration:
    """测试 GameState 事件完整流程。"""

    def test_time_of_day_event_triggers(self):
        """测试 TIME_OF_DAY 事件在条件满足时触发。"""
        # 创建状态上下文
        state_context = StateContext()

        # 创建触发器
        trigger = Trigger("trg_001")

        # 添加动作（使用 mock 验证）
        action_called = []

        def test_action():
            action_called.append(True)

        trigger.add_action(test_action)

        # 将触发器添加到管理器
        state_context.trigger_manager._triggers["trg_001"] = trigger

        # 注册游戏状态事件（在时间为 12.0 时触发）
        state_context.game_state_manager.register_state_listener(
            "trg_001",
            FGameState.TIME_OF_DAY,
            LimitOp.EQUAL,
            12.0
        )

        # 模拟时间推进到中午（4500帧 = 12小时）
        state_context.game_state_manager._frame_counter = 4500
        state_context.game_state_manager.update(0)

        # 验证动作被调用
        assert len(action_called) == 1

    def test_dawn_event_with_blizzard_constant(self):
        """测试黎明事件（模拟 bj_TOD_DAWN = 6.0）。"""
        state_context = StateContext()

        trigger = Trigger("trg_dawn")
        dawn_actions = []

        def dawn_action():
            dawn_actions.append("dawn_triggered")

        trigger.add_action(dawn_action)
        state_context.trigger_manager._triggers["trg_dawn"] = trigger

        # 注册黎明事件（6.0 = 黎明）
        state_context.game_state_manager.register_state_listener(
            "trg_dawn",
            FGameState.TIME_OF_DAY,
            LimitOp.EQUAL,
            6.0  # bj_TOD_DAWN
        )

        # 模拟时间推进到黎明（2250帧 = 6小时）
        state_context.game_state_manager._frame_counter = 2250
        state_context.game_state_manager.update(0)

        assert "dawn_triggered" in dawn_actions

    def test_multiple_listeners_same_time(self):
        """测试多个监听器在同一时间触发。"""
        state_context = StateContext()

        # 创建两个触发器
        trigger1 = Trigger("trg_1")
        trigger2 = Trigger("trg_2")

        actions = []
        trigger1.add_action(lambda: actions.append("action1"))
        trigger2.add_action(lambda: actions.append("action2"))

        state_context.trigger_manager._triggers["trg_1"] = trigger1
        state_context.trigger_manager._triggers["trg_2"] = trigger2

        # 注册两个监听器
        state_context.game_state_manager.register_state_listener(
            "trg_1", FGameState.TIME_OF_DAY, LimitOp.EQUAL, 12.0
        )
        state_context.game_state_manager.register_state_listener(
            "trg_2", FGameState.TIME_OF_DAY, LimitOp.EQUAL, 12.0
        )

        # 推进到中午
        state_context.game_state_manager._frame_counter = 4500
        state_context.game_state_manager.update(0)

        assert "action1" in actions
        assert "action2" in actions
```

**Step 2: 运行集成测试**

Run: `pytest tests/integration/test_gamestate_events.py -v`
Expected: PASS (3 tests)

**Step 3: 提交**

```bash
git add tests/integration/test_gamestate_events.py
git commit -m "$(cat <<'EOF'
test(integration): 添加 GameState 事件集成测试

测试完整的游戏状态事件流程，包括 TIME_OF_DAY 事件触发、
黎明事件模拟和多监听器场景。

Co-Authored-By: Claude (kimi-k2.5) <noreply@anthropic.com>
EOF
)"
```

---

## Task 9: 运行完整测试套件

**Step 1: 运行所有相关测试**

```bash
pytest tests/types/test_limitop.py tests/types/test_gamestate.py tests/gamestate/test_manager.py tests/trigger/test_event_types.py tests/natives/test_gamestate_event_natives.py tests/integration/test_gamestate_events.py -v
```

Expected: 所有测试通过

**Step 2: 运行完整测试套件**

```bash
pytest
```

Expected: 所有测试通过

**Step 3: 最终提交**

```bash
git commit -m "$(cat <<'EOF'
feat: 完整实现 GameState 事件系统

实现 TriggerRegisterGameStateEvent native 函数及相关基础设施：
- LimitOp 类型和比较操作符
- IGameState/FGameState 类型常量
- GameStateManager 管理游戏状态和日夜循环
- EVENT_GAME_STATE_LIMIT 事件类型
- 完整的单元测试和集成测试

支持 GAME_STATE_TIME_OF_DAY 状态监控，每9000帧一个完整日夜周期。

Co-Authored-By: Claude (kimi-k2.5) <noreply@anthropic.com>
EOF
)" --allow-empty
```

---

## 完成检查清单

- [ ] LimitOp 类型定义和测试
- [ ] GameState 类型定义和测试
- [ ] GameStateManager 实现和测试
- [ ] EVENT_GAME_STATE_LIMIT 事件类型
- [ ] TriggerRegisterGameStateEvent native 函数
- [ ] StateContext 集成
- [ ] NativeFactory 注册
- [ ] 集成测试
- [ ] 完整测试套件通过

## 实现后验证

验证以下 JASS 代码可以正常工作：

```jass
set bj_dncSoundsDawn = CreateTrigger()
call TriggerRegisterGameStateEvent(bj_dncSoundsDawn, GAME_STATE_TIME_OF_DAY, EQUAL, bj_TOD_DAWN)
call TriggerAddAction(bj_dncSoundsDawn, function SetDNCSoundsDawn)
```
