# Unit Slots Native Functions Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 实现 SetAllItemTypeSlots, SetAllUnitTypeSlots, SetItemTypeSlots, SetUnitTypeSlots 四个 native 函数

**Architecture:** 在 Unit 类中添加全局变量和槽位属性，新建 unit_slots_natives.py 模块实现四个 native 函数，支持截断逻辑

**Tech Stack:** Python 3.8+, pytest, 现有 JASS Runner 框架

---

## Task 1: 修改 Unit 类添加全局变量和槽位属性

**Files:**
- Modify: `src/jass_runner/natives/unit.py`

**Step 1: 添加全局变量**

在 `unit.py` 文件顶部（类定义之前）添加：
```python
# 技能格子槽位全局最大值（默认11）
MAX_ITEM_TYPE_SLOTS = 11
MAX_UNIT_TYPE_SLOTS = 11
```

**Step 2: 在 Unit.__init__ 中添加槽位属性**

在 `__init__` 方法中（inventory 属性之后）添加：
```python
# 技能格子槽位配置（用于商店出售物品/单位）
self._item_type_slots = MAX_ITEM_TYPE_SLOTS  # 出售物品的槽位数
self._unit_type_slots = MAX_UNIT_TYPE_SLOTS  # 出售单位的槽位数
```

**Step 3: 添加设置方法**

在 Unit 类中添加两个方法：
```python
def set_item_type_slots(self, slots: int) -> int:
    """设置技能格子中出售物品的槽位数。

    参数：
        slots: 期望的槽位数

    返回：
        实际设置的槽位数（会被截断到 0-MAX_ITEM_TYPE_SLOTS 范围）
    """
    actual_slots = max(0, min(slots, MAX_ITEM_TYPE_SLOTS))
    self._item_type_slots = actual_slots
    return actual_slots

def set_unit_type_slots(self, slots: int) -> int:
    """设置技能格子中出售单位的槽位数。

    参数：
        slots: 期望的槽位数

    返回：
        实际设置的槽位数（会被截断到 0-MAX_UNIT_TYPE_SLOTS 范围）
    """
    actual_slots = max(0, min(slots, MAX_UNIT_TYPE_SLOTS))
    self._unit_type_slots = actual_slots
    return actual_slots
```

**Step 4: 验证修改**

Run: `python -c "from src.jass_runner.natives.unit import Unit, MAX_ITEM_TYPE_SLOTS, MAX_UNIT_TYPE_SLOTS; print(f'MAX_ITEM_TYPE_SLOTS={MAX_ITEM_TYPE_SLOTS}'); print(f'MAX_UNIT_TYPE_SLOTS={MAX_UNIT_TYPE_SLOTS}')"`
Expected:
```
MAX_ITEM_TYPE_SLOTS=11
MAX_UNIT_TYPE_SLOTS=11
```

Run: `python -c "from src.jass_runner.natives.unit import Unit; u = Unit('u1', 'hfoo', 0, 0, 0); print(f'item_slots={u._item_type_slots}'); print(f'unit_slots={u._unit_type_slots}')"`
Expected:
```
item_slots=11
unit_slots=11
```

**Step 5: Commit**

```bash
git add src/jass_runner/natives/unit.py
git commit -m "feat(unit): 添加技能格子槽位全局变量和设置方法"
```

---

## Task 2: 创建 unit_slots_natives.py 模块

**Files:**
- Create: `src/jass_runner/natives/unit_slots_natives.py`

**Step 1: 编写模块代码**

```python
"""单位技能格子槽位相关 native 函数实现。

此模块包含与单位技能格子槽位设置相关的 JASS native 函数。
"""

import logging
from typing import TYPE_CHECKING

from .base import NativeFunction
from .unit import MAX_ITEM_TYPE_SLOTS, MAX_UNIT_TYPE_SLOTS

if TYPE_CHECKING:
    from .state import StateContext
    from .handle import Unit

logger = logging.getLogger(__name__)


class SetAllItemTypeSlots(NativeFunction):
    """设置全局物品类型最大槽位数。"""

    @property
    def name(self) -> str:
        return "SetAllItemTypeSlots"

    def execute(self, state_context: 'StateContext', slots: int) -> int:
        """执行 SetAllItemTypeSlots native 函数。

        参数：
            state_context: 状态上下文
            slots: 期望的最大槽位数

        返回：
            实际设置的最大槽位数（会被截断到 0-11 范围）
        """
        global MAX_ITEM_TYPE_SLOTS
        actual_slots = max(0, min(slots, 11))
        MAX_ITEM_TYPE_SLOTS = actual_slots
        logger.info(f"[SetAllItemTypeSlots] 设置全局物品类型最大槽位数为: {actual_slots}")
        return actual_slots


class SetAllUnitTypeSlots(NativeFunction):
    """设置全局单位类型最大槽位数。"""

    @property
    def name(self) -> str:
        return "SetAllUnitTypeSlots"

    def execute(self, state_context: 'StateContext', slots: int) -> int:
        """执行 SetAllUnitTypeSlots native 函数。

        参数：
            state_context: 状态上下文
            slots: 期望的最大槽位数

        返回：
            实际设置的最大槽位数（会被截断到 0-11 范围）
        """
        global MAX_UNIT_TYPE_SLOTS
        actual_slots = max(0, min(slots, 11))
        MAX_UNIT_TYPE_SLOTS = actual_slots
        logger.info(f"[SetAllUnitTypeSlots] 设置全局单位类型最大槽位数为: {actual_slots}")
        return actual_slots


class SetItemTypeSlots(NativeFunction):
    """为单位设置技能格子中出售物品的槽位数。"""

    @property
    def name(self) -> str:
        return "SetItemTypeSlots"

    def execute(self, state_context: 'StateContext', unit: 'Unit', slots: int) -> int:
        """执行 SetItemTypeSlots native 函数。

        参数：
            state_context: 状态上下文
            unit: 单位对象
            slots: 期望的槽位数

        返回：
            实际设置的槽位数（会被截断到 0-MAX_ITEM_TYPE_SLOTS 范围）
        """
        if unit is None:
            logger.warning("[SetItemTypeSlots] 单位对象为 None")
            return 0

        actual_slots = unit.set_item_type_slots(slots)
        logger.info(f"[SetItemTypeSlots] 单位{unit.id} 设置物品类型槽位数为: {actual_slots}")
        return actual_slots


class SetUnitTypeSlots(NativeFunction):
    """为单位设置技能格子中出售单位的槽位数。"""

    @property
    def name(self) -> str:
        return "SetUnitTypeSlots"

    def execute(self, state_context: 'StateContext', unit: 'Unit', slots: int) -> int:
        """执行 SetUnitTypeSlots native 函数。

        参数：
            state_context: 状态上下文
            unit: 单位对象
            slots: 期望的槽位数

        返回：
            实际设置的槽位数（会被截断到 0-MAX_UNIT_TYPE_SLOTS 范围）
        """
        if unit is None:
            logger.warning("[SetUnitTypeSlots] 单位对象为 None")
            return 0

        actual_slots = unit.set_unit_type_slots(slots)
        logger.info(f"[SetUnitTypeSlots] 单位{unit.id} 设置单位类型槽位数为: {actual_slots}")
        return actual_slots
```

**Step 2: 验证模块可导入**

Run: `python -c "from src.jass_runner.natives.unit_slots_natives import SetAllItemTypeSlots, SetAllUnitTypeSlots, SetItemTypeSlots, SetUnitTypeSlots; print('OK')"`
Expected: `OK`

**Step 3: Commit**

```bash
git add src/jass_runner/natives/unit_slots_natives.py
git commit -m "feat(natives): 实现技能格子槽位相关 native 函数"
```

---

## Task 3: 在工厂中注册新的 native 函数

**Files:**
- Modify: `src/jass_runner/natives/factory.py`

**Step 1: 添加导入语句**

在 player_slot_state_natives 导入后添加：
```python
from .unit_slots_natives import (
    SetAllItemTypeSlots,
    SetAllUnitTypeSlots,
    SetItemTypeSlots,
    SetUnitTypeSlots,
)
```

**Step 2: 注册 native 函数**

在 player_slot_state_natives 注册后添加：
```python
        # 注册技能格子槽位相关 native 函数
        registry.register(SetAllItemTypeSlots())
        registry.register(SetAllUnitTypeSlots())
        registry.register(SetItemTypeSlots())
        registry.register(SetUnitTypeSlots())
```

**Step 3: 验证工厂可正常工作**

Run: `python -c "from src.jass_runner.natives.factory import NativeFactory; f = NativeFactory(); r = f.create_default_registry(); print('SetAllItemTypeSlots' in r._functions); print('SetAllUnitTypeSlots' in r._functions); print('SetItemTypeSlots' in r._functions); print('SetUnitTypeSlots' in r._functions)"`
Expected:
```
True
True
True
True
```

**Step 4: Commit**

```bash
git add src/jass_runner/natives/factory.py
git commit -m "feat(natives): 在工厂中注册技能格子槽位 native 函数"
```

---

## Task 4: 编写单元测试

**Files:**
- Create: `tests/test_unit_slots_natives.py`

**Step 1: 编写测试代码**

```python
"""技能格子槽位 native 函数单元测试。"""

import pytest
from unittest.mock import MagicMock

from jass_runner.natives.unit_slots_natives import (
    SetAllItemTypeSlots,
    SetAllUnitTypeSlots,
    SetItemTypeSlots,
    SetUnitTypeSlots,
)
from jass_runner.natives.unit import MAX_ITEM_TYPE_SLOTS, MAX_UNIT_TYPE_SLOTS


class TestSetAllItemTypeSlots:
    """测试 SetAllItemTypeSlots native 函数。"""

    def test_set_valid_slots(self):
        """测试设置有效的槽位数。"""
        native = SetAllItemTypeSlots()
        mock_context = MagicMock()

        result = native.execute(mock_context, 8)

        assert result == 8

    def test_clamp_to_max(self):
        """测试超过最大值时截断。"""
        native = SetAllItemTypeSlots()
        mock_context = MagicMock()

        result = native.execute(mock_context, 15)

        assert result == 11  # 截断到最大值

    def test_clamp_to_min(self):
        """测试负数时截断到0。"""
        native = SetAllItemTypeSlots()
        mock_context = MagicMock()

        result = native.execute(mock_context, -5)

        assert result == 0


class TestSetAllUnitTypeSlots:
    """测试 SetAllUnitTypeSlots native 函数。"""

    def test_set_valid_slots(self):
        """测试设置有效的槽位数。"""
        native = SetAllUnitTypeSlots()
        mock_context = MagicMock()

        result = native.execute(mock_context, 6)

        assert result == 6

    def test_clamp_to_max(self):
        """测试超过最大值时截断。"""
        native = SetAllUnitTypeSlots()
        mock_context = MagicMock()

        result = native.execute(mock_context, 20)

        assert result == 11  # 截断到最大值


class TestSetItemTypeSlots:
    """测试 SetItemTypeSlots native 函数。"""

    def test_set_valid_slots(self):
        """测试为单位设置有效的槽位数。"""
        native = SetItemTypeSlots()
        mock_context = MagicMock()
        mock_unit = MagicMock()
        mock_unit.id = "unit_001"
        mock_unit.set_item_type_slots.return_value = 5

        result = native.execute(mock_context, mock_unit, 5)

        assert result == 5
        mock_unit.set_item_type_slots.assert_called_once_with(5)

    def test_returns_zero_for_none_unit(self):
        """测试单位对象为None时返回0。"""
        native = SetItemTypeSlots()
        mock_context = MagicMock()

        result = native.execute(mock_context, None, 5)

        assert result == 0


class TestSetUnitTypeSlots:
    """测试 SetUnitTypeSlots native 函数。"""

    def test_set_valid_slots(self):
        """测试为单位设置有效的槽位数。"""
        native = SetUnitTypeSlots()
        mock_context = MagicMock()
        mock_unit = MagicMock()
        mock_unit.id = "unit_002"
        mock_unit.set_unit_type_slots.return_value = 7

        result = native.execute(mock_context, mock_unit, 7)

        assert result == 7
        mock_unit.set_unit_type_slots.assert_called_once_with(7)

    def test_returns_zero_for_none_unit(self):
        """测试单位对象为None时返回0。"""
        native = SetUnitTypeSlots()
        mock_context = MagicMock()

        result = native.execute(mock_context, None, 7)

        assert result == 0
```

**Step 2: 运行测试**

Run: `pytest tests/test_unit_slots_natives.py -v`
Expected: 所有测试通过

**Step 3: Commit**

```bash
git add tests/test_unit_slots_natives.py
git commit -m "test(natives): 添加技能格子槽位 native 函数单元测试"
```

---

## Task 5: 编写集成测试

**Files:**
- Create: `tests/integration/test_unit_slots_integration.py`

**Step 1: 编写集成测试**

```python
"""技能格子槽位 native 函数集成测试。"""

import pytest
from src.jass_runner.natives.unit import Unit, MAX_ITEM_TYPE_SLOTS, MAX_UNIT_TYPE_SLOTS
from src.jass_runner.natives.unit_slots_natives import (
    SetAllItemTypeSlots,
    SetAllUnitTypeSlots,
    SetItemTypeSlots,
    SetUnitTypeSlots,
)


class TestUnitSlotsIntegration:
    """测试技能格子槽位相关 native 函数的集成。"""

    def test_default_slots(self):
        """测试单位默认槽位数为11。"""
        unit = Unit("test_unit", "hfoo", 0, 0, 0)

        assert unit._item_type_slots == 11
        assert unit._unit_type_slots == 11

    def test_set_item_type_slots_within_limit(self):
        """测试在限制范围内设置物品类型槽位。"""
        state_context = None
        unit = Unit("test_unit", "hfoo", 0, 0, 0)

        result = SetItemTypeSlots().execute(state_context, unit, 5)

        assert result == 5
        assert unit._item_type_slots == 5

    def test_set_item_type_slots_clamped(self):
        """测试设置物品类型槽位时截断到全局最大值。"""
        state_context = None
        unit = Unit("test_unit", "hfoo", 0, 0, 0)

        # 先设置全局最大值为8
        SetAllItemTypeSlots().execute(state_context, 8)

        # 尝试设置10，应该被截断到8
        result = SetItemTypeSlots().execute(state_context, unit, 10)

        assert result == 8
        assert unit._item_type_slots == 8

    def test_set_unit_type_slots_within_limit(self):
        """测试在限制范围内设置单位类型槽位。"""
        state_context = None
        unit = Unit("test_unit", "hfoo", 0, 0, 0)

        result = SetUnitTypeSlots().execute(state_context, unit, 6)

        assert result == 6
        assert unit._unit_type_slots == 6

    def test_set_all_item_type_slots_affects_new_units(self):
        """测试设置全局物品类型槽位影响后续单位设置。"""
        state_context = None

        # 设置全局最大值为5
        SetAllItemTypeSlots().execute(state_context, 5)

        # 创建新单位并尝试设置10
        unit = Unit("test_unit", "hfoo", 0, 0, 0)
        result = SetItemTypeSlots().execute(state_context, unit, 10)

        # 应该被截断到5
        assert result == 5
        assert unit._item_type_slots == 5

    def test_clamp_negative_slots(self):
        """测试负数槽位数被截断到0。"""
        state_context = None
        unit = Unit("test_unit", "hfoo", 0, 0, 0)

        result = SetItemTypeSlots().execute(state_context, unit, -3)

        assert result == 0
        assert unit._item_type_slots == 0

    def test_set_all_clamp_to_max(self):
        """测试设置全局槽位时截断到11。"""
        state_context = None

        result = SetAllItemTypeSlots().execute(state_context, 20)

        assert result == 11
```

**Step 2: 运行集成测试**

Run: `pytest tests/integration/test_unit_slots_integration.py -v`
Expected: 所有测试通过

**Step 3: Commit**

```bash
git add tests/integration/test_unit_slots_integration.py
git commit -m "test(integration): 添加技能格子槽位 native 函数集成测试"
```

---

## Task 6: 运行完整测试套件

**Step 1: 运行所有测试**

Run: `pytest tests/ -v --tb=short`
Expected: 所有测试通过

**Step 2: 最终提交**

```bash
git log --oneline -7
```

Expected 提交历史：
```
xxxxxxx test(integration): 添加技能格子槽位 native 函数集成测试
xxxxxxx test(natives): 添加技能格子槽位 native 函数单元测试
xxxxxxx feat(natives): 在工厂中注册技能格子槽位 native 函数
xxxxxxx feat(natives): 实现技能格子槽位相关 native 函数
xxxxxxx feat(unit): 添加技能格子槽位全局变量和设置方法
xxxxxxx docs(plans): 添加技能格子槽位 native 函数设计文档
```
