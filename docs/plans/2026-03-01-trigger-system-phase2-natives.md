# JASS触发器系统实施计划 - 阶段2：Native函数实现

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 实现20个触发器相关的native函数，包括生命周期管理、动作/条件管理、事件注册等功能。

**Architecture:** 每个native函数继承NativeFunction基类，通过execute方法实现具体逻辑，与TriggerManager交互完成触发器操作。

**Tech Stack:** Python 3.8+, pytest, 现有Native函数框架和TriggerManager

---

### Task 1: 实现生命周期管理Native函数（5个）

**Files:**
- Create: `src/jass_runner/natives/trigger_natives.py`
- Test: `tests/natives/test_trigger_natives.py`

**Step 1: Write the failing test**

```python
"""触发器native函数测试 - 生命周期管理。"""

import pytest
from unittest.mock import Mock, MagicMock


@pytest.fixture
def mock_state_context():
    """创建模拟的state_context。"""
    context = Mock()
    context.trigger_manager = Mock()
    return context


def test_create_trigger_native(mock_state_context):
    """测试CreateTrigger native函数。"""
    from jass_runner.natives.trigger_natives import CreateTrigger

    # 设置mock返回值
    mock_state_context.trigger_manager.create_trigger.return_value = "trigger_1"

    # 创建native函数实例
    native = CreateTrigger()

    # 执行
    result = native.execute(mock_state_context)

    # 验证
    assert result == "trigger_1"
    mock_state_context.trigger_manager.create_trigger.assert_called_once()


def test_destroy_trigger_native(mock_state_context):
    """测试DestroyTrigger native函数。"""
    from jass_runner.natives.trigger_natives import DestroyTrigger

    mock_state_context.trigger_manager.destroy_trigger.return_value = True

    native = DestroyTrigger()
    result = native.execute(mock_state_context, "trigger_1")

    assert result is None  # DestroyTrigger返回nothing
    mock_state_context.trigger_manager.destroy_trigger.assert_called_once_with("trigger_1")


def test_destroy_trigger_native_invalid_handle(mock_state_context):
    """测试DestroyTrigger native函数 - 无效handle。"""
    from jass_runner.natives.trigger_natives import DestroyTrigger

    mock_state_context.trigger_manager.destroy_trigger.return_value = False

    native = DestroyTrigger()
    result = native.execute(mock_state_context, "invalid_trigger")

    assert result is None


def test_enable_trigger_native(mock_state_context):
    """测试EnableTrigger native函数。"""
    from jass_runner.natives.trigger_natives import EnableTrigger

    mock_state_context.trigger_manager.enable_trigger.return_value = True

    native = EnableTrigger()
    result = native.execute(mock_state_context, "trigger_1")

    assert result is None
    mock_state_context.trigger_manager.enable_trigger.assert_called_once_with("trigger_1")


def test_disable_trigger_native(mock_state_context):
    """测试DisableTrigger native函数。"""
    from jass_runner.natives.trigger_natives import DisableTrigger

    mock_state_context.trigger_manager.disable_trigger.return_value = True

    native = DisableTrigger()
    result = native.execute(mock_state_context, "trigger_1")

    assert result is None
    mock_state_context.trigger_manager.disable_trigger.assert_called_once_with("trigger_1")


def test_is_trigger_enabled_native(mock_state_context):
    """测试IsTriggerEnabled native函数。"""
    from jass_runner.natives.trigger_natives import IsTriggerEnabled

    mock_state_context.trigger_manager.is_trigger_enabled.return_value = True

    native = IsTriggerEnabled()
    result = native.execute(mock_state_context, "trigger_1")

    assert result is True
    mock_state_context.trigger_manager.is_trigger_enabled.assert_called_once_with("trigger_1")


def test_is_trigger_enabled_native_disabled(mock_state_context):
    """测试IsTriggerEnabled native函数 - 禁用状态。"""
    from jass_runner.natives.trigger_natives import IsTriggerEnabled

    mock_state_context.trigger_manager.is_trigger_enabled.return_value = False

    native = IsTriggerEnabled()
    result = native.execute(mock_state_context, "trigger_1")

    assert result is False
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/natives/test_trigger_natives.py::test_create_trigger_native -v`
Expected: FAIL with "ModuleNotFoundError: No module named 'jass_runner.natives.trigger_natives'"

**Step 3: Write minimal implementation**

```python
"""JASS触发器相关native函数。

此模块包含所有触发器相关的native函数实现。
"""

from typing import Any, Callable, Optional

from .base import NativeFunction


class CreateTrigger(NativeFunction):
    """创建新触发器。"""

    @property
    def name(self) -> str:
        return "CreateTrigger"

    def execute(self, state_context, *args) -> str:
        """创建并返回触发器ID。"""
        if not state_context or not hasattr(state_context, 'trigger_manager'):
            return ""
        return state_context.trigger_manager.create_trigger()


class DestroyTrigger(NativeFunction):
    """销毁触发器。"""

    @property
    def name(self) -> str:
        return "DestroyTrigger"

    def execute(self, state_context, *args):
        """销毁指定的触发器。"""
        if not state_context or not hasattr(state_context, 'trigger_manager'):
            return None

        if len(args) < 1:
            return None

        trigger_id = args[0]
        state_context.trigger_manager.destroy_trigger(trigger_id)
        return None


class EnableTrigger(NativeFunction):
    """启用触发器。"""

    @property
    def name(self) -> str:
        return "EnableTrigger"

    def execute(self, state_context, *args):
        """启用指定的触发器。"""
        if not state_context or not hasattr(state_context, 'trigger_manager'):
            return None

        if len(args) < 1:
            return None

        trigger_id = args[0]
        state_context.trigger_manager.enable_trigger(trigger_id)
        return None


class DisableTrigger(NativeFunction):
    """禁用触发器。"""

    @property
    def name(self) -> str:
        return "DisableTrigger"

    def execute(self, state_context, *args):
        """禁用指定的触发器。"""
        if not state_context or not hasattr(state_context, 'trigger_manager'):
            return None

        if len(args) < 1:
            return None

        trigger_id = args[0]
        state_context.trigger_manager.disable_trigger(trigger_id)
        return None


class IsTriggerEnabled(NativeFunction):
    """检查触发器是否启用。"""

    @property
    def name(self) -> str:
        return "IsTriggerEnabled"

    def execute(self, state_context, *args) -> bool:
        """检查触发器是否启用。"""
        if not state_context or not hasattr(state_context, 'trigger_manager'):
            return False

        if len(args) < 1:
            return False

        trigger_id = args[0]
        return state_context.trigger_manager.is_trigger_enabled(trigger_id)
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/natives/test_trigger_natives.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add tests/natives/test_trigger_natives.py src/jass_runner/natives/trigger_natives.py
git commit -m "feat(trigger): add trigger lifecycle native functions"
```

---

### Task 2: 实现动作管理Native函数（3个）

**Files:**
- Modify: `src/jass_runner/natives/trigger_natives.py`
- Test: `tests/natives/test_trigger_natives.py`

**Step 1: Write the failing test**

```python
"""添加到 tests/natives/test_trigger_natives.py """


def test_trigger_add_action_native(mock_state_context):
    """测试TriggerAddAction native函数。"""
    from jass_runner.natives.trigger_natives import TriggerAddAction

    # 创建模拟触发器
    mock_trigger = Mock()
    mock_trigger.add_action.return_value = "action_001"

    mock_state_context.trigger_manager.get_trigger.return_value = mock_trigger

    # 定义测试动作函数
    def test_action():
        pass

    native = TriggerAddAction()
    result = native.execute(mock_state_context, "trigger_1", test_action)

    assert result == "action_001"
    mock_state_context.trigger_manager.get_trigger.assert_called_once_with("trigger_1")
    mock_trigger.add_action.assert_called_once_with(test_action)


def test_trigger_add_action_native_invalid_trigger(mock_state_context):
    """测试TriggerAddAction native函数 - 无效触发器。"""
    from jass_runner.natives.trigger_natives import TriggerAddAction

    mock_state_context.trigger_manager.get_trigger.return_value = None

    def test_action():
        pass

    native = TriggerAddAction()
    result = native.execute(mock_state_context, "invalid_trigger", test_action)

    assert result is None


def test_trigger_remove_action_native(mock_state_context):
    """测试TriggerRemoveAction native函数。"""
    from jass_runner.natives.trigger_natives import TriggerRemoveAction

    mock_trigger = Mock()
    mock_trigger.remove_action.return_value = True

    mock_state_context.trigger_manager.get_trigger.return_value = mock_trigger

    native = TriggerRemoveAction()
    result = native.execute(mock_state_context, "trigger_1", "action_001")

    assert result is True
    mock_trigger.remove_action.assert_called_once_with("action_001")


def test_trigger_clear_actions_native(mock_state_context):
    """测试TriggerClearActions native函数。"""
    from jass_runner.natives.trigger_natives import TriggerClearActions

    mock_trigger = Mock()
    mock_state_context.trigger_manager.get_trigger.return_value = mock_trigger

    native = TriggerClearActions()
    result = native.execute(mock_state_context, "trigger_1")

    assert result is None
    mock_trigger.clear_actions.assert_called_once()
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/natives/test_trigger_natives.py::test_trigger_add_action_native -v`
Expected: FAIL with "ImportError: cannot import name 'TriggerAddAction'"

**Step 3: Write minimal implementation**

```python
"""添加到 src/jass_runner/natives/trigger_natives.py """


class TriggerAddAction(NativeFunction):
    """为触发器添加动作。"""

    @property
    def name(self) -> str:
        return "TriggerAddAction"

    def execute(self, state_context, *args) -> Optional[str]:
        """为触发器添加动作函数。

        参数：
            state_context: 状态上下文
            args[0]: 触发器ID
            args[1]: 动作函数

        返回：
            动作handle或None
        """
        if not state_context or not hasattr(state_context, 'trigger_manager'):
            return None

        if len(args) < 2:
            return None

        trigger_id = args[0]
        action_func = args[1]

        trigger = state_context.trigger_manager.get_trigger(trigger_id)
        if not trigger:
            return None

        return trigger.add_action(action_func)


class TriggerRemoveAction(NativeFunction):
    """从触发器移除动作。"""

    @property
    def name(self) -> str:
        return "TriggerRemoveAction"

    def execute(self, state_context, *args) -> bool:
        """从触发器移除指定动作。

        参数：
            state_context: 状态上下文
            args[0]: 触发器ID
            args[1]: 动作handle

        返回：
            是否成功移除
        """
        if not state_context or not hasattr(state_context, 'trigger_manager'):
            return False

        if len(args) < 2:
            return False

        trigger_id = args[0]
        action_handle = args[1]

        trigger = state_context.trigger_manager.get_trigger(trigger_id)
        if not trigger:
            return False

        return trigger.remove_action(action_handle)


class TriggerClearActions(NativeFunction):
    """清空触发器的所有动作。"""

    @property
    def name(self) -> str:
        return "TriggerClearActions"

    def execute(self, state_context, *args):
        """清空触发器的所有动作。

        参数：
            state_context: 状态上下文
            args[0]: 触发器ID
        """
        if not state_context or not hasattr(state_context, 'trigger_manager'):
            return None

        if len(args) < 1:
            return None

        trigger_id = args[0]

        trigger = state_context.trigger_manager.get_trigger(trigger_id)
        if not trigger:
            return None

        trigger.clear_actions()
        return None
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/natives/test_trigger_natives.py::test_trigger_add_action_native -v`
Expected: PASS

**Step 5: Commit**

```bash
git add tests/natives/test_trigger_natives.py src/jass_runner/natives/trigger_natives.py
git commit -m "feat(trigger): add trigger action management native functions"
```

---

### Task 3: 实现条件管理Native函数（4个）

**Files:**
- Modify: `src/jass_runner/natives/trigger_natives.py`
- Test: `tests/natives/test_trigger_natives.py`

**Step 1: Write the failing test**

```python
"""添加到 tests/natives/test_trigger_natives.py """


def test_trigger_add_condition_native(mock_state_context):
    """测试TriggerAddCondition native函数。"""
    from jass_runner.natives.trigger_natives import TriggerAddCondition

    mock_trigger = Mock()
    mock_trigger.add_condition.return_value = "condition_001"

    mock_state_context.trigger_manager.get_trigger.return_value = mock_trigger

    def test_condition():
        return True

    native = TriggerAddCondition()
    result = native.execute(mock_state_context, "trigger_1", test_condition)

    assert result == "condition_001"
    mock_trigger.add_condition.assert_called_once_with(test_condition)


def test_trigger_remove_condition_native(mock_state_context):
    """测试TriggerRemoveCondition native函数。"""
    from jass_runner.natives.trigger_natives import TriggerRemoveCondition

    mock_trigger = Mock()
    mock_trigger.remove_condition.return_value = True

    mock_state_context.trigger_manager.get_trigger.return_value = mock_trigger

    native = TriggerRemoveCondition()
    result = native.execute(mock_state_context, "trigger_1", "condition_001")

    assert result is True
    mock_trigger.remove_condition.assert_called_once_with("condition_001")


def test_trigger_clear_conditions_native(mock_state_context):
    """测试TriggerClearConditions native函数。"""
    from jass_runner.natives.trigger_natives import TriggerClearConditions

    mock_trigger = Mock()
    mock_state_context.trigger_manager.get_trigger.return_value = mock_trigger

    native = TriggerClearConditions()
    result = native.execute(mock_state_context, "trigger_1")

    assert result is None
    mock_trigger.clear_conditions.assert_called_once()


def test_trigger_evaluate_native(mock_state_context):
    """测试TriggerEvaluate native函数。"""
    from jass_runner.natives.trigger_natives import TriggerEvaluate

    mock_trigger = Mock()
    mock_trigger.evaluate_conditions.return_value = True

    mock_state_context.trigger_manager.get_trigger.return_value = mock_trigger

    native = TriggerEvaluate()
    result = native.execute(mock_state_context, "trigger_1")

    assert result is True
    mock_trigger.evaluate_conditions.assert_called_once()


def test_trigger_evaluate_native_false(mock_state_context):
    """测试TriggerEvaluate native函数 - 条件为False。"""
    from jass_runner.natives.trigger_natives import TriggerEvaluate

    mock_trigger = Mock()
    mock_trigger.evaluate_conditions.return_value = False

    mock_state_context.trigger_manager.get_trigger.return_value = mock_trigger

    native = TriggerEvaluate()
    result = native.execute(mock_state_context, "trigger_1")

    assert result is False
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/natives/test_trigger_natives.py::test_trigger_add_condition_native -v`
Expected: FAIL with "ImportError: cannot import name 'TriggerAddCondition'"

**Step 3: Write minimal implementation**

```python
"""添加到 src/jass_runner/natives/trigger_natives.py """


class TriggerAddCondition(NativeFunction):
    """为触发器添加条件。"""

    @property
    def name(self) -> str:
        return "TriggerAddCondition"

    def execute(self, state_context, *args) -> Optional[str]:
        """为触发器添加条件函数。

        参数：
            state_context: 状态上下文
            args[0]: 触发器ID
            args[1]: 条件函数

        返回：
            条件handle或None
        """
        if not state_context or not hasattr(state_context, 'trigger_manager'):
            return None

        if len(args) < 2:
            return None

        trigger_id = args[0]
        condition_func = args[1]

        trigger = state_context.trigger_manager.get_trigger(trigger_id)
        if not trigger:
            return None

        return trigger.add_condition(condition_func)


class TriggerRemoveCondition(NativeFunction):
    """从触发器移除条件。"""

    @property
    def name(self) -> str:
        return "TriggerRemoveCondition"

    def execute(self, state_context, *args) -> bool:
        """从触发器移除指定条件。

        参数：
            state_context: 状态上下文
            args[0]: 触发器ID
            args[1]: 条件handle

        返回：
            是否成功移除
        """
        if not state_context or not hasattr(state_context, 'trigger_manager'):
            return False

        if len(args) < 2:
            return False

        trigger_id = args[0]
        condition_handle = args[1]

        trigger = state_context.trigger_manager.get_trigger(trigger_id)
        if not trigger:
            return False

        return trigger.remove_condition(condition_handle)


class TriggerClearConditions(NativeFunction):
    """清空触发器的所有条件。"""

    @property
    def name(self) -> str:
        return "TriggerClearConditions"

    def execute(self, state_context, *args):
        """清空触发器的所有条件。

        参数：
            state_context: 状态上下文
            args[0]: 触发器ID
        """
        if not state_context or not hasattr(state_context, 'trigger_manager'):
            return None

        if len(args) < 1:
            return None

        trigger_id = args[0]

        trigger = state_context.trigger_manager.get_trigger(trigger_id)
        if not trigger:
            return None

        trigger.clear_conditions()
        return None


class TriggerEvaluate(NativeFunction):
    """手动评估触发器条件。"""

    @property
    def name(self) -> str:
        return "TriggerEvaluate"

    def execute(self, state_context, *args) -> bool:
        """手动评估触发器的所有条件。

        参数：
            state_context: 状态上下文
            args[0]: 触发器ID

        返回：
            所有条件是否都满足
        """
        if not state_context or not hasattr(state_context, 'trigger_manager'):
            return False

        if len(args) < 1:
            return False

        trigger_id = args[0]

        trigger = state_context.trigger_manager.get_trigger(trigger_id)
        if not trigger:
            return False

        return trigger.evaluate_conditions({})
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/natives/test_trigger_natives.py::test_trigger_add_condition_native -v`
Expected: PASS

**Step 5: Commit**

```bash
git add tests/natives/test_trigger_natives.py src/jass_runner/natives/trigger_natives.py
git commit -m "feat(trigger): add trigger condition management native functions"
```

---

### Task 4: 实现事件注册Native函数（6个）

**Files:**
- Modify: `src/jass_runner/natives/trigger_natives.py`
- Test: `tests/natives/test_trigger_natives.py`

**Step 1: Write the failing test**

```python
"""添加到 tests/natives/test_trigger_natives.py """


def test_trigger_register_timer_event_native(mock_state_context):
    """测试TriggerRegisterTimerEvent native函数。"""
    from jass_runner.natives.trigger_natives import TriggerRegisterTimerEvent

    mock_state_context.trigger_manager.register_event.return_value = "event_001"

    native = TriggerRegisterTimerEvent()
    result = native.execute(mock_state_context, "trigger_1", 1.0, False)

    assert result == "event_001"
    mock_state_context.trigger_manager.register_event.assert_called_once()


def test_trigger_register_timer_expire_event_native(mock_state_context):
    """测试TriggerRegisterTimerExpireEvent native函数。"""
    from jass_runner.natives.trigger_natives import TriggerRegisterTimerExpireEvent

    mock_state_context.trigger_manager.register_event.return_value = "event_002"

    native = TriggerRegisterTimerExpireEvent()
    result = native.execute(mock_state_context, "trigger_1", "timer_001")

    assert result == "event_002"


def test_trigger_register_player_unit_event_native(mock_state_context):
    """测试TriggerRegisterPlayerUnitEvent native函数。"""
    from jass_runner.natives.trigger_natives import TriggerRegisterPlayerUnitEvent
    from jass_runner.trigger.event_types import EVENT_PLAYER_UNIT_DEATH

    mock_state_context.trigger_manager.register_event.return_value = "event_003"

    native = TriggerRegisterPlayerUnitEvent()
    result = native.execute(mock_state_context, "trigger_1", 0, EVENT_PLAYER_UNIT_DEATH, None)

    assert result == "event_003"


def test_trigger_register_unit_event_native(mock_state_context):
    """测试TriggerRegisterUnitEvent native函数。"""
    from jass_runner.natives.trigger_natives import TriggerRegisterUnitEvent
    from jass_runner.trigger.event_types import EVENT_UNIT_DEATH

    mock_state_context.trigger_manager.register_event.return_value = "event_004"

    native = TriggerRegisterUnitEvent()
    result = native.execute(mock_state_context, "trigger_1", EVENT_UNIT_DEATH, None)

    assert result == "event_004"


def test_trigger_register_player_event_native(mock_state_context):
    """测试TriggerRegisterPlayerEvent native函数。"""
    from jass_runner.natives.trigger_natives import TriggerRegisterPlayerEvent
    from jass_runner.trigger.event_types import EVENT_PLAYER_DEFEAT

    mock_state_context.trigger_manager.register_event.return_value = "event_005"

    native = TriggerRegisterPlayerEvent()
    result = native.execute(mock_state_context, "trigger_1", 0, EVENT_PLAYER_DEFEAT)

    assert result == "event_005"


def test_trigger_register_game_event_native(mock_state_context):
    """测试TriggerRegisterGameEvent native函数。"""
    from jass_runner.natives.trigger_natives import TriggerRegisterGameEvent
    from jass_runner.trigger.event_types import EVENT_GAME_TIMER_EXPIRED

    mock_state_context.trigger_manager.register_event.return_value = "event_006"

    native = TriggerRegisterGameEvent()
    result = native.execute(mock_state_context, "trigger_1", EVENT_GAME_TIMER_EXPIRED)

    assert result == "event_006"
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/natives/test_trigger_natives.py::test_trigger_register_timer_event_native -v`
Expected: FAIL with "ImportError: cannot import name 'TriggerRegisterTimerEvent'"

**Step 3: Write minimal implementation**

```python
"""添加到 src/jass_runner/natives/trigger_natives.py """


class TriggerRegisterTimerEvent(NativeFunction):
    """注册计时器事件。"""

    @property
    def name(self) -> str:
        return "TriggerRegisterTimerEvent"

    def execute(self, state_context, *args) -> Optional[str]:
        """注册计时器事件。

        参数：
            state_context: 状态上下文
            args[0]: 触发器ID
            args[1]: 超时时间（秒）
            args[2]: 是否周期性

        返回：
            事件handle或None
        """
        if not state_context or not hasattr(state_context, 'trigger_manager'):
            return None

        if len(args) < 3:
            return None

        trigger_id = args[0]
        timeout = args[1]
        periodic = args[2]

        # 这里应该与TimerSystem集成，暂时简化处理
        filter_data = {"timeout": timeout, "periodic": periodic}
        return state_context.trigger_manager.register_event(
            trigger_id, "EVENT_TIMER_GENERIC", filter_data
        )


class TriggerRegisterTimerExpireEvent(NativeFunction):
    """注册特定计时器过期事件。"""

    @property
    def name(self) -> str:
        return "TriggerRegisterTimerExpireEvent"

    def execute(self, state_context, *args) -> Optional[str]:
        """注册特定计时器过期事件。

        参数：
            state_context: 状态上下文
            args[0]: 触发器ID
            args[1]: 计时器ID

        返回：
            事件handle或None
        """
        if not state_context or not hasattr(state_context, 'trigger_manager'):
            return None

        if len(args) < 2:
            return None

        trigger_id = args[0]
        timer_id = args[1]

        from jass_runner.trigger.event_types import EVENT_GAME_TIMER_EXPIRED

        filter_data = {"timer_id": timer_id}
        return state_context.trigger_manager.register_event(
            trigger_id, EVENT_GAME_TIMER_EXPIRED, filter_data
        )


class TriggerRegisterPlayerUnitEvent(NativeFunction):
    """注册玩家单位事件。"""

    @property
    def name(self) -> str:
        return "TriggerRegisterPlayerUnitEvent"

    def execute(self, state_context, *args) -> Optional[str]:
        """注册玩家单位事件。

        参数：
            state_context: 状态上下文
            args[0]: 触发器ID
            args[1]: 玩家ID
            args[2]: 事件类型
            args[3]: 过滤器（可选）

        返回：
            事件handle或None
        """
        if not state_context or not hasattr(state_context, 'trigger_manager'):
            return None

        if len(args) < 3:
            return None

        trigger_id = args[0]
        player_id = args[1]
        event_type = args[2]
        filter_data = args[3] if len(args) > 3 else None

        if filter_data is None:
            filter_data = {}
        filter_data["player_id"] = player_id

        return state_context.trigger_manager.register_event(
            trigger_id, event_type, filter_data
        )


class TriggerRegisterUnitEvent(NativeFunction):
    """注册单位事件。"""

    @property
    def name(self) -> str:
        return "TriggerRegisterUnitEvent"

    def execute(self, state_context, *args) -> Optional[str]:
        """注册单位事件。

        参数：
            state_context: 状态上下文
            args[0]: 触发器ID
            args[1]: 事件类型
            args[2]: 过滤器（可选）

        返回：
            事件handle或None
        """
        if not state_context or not hasattr(state_context, 'trigger_manager'):
            return None

        if len(args) < 2:
            return None

        trigger_id = args[0]
        event_type = args[1]
        filter_data = args[2] if len(args) > 2 else None

        return state_context.trigger_manager.register_event(
            trigger_id, event_type, filter_data
        )


class TriggerRegisterPlayerEvent(NativeFunction):
    """注册玩家事件。"""

    @property
    def name(self) -> str:
        return "TriggerRegisterPlayerEvent"

    def execute(self, state_context, *args) -> Optional[str]:
        """注册玩家事件。

        参数：
            state_context: 状态上下文
            args[0]: 触发器ID
            args[1]: 玩家ID
            args[2]: 事件类型

        返回：
            事件handle或None
        """
        if not state_context or not hasattr(state_context, 'trigger_manager'):
            return None

        if len(args) < 3:
            return None

        trigger_id = args[0]
        player_id = args[1]
        event_type = args[2]

        filter_data = {"player_id": player_id}

        return state_context.trigger_manager.register_event(
            trigger_id, event_type, filter_data
        )


class TriggerRegisterGameEvent(NativeFunction):
    """注册游戏事件。"""

    @property
    def name(self) -> str:
        return "TriggerRegisterGameEvent"

    def execute(self, state_context, *args) -> Optional[str]:
        """注册游戏事件。

        参数：
            state_context: 状态上下文
            args[0]: 触发器ID
            args[1]: 事件类型

        返回：
            事件handle或None
        """
        if not state_context or not hasattr(state_context, 'trigger_manager'):
            return None

        if len(args) < 2:
            return None

        trigger_id = args[0]
        event_type = args[1]

        return state_context.trigger_manager.register_event(
            trigger_id, event_type, None
        )
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/natives/test_trigger_natives.py::test_trigger_register_timer_event_native -v`
Expected: PASS

**Step 5: Commit**

```bash
git add tests/natives/test_trigger_natives.py src/jass_runner/natives/trigger_natives.py
git commit -m "feat(trigger): add trigger event registration native functions"
```

---

### Task 5: 实现事件清理Native函数（1个）

**Files:**
- Modify: `src/jass_runner/natives/trigger_natives.py`
- Test: `tests/natives/test_trigger_natives.py`

**Step 1: Write the failing test**

```python
"""添加到 tests/natives/test_trigger_natives.py """


def test_trigger_clear_events_native(mock_state_context):
    """测试TriggerClearEvents native函数。"""
    from jass_runner.natives.trigger_natives import TriggerClearEvents

    mock_state_context.trigger_manager.clear_trigger_events.return_value = True

    native = TriggerClearEvents()
    result = native.execute(mock_state_context, "trigger_1")

    assert result is None
    mock_state_context.trigger_manager.clear_trigger_events.assert_called_once_with("trigger_1")


def test_trigger_clear_events_native_invalid_trigger(mock_state_context):
    """测试TriggerClearEvents native函数 - 无效触发器。"""
    from jass_runner.natives.trigger_natives import TriggerClearEvents

    mock_state_context.trigger_manager.clear_trigger_events.return_value = False

    native = TriggerClearEvents()
    result = native.execute(mock_state_context, "invalid_trigger")

    assert result is None
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/natives/test_trigger_natives.py::test_trigger_clear_events_native -v`
Expected: FAIL with "ImportError: cannot import name 'TriggerClearEvents'"

**Step 3: Write minimal implementation**

```python
"""添加到 src/jass_runner/natives/trigger_natives.py """


class TriggerClearEvents(NativeFunction):
    """清空触发器的所有事件。"""

    @property
    def name(self) -> str:
        return "TriggerClearEvents"

    def execute(self, state_context, *args):
        """清空触发器的所有事件。

        参数：
            state_context: 状态上下文
            args[0]: 触发器ID
        """
        if not state_context or not hasattr(state_context, 'trigger_manager'):
            return None

        if len(args) < 1:
            return None

        trigger_id = args[0]
        state_context.trigger_manager.clear_trigger_events(trigger_id)
        return None
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/natives/test_trigger_natives.py::test_trigger_clear_events_native -v`
Expected: PASS

**Step 5: Commit**

```bash
git add tests/natives/test_trigger_natives.py src/jass_runner/natives/trigger_natives.py
git commit -m "feat(trigger): add TriggerClearEvents native function"
```

---

### Task 6: 更新NativeRegistry注册触发器函数

**Files:**
- Modify: `src/jass_runner/natives/factory.py`
- Test: `tests/natives/test_factory.py`

**Step 1: Write the failing test**

```python
"""添加到 tests/natives/test_factory.py 或创建新测试文件"""


def test_factory_creates_trigger_natives():
    """测试NativeFactory创建触发器native函数。"""
    from jass_runner.natives.factory import NativeFactory
    from jass_runner.natives.trigger_natives import (
        CreateTrigger, DestroyTrigger, EnableTrigger, DisableTrigger,
        IsTriggerEnabled, TriggerAddAction, TriggerRemoveAction, TriggerClearActions,
        TriggerAddCondition, TriggerRemoveCondition, TriggerClearConditions,
        TriggerEvaluate, TriggerRegisterTimerEvent, TriggerRegisterTimerExpireEvent,
        TriggerRegisterPlayerUnitEvent, TriggerRegisterUnitEvent,
        TriggerRegisterPlayerEvent, TriggerRegisterGameEvent, TriggerClearEvents,
    )

    registry = NativeFactory.create_default_registry()

    # 验证所有触发器native函数已注册
    assert isinstance(registry.get_native("CreateTrigger"), CreateTrigger)
    assert isinstance(registry.get_native("DestroyTrigger"), DestroyTrigger)
    assert isinstance(registry.get_native("EnableTrigger"), EnableTrigger)
    assert isinstance(registry.get_native("DisableTrigger"), DisableTrigger)
    assert isinstance(registry.get_native("IsTriggerEnabled"), IsTriggerEnabled)
    assert isinstance(registry.get_native("TriggerAddAction"), TriggerAddAction)
    assert isinstance(registry.get_native("TriggerRemoveAction"), TriggerRemoveAction)
    assert isinstance(registry.get_native("TriggerClearActions"), TriggerClearActions)
    assert isinstance(registry.get_native("TriggerAddCondition"), TriggerAddCondition)
    assert isinstance(registry.get_native("TriggerRemoveCondition"), TriggerRemoveCondition)
    assert isinstance(registry.get_native("TriggerClearConditions"), TriggerClearConditions)
    assert isinstance(registry.get_native("TriggerEvaluate"), TriggerEvaluate)
    assert isinstance(registry.get_native("TriggerRegisterTimerEvent"), TriggerRegisterTimerEvent)
    assert isinstance(registry.get_native("TriggerRegisterTimerExpireEvent"), TriggerRegisterTimerExpireEvent)
    assert isinstance(registry.get_native("TriggerRegisterPlayerUnitEvent"), TriggerRegisterPlayerUnitEvent)
    assert isinstance(registry.get_native("TriggerRegisterUnitEvent"), TriggerRegisterUnitEvent)
    assert isinstance(registry.get_native("TriggerRegisterPlayerEvent"), TriggerRegisterPlayerEvent)
    assert isinstance(registry.get_native("TriggerRegisterGameEvent"), TriggerRegisterGameEvent)
    assert isinstance(registry.get_native("TriggerClearEvents"), TriggerClearEvents)
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/natives/test_factory.py::test_factory_creates_trigger_natives -v`
Expected: FAIL with "AssertionError" (因为函数还未注册)

**Step 3: Write minimal implementation**

```python
"""修改 src/jass_runner/natives/factory.py """

# 在文件顶部添加导入
from .trigger_natives import (
    CreateTrigger, DestroyTrigger, EnableTrigger, DisableTrigger,
    IsTriggerEnabled, TriggerAddAction, TriggerRemoveAction, TriggerClearActions,
    TriggerAddCondition, TriggerRemoveCondition, TriggerClearConditions,
    TriggerEvaluate, TriggerRegisterTimerEvent, TriggerRegisterTimerExpireEvent,
    TriggerRegisterPlayerUnitEvent, TriggerRegisterUnitEvent,
    TriggerRegisterPlayerEvent, TriggerRegisterGameEvent, TriggerClearEvents,
)


# 在 create_default_registry 方法中添加注册
@staticmethod
def create_default_registry() -> NativeRegistry:
    """创建包含所有默认native函数的注册表。"""
    registry = NativeRegistry()

    # ... 现有注册 ...

    # 注册触发器native函数
    registry.register(CreateTrigger())
    registry.register(DestroyTrigger())
    registry.register(EnableTrigger())
    registry.register(DisableTrigger())
    registry.register(IsTriggerEnabled())
    registry.register(TriggerAddAction())
    registry.register(TriggerRemoveAction())
    registry.register(TriggerClearActions())
    registry.register(TriggerAddCondition())
    registry.register(TriggerRemoveCondition())
    registry.register(TriggerClearConditions())
    registry.register(TriggerEvaluate())
    registry.register(TriggerRegisterTimerEvent())
    registry.register(TriggerRegisterTimerExpireEvent())
    registry.register(TriggerRegisterPlayerUnitEvent())
    registry.register(TriggerRegisterUnitEvent())
    registry.register(TriggerRegisterPlayerEvent())
    registry.register(TriggerRegisterGameEvent())
    registry.register(TriggerClearEvents())

    return registry
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/natives/test_factory.py::test_factory_creates_trigger_natives -v`
Expected: PASS

**Step 5: Commit**

```bash
git add tests/natives/test_factory.py src/jass_runner/natives/factory.py
git commit -m "feat(trigger): register all trigger native functions in NativeFactory"
```

---

### Task 7: 更新natives模块导出

**Files:**
- Modify: `src/jass_runner/natives/__init__.py`
- Test: `tests/natives/test_imports.py`

**Step 1: Write the failing test**

```python
"""添加到 tests/natives/test_imports.py """


def test_trigger_natives_imports():
    """测试触发器native函数导入。"""
    from jass_runner.natives import (
        CreateTrigger, DestroyTrigger, EnableTrigger, DisableTrigger,
        IsTriggerEnabled, TriggerAddAction, TriggerRemoveAction, TriggerClearActions,
        TriggerAddCondition, TriggerRemoveCondition, TriggerClearConditions,
        TriggerEvaluate, TriggerRegisterTimerEvent, TriggerRegisterTimerExpireEvent,
        TriggerRegisterPlayerUnitEvent, TriggerRegisterUnitEvent,
        TriggerRegisterPlayerEvent, TriggerRegisterGameEvent, TriggerClearEvents,
    )

    # 验证所有类都可导入
    assert CreateTrigger is not None
    assert DestroyTrigger is not None
    assert TriggerClearEvents is not None
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/natives/test_imports.py::test_trigger_natives_imports -v`
Expected: FAIL with "ImportError"

**Step 3: Write minimal implementation**

```python
"""修改 src/jass_runner/natives/__init__.py """

# 添加导入
from .trigger_natives import (
    CreateTrigger, DestroyTrigger, EnableTrigger, DisableTrigger,
    IsTriggerEnabled, TriggerAddAction, TriggerRemoveAction, TriggerClearActions,
    TriggerAddCondition, TriggerRemoveCondition, TriggerClearConditions,
    TriggerEvaluate, TriggerRegisterTimerEvent, TriggerRegisterTimerExpireEvent,
    TriggerRegisterPlayerUnitEvent, TriggerRegisterUnitEvent,
    TriggerRegisterPlayerEvent, TriggerRegisterGameEvent, TriggerClearEvents,
)

# 更新 __all__ 列表
__all__ = [
    # ... 现有导出 ...
    # 触发器native函数
    "CreateTrigger",
    "DestroyTrigger",
    "EnableTrigger",
    "DisableTrigger",
    "IsTriggerEnabled",
    "TriggerAddAction",
    "TriggerRemoveAction",
    "TriggerClearActions",
    "TriggerAddCondition",
    "TriggerRemoveCondition",
    "TriggerClearConditions",
    "TriggerEvaluate",
    "TriggerRegisterTimerEvent",
    "TriggerRegisterTimerExpireEvent",
    "TriggerRegisterPlayerUnitEvent",
    "TriggerRegisterUnitEvent",
    "TriggerRegisterPlayerEvent",
    "TriggerRegisterGameEvent",
    "TriggerClearEvents",
]
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/natives/test_imports.py::test_trigger_natives_imports -v`
Expected: PASS

**Step 5: Commit**

```bash
git add tests/natives/test_imports.py src/jass_runner/natives/__init__.py
git commit -m "feat(trigger): update natives module exports for trigger functions"
```

---

### Task 8: 运行阶段2完整测试套件

**Files:**
- Test: 所有阶段2相关测试文件

**Step 1: 运行所有触发器native函数测试**

Run: `pytest tests/natives/test_trigger_natives.py -v`
Expected: 所有测试通过

**Step 2: 验证测试覆盖率**

Run: `pytest --cov=src/jass_runner/natives/trigger_natives --cov-report=term-missing tests/natives/test_trigger_natives.py`
Expected: 显示覆盖率报告，关键模块应达到90%以上

**Step 3: 运行完整项目测试确保无回归**

Run: `pytest tests/ -v`
Expected: 所有现有测试通过，无回归

**Step 4: 提交最终状态**

```bash
git add .
git commit -m "feat(trigger): complete phase 2 - all 20 trigger native functions"
```

---

## 阶段2完成标准

1. **生命周期管理**：5个native函数（CreateTrigger, DestroyTrigger, EnableTrigger, DisableTrigger, IsTriggerEnabled）
2. **动作管理**：3个native函数（TriggerAddAction, TriggerRemoveAction, TriggerClearActions）
3. **条件管理**：4个native函数（TriggerAddCondition, TriggerRemoveCondition, TriggerClearConditions, TriggerEvaluate）
4. **事件注册**：6个native函数（TriggerRegisterTimerEvent, TriggerRegisterTimerExpireEvent, TriggerRegisterPlayerUnitEvent, TriggerRegisterUnitEvent, TriggerRegisterPlayerEvent, TriggerRegisterGameEvent）
5. **事件清理**：1个native函数（TriggerClearEvents）
6. **工厂注册**：所有20个函数在NativeFactory中注册
7. **模块导出**：natives模块导出所有触发器函数
8. **完整测试覆盖**：所有native函数都有单元测试
9. **无回归**：所有现有测试通过

## 下一阶段

阶段3将集成触发器系统与HandleManager和TimerSystem。
计划保存为：`docs/plans/2026-03-01-trigger-system-phase3-integration.md`
