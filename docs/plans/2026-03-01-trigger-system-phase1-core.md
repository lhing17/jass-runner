# JASS触发器系统实施计划 - 阶段1：核心组件

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 实现触发器系统的核心组件：Trigger类、TriggerManager类和事件类型定义。

**Architecture:** 采用混合架构，Trigger类管理单个触发器的事件/条件/动作，TriggerManager集中管理所有触发器生命周期和事件分发，与现有TimerSystem风格保持一致。

**Tech Stack:** Python 3.8+, pytest, 现有Handle和Native函数框架

---

### Task 1: 创建事件类型定义模块

**Files:**
- Create: `src/jass_runner/trigger/event_types.py`
- Test: `tests/trigger/test_event_types.py`

**Step 1: Write the failing test**

```python
"""事件类型定义测试。"""


def test_event_type_constants():
    """测试事件类型常量定义。"""
    from jass_runner.trigger.event_types import (
        EVENT_PLAYER_UNIT_DEATH,
        EVENT_PLAYER_UNIT_ATTACKED,
        EVENT_PLAYER_UNIT_SPELL_EFFECT,
        EVENT_PLAYER_UNIT_DAMAGED,
        EVENT_PLAYER_UNIT_PICKUP_ITEM,
        EVENT_PLAYER_UNIT_DROP_ITEM,
        EVENT_PLAYER_UNIT_USE_ITEM,
        EVENT_PLAYER_UNIT_ISSUED_ORDER,
        EVENT_UNIT_DEATH,
        EVENT_UNIT_DAMAGED,
        EVENT_PLAYER_DEFEAT,
        EVENT_PLAYER_VICTORY,
        EVENT_PLAYER_LEAVE,
        EVENT_PLAYER_CHAT,
        EVENT_GAME_TIMER_EXPIRED,
    )

    # 验证所有常量都是字符串
    assert isinstance(EVENT_PLAYER_UNIT_DEATH, str)
    assert isinstance(EVENT_UNIT_DEATH, str)
    assert isinstance(EVENT_PLAYER_DEFEAT, str)

    # 验证值不为空
    assert EVENT_PLAYER_UNIT_DEATH != ""
    assert EVENT_UNIT_DEATH != ""


def test_event_categories():
    """测试事件分类列表。"""
    from jass_runner.trigger.event_types import (
        PLAYER_UNIT_EVENTS,
        UNIT_EVENTS,
        PLAYER_EVENTS,
        GAME_EVENTS,
        ALL_EVENTS,
    )

    # 验证分类列表包含正确的事件
    assert EVENT_PLAYER_UNIT_DEATH in PLAYER_UNIT_EVENTS
    assert EVENT_UNIT_DEATH in UNIT_EVENTS
    assert EVENT_PLAYER_DEFEAT in PLAYER_EVENTS
    assert EVENT_GAME_TIMER_EXPIRED in GAME_EVENTS

    # 验证ALL_EVENTS包含所有事件
    assert EVENT_PLAYER_UNIT_DEATH in ALL_EVENTS
    assert EVENT_UNIT_DEATH in ALL_EVENTS
    assert EVENT_PLAYER_DEFEAT in ALL_EVENTS
    assert EVENT_GAME_TIMER_EXPIRED in ALL_EVENTS
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/trigger/test_event_types.py::test_event_type_constants -v`
Expected: FAIL with "ModuleNotFoundError: No module named 'jass_runner.trigger.event_types'"

**Step 3: Write minimal implementation**

```python
"""JASS触发器事件类型定义。

此模块包含所有支持的触发器事件类型常量。
"""

# 玩家-单位事件 (EVENT_PLAYER_UNIT_*)
EVENT_PLAYER_UNIT_DEATH = "EVENT_PLAYER_UNIT_DEATH"
EVENT_PLAYER_UNIT_ATTACKED = "EVENT_PLAYER_UNIT_ATTACKED"
EVENT_PLAYER_UNIT_SPELL_EFFECT = "EVENT_PLAYER_UNIT_SPELL_EFFECT"
EVENT_PLAYER_UNIT_DAMAGED = "EVENT_PLAYER_UNIT_DAMAGED"
EVENT_PLAYER_UNIT_PICKUP_ITEM = "EVENT_PLAYER_UNIT_PICKUP_ITEM"
EVENT_PLAYER_UNIT_DROP_ITEM = "EVENT_PLAYER_UNIT_DROP_ITEM"
EVENT_PLAYER_UNIT_USE_ITEM = "EVENT_PLAYER_UNIT_USE_ITEM"
EVENT_PLAYER_UNIT_ISSUED_ORDER = "EVENT_PLAYER_UNIT_ISSUED_ORDER"

# 通用单位事件 (EVENT_UNIT_*)
EVENT_UNIT_DEATH = "EVENT_UNIT_DEATH"
EVENT_UNIT_DAMAGED = "EVENT_UNIT_DAMAGED"

# 玩家事件 (EVENT_PLAYER_*)
EVENT_PLAYER_DEFEAT = "EVENT_PLAYER_DEFEAT"
EVENT_PLAYER_VICTORY = "EVENT_PLAYER_VICTORY"
EVENT_PLAYER_LEAVE = "EVENT_PLAYER_LEAVE"
EVENT_PLAYER_CHAT = "EVENT_PLAYER_CHAT"

# 游戏事件 (EVENT_GAME_*)
EVENT_GAME_TIMER_EXPIRED = "EVENT_GAME_TIMER_EXPIRED"

# 事件分类列表
PLAYER_UNIT_EVENTS = [
    EVENT_PLAYER_UNIT_DEATH,
    EVENT_PLAYER_UNIT_ATTACKED,
    EVENT_PLAYER_UNIT_SPELL_EFFECT,
    EVENT_PLAYER_UNIT_DAMAGED,
    EVENT_PLAYER_UNIT_PICKUP_ITEM,
    EVENT_PLAYER_UNIT_DROP_ITEM,
    EVENT_PLAYER_UNIT_USE_ITEM,
    EVENT_PLAYER_UNIT_ISSUED_ORDER,
]

UNIT_EVENTS = [
    EVENT_UNIT_DEATH,
    EVENT_UNIT_DAMAGED,
]

PLAYER_EVENTS = [
    EVENT_PLAYER_DEFEAT,
    EVENT_PLAYER_VICTORY,
    EVENT_PLAYER_LEAVE,
    EVENT_PLAYER_CHAT,
]

GAME_EVENTS = [
    EVENT_GAME_TIMER_EXPIRED,
]

ALL_EVENTS = PLAYER_UNIT_EVENTS + UNIT_EVENTS + PLAYER_EVENTS + GAME_EVENTS
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/trigger/test_event_types.py::test_event_type_constants -v`
Expected: PASS

**Step 5: Commit**

```bash
git add tests/trigger/test_event_types.py src/jass_runner/trigger/event_types.py
git commit -m "feat(trigger): add event type constants"
```

---

### Task 2: 创建Trigger类

**Files:**
- Create: `src/jass_runner/trigger/trigger.py`
- Test: `tests/trigger/test_trigger.py`

**Step 1: Write the failing test**

```python
"""Trigger类测试。"""


def test_trigger_creation():
    """测试Trigger创建和基本属性。"""
    from jass_runner.trigger.trigger import Trigger

    trigger = Trigger("trigger_001")

    # 验证基本属性
    assert trigger.trigger_id == "trigger_001"
    assert trigger.enabled is True
    assert trigger.events == []
    assert trigger.conditions == []
    assert trigger.actions == []


def test_trigger_enable_disable():
    """测试Trigger启用和禁用功能。"""
    from jass_runner.trigger.trigger import Trigger

    trigger = Trigger("trigger_002")
    assert trigger.enabled is True

    # 禁用触发器
    trigger.enabled = False
    assert trigger.enabled is False

    # 重新启用
    trigger.enabled = True
    assert trigger.enabled is True


def test_trigger_add_action():
    """测试Trigger添加动作功能。"""
    from jass_runner.trigger.trigger import Trigger

    trigger = Trigger("trigger_003")

    # 定义测试动作函数
    def test_action():
        return "action executed"

    # 添加动作
    action_handle = trigger.add_action(test_action)

    # 验证动作已添加
    assert len(trigger.actions) == 1
    assert trigger.actions[0]["handle"] == action_handle
    assert trigger.actions[0]["func"] == test_action

    # 验证handle格式
    assert isinstance(action_handle, str)
    assert action_handle.startswith("action_")


def test_trigger_remove_action():
    """测试Trigger移除动作功能。"""
    from jass_runner.trigger.trigger import Trigger

    trigger = Trigger("trigger_004")

    def test_action():
        pass

    # 添加并移除动作
    action_handle = trigger.add_action(test_action)
    result = trigger.remove_action(action_handle)

    # 验证移除成功
    assert result is True
    assert len(trigger.actions) == 0

    # 验证移除不存在的动作返回False
    result = trigger.remove_action("nonexistent")
    assert result is False


def test_trigger_add_condition():
    """测试Trigger添加条件功能。"""
    from jass_runner.trigger.trigger import Trigger

    trigger = Trigger("trigger_005")

    # 定义测试条件函数
    def test_condition():
        return True

    # 添加条件
    condition_handle = trigger.add_condition(test_condition)

    # 验证条件已添加
    assert len(trigger.conditions) == 1
    assert trigger.conditions[0]["handle"] == condition_handle
    assert trigger.conditions[0]["func"] == test_condition


def test_trigger_remove_condition():
    """测试Trigger移除条件功能。"""
    from jass_runner.trigger.trigger import Trigger

    trigger = Trigger("trigger_006")

    def test_condition():
        return True

    # 添加并移除条件
    condition_handle = trigger.add_condition(test_condition)
    result = trigger.remove_condition(condition_handle)

    # 验证移除成功
    assert result is True
    assert len(trigger.conditions) == 0

    # 验证移除不存在的条件返回False
    result = trigger.remove_condition("nonexistent")
    assert result is False


def test_trigger_register_event():
    """测试Trigger注册事件功能。"""
    from jass_runner.trigger.trigger import Trigger
    from jass_runner.trigger.event_types import EVENT_UNIT_DEATH

    trigger = Trigger("trigger_007")

    # 注册事件
    event_handle = trigger.register_event(EVENT_UNIT_DEATH, {"unit_type": "hfoo"})

    # 验证事件已注册
    assert len(trigger.events) == 1
    assert trigger.events[0]["handle"] == event_handle
    assert trigger.events[0]["type"] == EVENT_UNIT_DEATH
    assert trigger.events[0]["filter"] == {"unit_type": "hfoo"}


def test_trigger_clear_events():
    """测试Trigger清空事件功能。"""
    from jass_runner.trigger.trigger import Trigger
    from jass_runner.trigger.event_types import EVENT_UNIT_DEATH, EVENT_PLAYER_DEFEAT

    trigger = Trigger("trigger_008")

    # 注册多个事件
    trigger.register_event(EVENT_UNIT_DEATH, None)
    trigger.register_event(EVENT_PLAYER_DEFEAT, None)

    # 验证事件已注册
    assert len(trigger.events) == 2

    # 清空事件
    trigger.clear_events()

    # 验证事件已清空
    assert len(trigger.events) == 0


def test_trigger_evaluate_conditions_all_true():
    """测试Trigger条件评估 - 所有条件为True。"""
    from jass_runner.trigger.trigger import Trigger

    trigger = Trigger("trigger_009")

    # 添加条件（都返回True）
    trigger.add_condition(lambda: True)
    trigger.add_condition(lambda: True)

    # 评估条件
    result = trigger.evaluate_conditions({})

    # 验证结果为True
    assert result is True


def test_trigger_evaluate_conditions_one_false():
    """测试Trigger条件评估 - 任一条件为False。"""
    from jass_runner.trigger.trigger import Trigger

    trigger = Trigger("trigger_010")

    # 添加条件（一个返回False）
    trigger.add_condition(lambda: True)
    trigger.add_condition(lambda: False)

    # 评估条件
    result = trigger.evaluate_conditions({})

    # 验证结果为False
    assert result is False


def test_trigger_evaluate_conditions_no_conditions():
    """测试Trigger条件评估 - 无条件时默认通过。"""
    from jass_runner.trigger.trigger import Trigger

    trigger = Trigger("trigger_011")

    # 不添加任何条件
    result = trigger.evaluate_conditions({})

    # 验证结果为True（无条件时默认通过）
    assert result is True


def test_trigger_execute_actions():
    """测试Trigger动作执行。"""
    from jass_runner.trigger.trigger import Trigger

    trigger = Trigger("trigger_012")

    # 记录执行顺序
    execution_order = []

    def action1():
        execution_order.append(1)

    def action2():
        execution_order.append(2)

    # 添加动作
    trigger.add_action(action1)
    trigger.add_action(action2)

    # 执行动作
    trigger.execute_actions({})

    # 验证执行顺序
    assert execution_order == [1, 2]


def test_trigger_execute_actions_empty():
    """测试Trigger动作执行 - 无动作时不报错。"""
    from jass_runner.trigger.trigger import Trigger

    trigger = Trigger("trigger_013")

    # 不添加任何动作，执行不应报错
    trigger.execute_actions({})

    # 验证无异常抛出
    assert True
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/trigger/test_trigger.py::test_trigger_creation -v`
Expected: FAIL with "ModuleNotFoundError: No module named 'jass_runner.trigger.trigger'"

**Step 3: Write minimal implementation**

```python
"""JASS触发器类。

此模块包含Trigger类，管理单个触发器的事件、条件和动作。
"""

import uuid
from typing import Any, Callable, Dict, List, Optional


class Trigger:
    """单个JASS触发器。

    管理触发器的事件注册、条件评估和动作执行。

    属性：
        trigger_id: 唯一标识符
        events: 注册的事件列表
        conditions: 条件函数列表
        actions: 动作函数列表
        enabled: 是否启用
    """

    def __init__(self, trigger_id: str):
        """初始化触发器。

        参数：
            trigger_id: 触发器唯一标识符
        """
        self.trigger_id = trigger_id
        self.events: List[Dict[str, Any]] = []
        self.conditions: List[Dict[str, Any]] = []
        self.actions: List[Dict[str, Any]] = []
        self.enabled = True

    def add_action(self, action_func: Callable) -> str:
        """添加动作函数。

        参数：
            action_func: 动作函数

        返回：
            动作handle
        """
        handle = f"action_{uuid.uuid4().hex[:8]}"
        self.actions.append({"handle": handle, "func": action_func})
        return handle

    def remove_action(self, action_handle: str) -> bool:
        """移除指定动作。

        参数：
            action_handle: 动作handle

        返回：
            是否成功移除
        """
        for i, action in enumerate(self.actions):
            if action["handle"] == action_handle:
                self.actions.pop(i)
                return True
        return False

    def clear_actions(self):
        """清空所有动作。"""
        self.actions.clear()

    def add_condition(self, condition_func: Callable) -> str:
        """添加条件函数。

        参数：
            condition_func: 条件函数，返回布尔值

        返回：
            条件handle
        """
        handle = f"condition_{uuid.uuid4().hex[:8]}"
        self.conditions.append({"handle": handle, "func": condition_func})
        return handle

    def remove_condition(self, condition_handle: str) -> bool:
        """移除指定条件。

        参数：
            condition_handle: 条件handle

        返回：
            是否成功移除
        """
        for i, condition in enumerate(self.conditions):
            if condition["handle"] == condition_handle:
                self.conditions.pop(i)
                return True
        return False

    def clear_conditions(self):
        """清空所有条件。"""
        self.conditions.clear()

    def register_event(self, event_type: str, filter_data: Optional[Dict]) -> str:
        """注册事件。

        参数：
            event_type: 事件类型
            filter_data: 过滤数据

        返回：
            事件handle
        """
        handle = f"event_{uuid.uuid4().hex[:8]}"
        self.events.append({
            "handle": handle,
            "type": event_type,
            "filter": filter_data
        })
        return handle

    def clear_events(self):
        """清空所有事件。"""
        self.events.clear()

    def evaluate_conditions(self, state_context: Dict) -> bool:
        """评估所有条件。

        参数：
            state_context: 状态上下文

        返回：
            所有条件都为True时返回True
        """
        if not self.conditions:
            return True

        for condition in self.conditions:
            try:
                result = condition["func"]()
                if not result:
                    return False
            except Exception:
                # 条件执行异常视为失败
                return False

        return True

    def execute_actions(self, state_context: Dict):
        """执行所有动作。

        参数：
            state_context: 状态上下文
        """
        for action in self.actions:
            try:
                action["func"]()
            except Exception:
                # 动作执行异常继续执行下一个
                pass
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/trigger/test_trigger.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add tests/trigger/test_trigger.py src/jass_runner/trigger/trigger.py
git commit -m "feat(trigger): add Trigger class with events, conditions and actions"
```

---

### Task 3: 创建TriggerManager类

**Files:**
- Create: `src/jass_runner/trigger/manager.py`
- Test: `tests/trigger/test_trigger_manager.py`

**Step 1: Write the failing test**

```python
"""TriggerManager类测试。"""


def test_trigger_manager_creation():
    """测试TriggerManager创建。"""
    from jass_runner.trigger.manager import TriggerManager

    manager = TriggerManager()

    # 验证初始状态
    assert manager._triggers == {}
    assert manager._event_index == {}
    assert manager._global_enabled is True


def test_trigger_manager_create_trigger():
    """测试TriggerManager创建触发器。"""
    from jass_runner.trigger.manager import TriggerManager

    manager = TriggerManager()

    # 创建触发器
    trigger_id = manager.create_trigger()

    # 验证返回的ID格式
    assert isinstance(trigger_id, str)
    assert trigger_id.startswith("trigger_")

    # 验证触发器已注册
    trigger = manager.get_trigger(trigger_id)
    assert trigger is not None
    assert trigger.trigger_id == trigger_id
    assert trigger.enabled is True


def test_trigger_manager_destroy_trigger():
    """测试TriggerManager销毁触发器。"""
    from jass_runner.trigger.manager import TriggerManager

    manager = TriggerManager()

    # 创建并销毁触发器
    trigger_id = manager.create_trigger()
    result = manager.destroy_trigger(trigger_id)

    # 验证销毁成功
    assert result is True
    assert manager.get_trigger(trigger_id) is None

    # 验证销毁不存在的触发器返回False
    result = manager.destroy_trigger("nonexistent")
    assert result is False


def test_trigger_manager_enable_disable_trigger():
    """测试TriggerManager启用/禁用触发器。"""
    from jass_runner.trigger.manager import TriggerManager

    manager = TriggerManager()
    trigger_id = manager.create_trigger()

    # 验证初始状态为启用
    assert manager.is_trigger_enabled(trigger_id) is True

    # 禁用触发器
    result = manager.disable_trigger(trigger_id)
    assert result is True
    assert manager.is_trigger_enabled(trigger_id) is False

    # 启用触发器
    result = manager.enable_trigger(trigger_id)
    assert result is True
    assert manager.is_trigger_enabled(trigger_id) is True

    # 验证操作不存在的触发器返回False
    assert manager.disable_trigger("nonexistent") is False
    assert manager.enable_trigger("nonexistent") is False
    assert manager.is_trigger_enabled("nonexistent") is False


def test_trigger_manager_register_event():
    """测试TriggerManager注册事件。"""
    from jass_runner.trigger.manager import TriggerManager
    from jass_runner.trigger.event_types import EVENT_UNIT_DEATH

    manager = TriggerManager()
    trigger_id = manager.create_trigger()

    # 注册事件
    event_handle = manager.register_event(trigger_id, EVENT_UNIT_DEATH, {"unit_type": "hfoo"})

    # 验证事件handle
    assert isinstance(event_handle, str)

    # 验证事件索引
    assert EVENT_UNIT_DEATH in manager._event_index
    assert trigger_id in manager._event_index[EVENT_UNIT_DEATH]

    # 验证触发器上的事件
    trigger = manager.get_trigger(trigger_id)
    assert len(trigger.events) == 1


def test_trigger_manager_clear_trigger_events():
    """测试TriggerManager清空触发器事件。"""
    from jass_runner.trigger.manager import TriggerManager
    from jass_runner.trigger.event_types import EVENT_UNIT_DEATH, EVENT_PLAYER_DEFEAT

    manager = TriggerManager()
    trigger_id = manager.create_trigger()

    # 注册多个事件
    manager.register_event(trigger_id, EVENT_UNIT_DEATH, None)
    manager.register_event(trigger_id, EVENT_PLAYER_DEFEAT, None)

    # 验证事件已注册
    trigger = manager.get_trigger(trigger_id)
    assert len(trigger.events) == 2
    assert EVENT_UNIT_DEATH in manager._event_index

    # 清空事件
    result = manager.clear_trigger_events(trigger_id)
    assert result is True

    # 验证事件已清空
    assert len(trigger.events) == 0
    assert trigger_id not in manager._event_index.get(EVENT_UNIT_DEATH, [])

    # 验证清空不存在的触发器返回False
    assert manager.clear_trigger_events("nonexistent") is False


def test_trigger_manager_fire_event_no_match():
    """测试TriggerManager触发事件 - 无匹配触发器。"""
    from jass_runner.trigger.manager import TriggerManager
    from jass_runner.trigger.event_types import EVENT_UNIT_DEATH

    manager = TriggerManager()

    # 触发事件（无注册触发器）
    manager.fire_event(EVENT_UNIT_DEATH, {"unit_id": "unit_001"})

    # 验证无异常抛出
    assert True


def test_trigger_manager_fire_event_with_match():
    """测试TriggerManager触发事件 - 有匹配触发器。"""
    from jass_runner.trigger.manager import TriggerManager
    from jass_runner.trigger.event_types import EVENT_UNIT_DEATH

    manager = TriggerManager()
    trigger_id = manager.create_trigger()

    # 记录动作执行
    action_executed = []

    def test_action():
        action_executed.append(True)

    # 注册事件和动作
    manager.register_event(trigger_id, EVENT_UNIT_DEATH, None)
    trigger = manager.get_trigger(trigger_id)
    trigger.add_action(test_action)

    # 触发事件
    manager.fire_event(EVENT_UNIT_DEATH, {"unit_id": "unit_001"})

    # 验证动作已执行
    assert len(action_executed) == 1


def test_trigger_manager_fire_event_disabled_trigger():
    """测试TriggerManager触发事件 - 禁用触发器不执行。"""
    from jass_runner.trigger.manager import TriggerManager
    from jass_runner.trigger.event_types import EVENT_UNIT_DEATH

    manager = TriggerManager()
    trigger_id = manager.create_trigger()

    action_executed = []

    def test_action():
        action_executed.append(True)

    # 注册事件和动作，然后禁用触发器
    manager.register_event(trigger_id, EVENT_UNIT_DEATH, None)
    trigger = manager.get_trigger(trigger_id)
    trigger.add_action(test_action)
    manager.disable_trigger(trigger_id)

    # 触发事件
    manager.fire_event(EVENT_UNIT_DEATH, {"unit_id": "unit_001"})

    # 验证动作未执行
    assert len(action_executed) == 0


def test_trigger_manager_fire_event_condition_filter():
    """测试TriggerManager触发事件 - 条件过滤。"""
    from jass_runner.trigger.manager import TriggerManager
    from jass_runner.trigger.event_types import EVENT_UNIT_DEATH

    manager = TriggerManager()
    trigger_id = manager.create_trigger()

    action_executed = []

    def test_action():
        action_executed.append(True)

    def false_condition():
        return False

    # 注册事件、条件和动作
    manager.register_event(trigger_id, EVENT_UNIT_DEATH, None)
    trigger = manager.get_trigger(trigger_id)
    trigger.add_condition(false_condition)
    trigger.add_action(test_action)

    # 触发事件
    manager.fire_event(EVENT_UNIT_DEATH, {"unit_id": "unit_001"})

    # 验证动作未执行（条件过滤）
    assert len(action_executed) == 0


def test_trigger_manager_fire_event_multiple_triggers():
    """测试TriggerManager触发事件 - 多个触发器。"""
    from jass_runner.trigger.manager import TriggerManager
    from jass_runner.trigger.event_types import EVENT_UNIT_DEATH

    manager = TriggerManager()

    trigger_id1 = manager.create_trigger()
    trigger_id2 = manager.create_trigger()

    actions_executed = []

    def action1():
        actions_executed.append("action1")

    def action2():
        actions_executed.append("action2")

    # 为两个触发器注册相同事件
    manager.register_event(trigger_id1, EVENT_UNIT_DEATH, None)
    manager.register_event(trigger_id2, EVENT_UNIT_DEATH, None)

    trigger1 = manager.get_trigger(trigger_id1)
    trigger2 = manager.get_trigger(trigger_id2)
    trigger1.add_action(action1)
    trigger2.add_action(action2)

    # 触发事件
    manager.fire_event(EVENT_UNIT_DEATH, {"unit_id": "unit_001"})

    # 验证两个动作都执行
    assert "action1" in actions_executed
    assert "action2" in actions_executed
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/trigger/test_trigger_manager.py::test_trigger_manager_creation -v`
Expected: FAIL with "ModuleNotFoundError: No module named 'jass_runner.trigger.manager'"

**Step 3: Write minimal implementation**

```python
"""JASS触发器管理器。

此模块包含TriggerManager类，管理所有触发器的生命周期和事件分发。
"""

import uuid
from typing import Any, Dict, List, Optional

from .trigger import Trigger


class TriggerManager:
    """触发器管理器。

    负责所有触发器的生命周期管理和事件分发。

    属性：
        _triggers: 所有触发器的映射
        _event_index: 事件到触发器ID的索引
        _global_enabled: 全局启用状态
    """

    def __init__(self):
        """初始化触发器管理器。"""
        self._triggers: Dict[str, Trigger] = {}
        self._event_index: Dict[str, List[str]] = {}
        self._global_enabled = True
        self._next_id = 1

    def _generate_trigger_id(self) -> str:
        """生成唯一的触发器ID。"""
        trigger_id = f"trigger_{self._next_id}"
        self._next_id += 1
        return trigger_id

    def create_trigger(self) -> str:
        """创建新触发器。

        返回：
            新触发器的ID
        """
        trigger_id = self._generate_trigger_id()
        trigger = Trigger(trigger_id)
        self._triggers[trigger_id] = trigger
        return trigger_id

    def destroy_trigger(self, trigger_id: str) -> bool:
        """销毁触发器。

        参数：
            trigger_id: 触发器ID

        返回：
            是否成功销毁
        """
        if trigger_id not in self._triggers:
            return False

        # 从事件索引中移除
        trigger = self._triggers[trigger_id]
        for event in trigger.events:
            event_type = event["type"]
            if event_type in self._event_index:
                if trigger_id in self._event_index[event_type]:
                    self._event_index[event_type].remove(trigger_id)

        # 删除触发器
        del self._triggers[trigger_id]
        return True

    def enable_trigger(self, trigger_id: str) -> bool:
        """启用触发器。

        参数：
            trigger_id: 触发器ID

        返回：
            是否成功启用
        """
        trigger = self._triggers.get(trigger_id)
        if trigger:
            trigger.enabled = True
            return True
        return False

    def disable_trigger(self, trigger_id: str) -> bool:
        """禁用触发器。

        参数：
            trigger_id: 触发器ID

        返回：
            是否成功禁用
        """
        trigger = self._triggers.get(trigger_id)
        if trigger:
            trigger.enabled = False
            return True
        return False

    def is_trigger_enabled(self, trigger_id: str) -> bool:
        """检查触发器是否启用。

        参数：
            trigger_id: 触发器ID

        返回：
            触发器是否启用
        """
        trigger = self._triggers.get(trigger_id)
        if trigger:
            return trigger.enabled
        return False

    def get_trigger(self, trigger_id: str) -> Optional[Trigger]:
        """获取触发器对象。

        参数：
            trigger_id: 触发器ID

        返回：
            触发器对象或None
        """
        return self._triggers.get(trigger_id)

    def register_event(self, trigger_id: str, event_type: str,
                       filter_data: Optional[Dict]) -> Optional[str]:
        """为触发器注册事件。

        参数：
            trigger_id: 触发器ID
            event_type: 事件类型
            filter_data: 过滤数据

        返回：
            事件handle或None
        """
        trigger = self._triggers.get(trigger_id)
        if not trigger:
            return None

        # 在触发器上注册事件
        event_handle = trigger.register_event(event_type, filter_data)

        # 更新事件索引
        if event_type not in self._event_index:
            self._event_index[event_type] = []
        if trigger_id not in self._event_index[event_type]:
            self._event_index[event_type].append(trigger_id)

        return event_handle

    def clear_trigger_events(self, trigger_id: str) -> bool:
        """清空触发器的所有事件。

        参数：
            trigger_id: 触发器ID

        返回：
            是否成功清空
        """
        trigger = self._triggers.get(trigger_id)
        if not trigger:
            return False

        # 从事件索引中移除
        for event in trigger.events:
            event_type = event["type"]
            if event_type in self._event_index:
                if trigger_id in self._event_index[event_type]:
                    self._event_index[event_type].remove(trigger_id)

        # 清空触发器的事件
        trigger.clear_events()
        return True

    def fire_event(self, event_type: str, event_data: Dict[str, Any]):
        """触发事件。

        参数：
            event_type: 事件类型
            event_data: 事件数据
        """
        if not self._global_enabled:
            return

        # 获取候选触发器列表
        candidate_ids = self._event_index.get(event_type, [])

        for trigger_id in candidate_ids:
            trigger = self._triggers.get(trigger_id)
            if not trigger:
                continue

            # 检查触发器是否启用
            if not trigger.enabled:
                continue

            # 评估条件
            if not trigger.evaluate_conditions(event_data):
                continue

            # 执行动作
            trigger.execute_actions(event_data)
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/trigger/test_trigger_manager.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add tests/trigger/test_trigger_manager.py src/jass_runner/trigger/manager.py
git commit -m "feat(trigger): add TriggerManager class for lifecycle and event dispatch"
```

---

### Task 4: 创建trigger模块初始化文件

**Files:**
- Create: `src/jass_runner/trigger/__init__.py`
- Test: `tests/trigger/test_trigger_imports.py`

**Step 1: Write the failing test**

```python
"""trigger模块导入测试。"""


def test_trigger_module_imports():
    """测试trigger模块的所有导出。"""
    from jass_runner.trigger import (
        Trigger,
        TriggerManager,
        EVENT_PLAYER_UNIT_DEATH,
        EVENT_UNIT_DEATH,
        EVENT_PLAYER_DEFEAT,
        EVENT_GAME_TIMER_EXPIRED,
        PLAYER_UNIT_EVENTS,
        ALL_EVENTS,
    )

    # 验证类型
    assert Trigger is not None
    assert TriggerManager is not None
    assert isinstance(EVENT_PLAYER_UNIT_DEATH, str)
    assert isinstance(EVENT_UNIT_DEATH, str)
    assert isinstance(EVENT_PLAYER_DEFEAT, str)
    assert isinstance(EVENT_GAME_TIMER_EXPIRED, str)
    assert isinstance(PLAYER_UNIT_EVENTS, list)
    assert isinstance(ALL_EVENTS, list)
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/trigger/test_trigger_imports.py::test_trigger_module_imports -v`
Expected: FAIL with "ModuleNotFoundError: No module named 'jass_runner.trigger'"

**Step 3: Write minimal implementation**

```python
"""JASS触发器系统。

此包包含JASS触发器系统的实现，包括事件管理、条件评估和动作执行。
"""

from .trigger import Trigger
from .manager import TriggerManager
from .event_types import (
    EVENT_PLAYER_UNIT_DEATH,
    EVENT_PLAYER_UNIT_ATTACKED,
    EVENT_PLAYER_UNIT_SPELL_EFFECT,
    EVENT_PLAYER_UNIT_DAMAGED,
    EVENT_PLAYER_UNIT_PICKUP_ITEM,
    EVENT_PLAYER_UNIT_DROP_ITEM,
    EVENT_PLAYER_UNIT_USE_ITEM,
    EVENT_PLAYER_UNIT_ISSUED_ORDER,
    EVENT_UNIT_DEATH,
    EVENT_UNIT_DAMAGED,
    EVENT_PLAYER_DEFEAT,
    EVENT_PLAYER_VICTORY,
    EVENT_PLAYER_LEAVE,
    EVENT_PLAYER_CHAT,
    EVENT_GAME_TIMER_EXPIRED,
    PLAYER_UNIT_EVENTS,
    UNIT_EVENTS,
    PLAYER_EVENTS,
    GAME_EVENTS,
    ALL_EVENTS,
)

__all__ = [
    "Trigger",
    "TriggerManager",
    "EVENT_PLAYER_UNIT_DEATH",
    "EVENT_PLAYER_UNIT_ATTACKED",
    "EVENT_PLAYER_UNIT_SPELL_EFFECT",
    "EVENT_PLAYER_UNIT_DAMAGED",
    "EVENT_PLAYER_UNIT_PICKUP_ITEM",
    "EVENT_PLAYER_UNIT_DROP_ITEM",
    "EVENT_PLAYER_UNIT_USE_ITEM",
    "EVENT_PLAYER_UNIT_ISSUED_ORDER",
    "EVENT_UNIT_DEATH",
    "EVENT_UNIT_DAMAGED",
    "EVENT_PLAYER_DEFEAT",
    "EVENT_PLAYER_VICTORY",
    "EVENT_PLAYER_LEAVE",
    "EVENT_PLAYER_CHAT",
    "EVENT_GAME_TIMER_EXPIRED",
    "PLAYER_UNIT_EVENTS",
    "UNIT_EVENTS",
    "PLAYER_EVENTS",
    "GAME_EVENTS",
    "ALL_EVENTS",
]
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/trigger/test_trigger_imports.py::test_trigger_module_imports -v`
Expected: PASS

**Step 5: Commit**

```bash
git add tests/trigger/test_trigger_imports.py src/jass_runner/trigger/__init__.py
git commit -m "feat(trigger): add trigger module exports"
```

---

### Task 5: 运行阶段1完整测试套件

**Files:**
- Test: 所有阶段1相关测试文件

**Step 1: 运行所有阶段1测试**

Run: `pytest tests/trigger/test_event_types.py tests/trigger/test_trigger.py tests/trigger/test_trigger_manager.py tests/trigger/test_trigger_imports.py -v`
Expected: 所有测试通过

**Step 2: 验证测试覆盖率**

Run: `pytest --cov=src/jass_runner/trigger --cov-report=term-missing tests/trigger/`
Expected: 显示覆盖率报告，关键模块应达到90%以上

**Step 3: 运行完整项目测试确保无回归**

Run: `pytest tests/ -v`
Expected: 所有现有测试通过，无回归

**Step 4: 提交最终状态**

```bash
git add .
git commit -m "feat(trigger): complete phase 1 - core trigger components"
```

---

## 阶段1完成标准

1. **事件类型定义**：所有12个标准事件类型常量定义完成
2. **Trigger类**：支持事件注册、条件评估、动作执行
3. **TriggerManager类**：支持触发器生命周期管理和事件分发
4. **模块导出**：trigger包导出所有公共API
5. **完整测试覆盖**：单元测试覆盖所有功能
6. **无回归**：所有现有测试通过

## 下一阶段

阶段2将实现20个触发器相关的native函数。
计划保存为：`docs/plans/2026-03-01-trigger-system-phase2-natives.md`
