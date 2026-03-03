# 物品系统实施计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 实现完整的单位背包系统，包含6槽位物品管理和6个Native API函数

**Architecture:** 扩展现有 Unit 类添加 6 槽位 inventory 列表，新建 item_inventory_natives.py 实现 6 个 Native 函数，通过 NativeFactory 注册。

**Tech Stack:** Python 3.8+, pytest, 现有 Handle 系统, 现有 Native 框架

---

## 前置准备

**需要了解的现有代码:**
- `src/jass_runner/natives/handle.py` - 包含 Unit、Item、Player 类定义
- `src/jass_runner/natives/manager.py` - HandleManager 管理创建和销毁
- `src/jass_runner/natives/factory.py` - NativeFactory 注册 Native 函数
- `tests/natives/test_unit_ability.py` - 参考测试风格 (类似功能)

**参考设计文档:** `docs/plans/2026-03-03-item-system-design.md`

---

## Task 1: 扩展 Unit 类添加 Inventory 支持

**Files:**
- Modify: `src/jass_runner/natives/handle.py` (Unit 类)

**Step 1: 查看现有 Unit 类结构**

Run: `head -50 src/jass_runner/natives/handle.py`
Expected: 查看 Unit 类现有定义

**Step 2: 在 Unit.__init__ 中添加 inventory 属性**

在 `__init__` 方法末尾添加（在现有属性之后）:

```python
self.inventory: List[Optional[Item]] = [None] * 6  # 6槽位背包
```

**Step 3: 添加 inventory 操作方法**

在 `__init__` 之后添加以下方法:

```python
    def add_item(self, item: Item, slot: int = -1) -> bool:
        """添加物品到背包，成功返回 True。"""
        if slot >= 0:
            if 0 <= slot < 6 and self.inventory[slot] is None:
                self.inventory[slot] = item
                return True
            return False
        # 自动找空槽
        for i in range(6):
            if self.inventory[i] is None:
                self.inventory[i] = item
                return True
        return False

    def remove_item(self, item: Item) -> bool:
        """从背包移除指定物品，成功返回 True。"""
        for i in range(6):
            if self.inventory[i] is item:
                self.inventory[i] = None
                return True
        return False

    def remove_item_from_slot(self, slot: int) -> bool:
        """从指定槽位移除物品，成功返回 True。"""
        if 0 <= slot < 6 and self.inventory[slot] is not None:
            self.inventory[slot] = None
            return True
        return False

    def get_item_in_slot(self, slot: int) -> Optional[Item]:
        """获取指定槽位的物品。"""
        if 0 <= slot < 6:
            return self.inventory[slot]
        return None

    def find_item(self, item: Item) -> int:
        """查找物品所在槽位，未找到返回 -1。"""
        for i in range(6):
            if self.inventory[i] is item:
                return i
        return -1
```

**Step 4: 验证代码无语法错误**

Run: `python -c "from src.jass_runner.natives.handle import Unit; print('OK')"`
Expected: 显示 "OK"

**Step 5: Commit**

```bash
git add src/jass_runner/natives/handle.py
git commit -m "feat(unit): add 6-slot inventory to Unit class

- inventory: List[Optional[Item]] with 6 slots
- add_item, remove_item, remove_item_from_slot methods
- get_item_in_slot, find_item helper methods"
```

---

## Task 2: 创建 UnitAddItem Native 函数

**Files:**
- Create: `src/jass_runner/natives/item_inventory_natives.py`
- Modify: `src/jass_runner/natives/__init__.py`

**Step 1: 创建文件并导入依赖**

Create `src/jass_runner/natives/item_inventory_natives.py`:

```python
"""物品背包系统 Native 函数实现。"""

import logging
from typing import Optional

from jass_runner.natives.base import NativeFunction
from jass_runner.natives.handle import Unit, Item
from jass_runner.state_context import StateContext
from jass_runner.utils.fourcc import int_to_fourcc, string_to_fourcc

logger = logging.getLogger(__name__)


class UnitAddItem(NativeFunction):
    """将物品添加到单位背包。"""

    @property
    def name(self) -> str:
        return "UnitAddItem"

    def execute(self, state_context: StateContext, unit: Unit, item: Item) -> bool:
        """执行添加物品操作。"""
        if unit.find_item(item) >= 0:
            logger.warning(f"[UnitAddItem] 物品 {item.id} 已在单位背包中")
            return False
        result = unit.add_item(item)
        if result:
            logger.info(f"[UnitAddItem] 物品 {item.id} 添加到单位 {unit.id}")
        else:
            logger.warning(f"[UnitAddItem] 单位 {unit.id} 背包已满，无法添加物品")
        return result
```

**Step 2: 更新 __init__.py 导出**

在 `src/jass_runner/natives/__init__.py` 末尾添加:

```python
from jass_runner.natives.item_inventory_natives import (
    UnitAddItem,
)

__all__.extend([
    "UnitAddItem",
])
```

**Step 3: 创建单元测试文件**

Create `tests/natives/test_item_inventory_natives.py`:

```python
"""物品背包 Native 函数单元测试。"""

import pytest
from jass_runner.natives.handle import Unit, Item, Player
from jass_runner.natives.manager import HandleManager
from jass_runner.natives.item_inventory_natives import UnitAddItem
from jass_runner.state_context import StateContext


class TestUnitAddItem:
    """测试 UnitAddItem 函数。"""

    def test_add_item_to_empty_slot_success(self):
        """测试成功添加物品到空槽位。"""
        # 准备
        handle_manager = HandleManager()
        state_context = StateContext(handle_manager)
        player = handle_manager.get_player(0)
        unit = handle_manager.create_unit(0, player, 0.0, 0.0)
        item = handle_manager.create_item("ratf", 1.0, 1.0)
        native = UnitAddItem()

        # 执行
        result = native.execute(state_context, unit, item)

        # 验证
        assert result is True
        assert unit.find_item(item) >= 0

    def test_add_item_when_inventory_full_fails(self):
        """测试背包满时添加失败。"""
        handle_manager = HandleManager()
        state_context = StateContext(handle_manager)
        player = handle_manager.get_player(0)
        unit = handle_manager.create_unit(0, player, 0.0, 0.0)
        native = UnitAddItem()

        # 填满6个槽位
        for i in range(6):
            item = handle_manager.create_item(f"item{i}", float(i), float(i))
            unit.add_item(item)

        # 尝试添加第7个
        extra_item = handle_manager.create_item("extra", 10.0, 10.0)
        result = native.execute(state_context, unit, extra_item)

        assert result is False
```

**Step 4: 运行测试确保失败（红阶段）**

Run: `pytest tests/natives/test_item_inventory_natives.py::TestUnitAddItem::test_add_item_to_empty_slot_success -v`
Expected: FAIL (可能需要修复导入等基础问题)

**Step 5: Run 确保通过（绿阶段）**

Run: `pytest tests/natives/test_item_inventory_natives.py::TestUnitAddItem -v`
Expected: PASS

**Step 6: Commit**

```bash
git add src/jass_runner/natives/item_inventory_natives.py src/jass_runner/natives/__init__.py tests/natives/test_item_inventory_natives.py
git commit -m "feat(natives): add UnitAddItem native function

- Add item to first empty slot
- Return False when inventory full or item already in unit"
```

---

## Task 3: 实现 UnitAddItemById Native 函数

**Files:**
- Modify: `src/jass_runner/natives/item_inventory_natives.py`
- Modify: `src/jass_runner/natives/__init__.py`
- Modify: `tests/natives/test_item_inventory_natives.py`

**Step 1: 添加函数到 item_inventory_natives.py**

在 UnitAddItem 类之后添加:

```python
class UnitAddItemById(NativeFunction):
    """创建物品并添加到单位背包。"""

    @property
    def name(self) -> str:
        return "UnitAddItemById"

    def execute(self, state_context: StateContext, unit: Unit, item_type_id: int, slot: int = -1) -> Optional[Item]:
        """执行创建并添加物品操作。"""
        item_type_str = int_to_fourcc(item_type_id)
        handle_manager = state_context.handle_manager

        # 创建物品（使用单位位置）
        item = handle_manager.create_item(item_type_str, unit.x, unit.y)

        # 添加到单位
        if unit.add_item(item, slot):
            slot_str = f"槽位 {slot}" if slot >= 0 else "自动槽位"
            logger.info(f"[UnitAddItemById] 创建 {item_type_str} 并添加到单位 {unit.id} 的{slot_str}")
            return item
        else:
            # 添加失败，销毁物品
            handle_manager.destroy_handle(item.id)
            slot_str = f"槽位 {slot}" if slot >= 0 else "背包"
            logger.warning(f"[UnitAddItemById] {slot_str}已满或无效，销毁已创建的 {item_type_str}")
            return None
```

**Step 2: 更新 __init__.py**

添加:

```python
from jass_runner.natives.item_inventory_natives import (
    UnitAddItem,
    UnitAddItemById,
)

__all__.extend([
    "UnitAddItem",
    "UnitAddItemById",
])
```

**Step 3: 添加测试到 test_item_inventory_natives.py**

```python
class TestUnitAddItemById:
    """测试 UnitAddItemById 函数。"""

    def test_add_item_by_id_auto_slot(self):
        """测试自动找空槽添加。"""
        handle_manager = HandleManager()
        state_context = StateContext(handle_manager)
        player = handle_manager.get_player(0)
        unit = handle_manager.create_unit(0, player, 0.0, 0.0)
        native = UnitAddItemById()

        # FourCC 'ratf' = 1380010356
        item_type_id = 1380010356
        result = native.execute(state_context, unit, item_type_id, -1)

        assert result is not None
        assert result.item_type == "ratf"
        assert unit.find_item(result) >= 0

    def test_add_item_by_id_specific_slot(self):
        """测试指定槽位添加。"""
        handle_manager = HandleManager()
        state_context = StateContext(handle_manager)
        player = handle_manager.get_player(0)
        unit = handle_manager.create_unit(0, player, 0.0, 0.0)
        native = UnitAddItemById()

        item_type_id = 1380010356  # 'ratf'
        result = native.execute(state_context, unit, item_type_id, 3)

        assert result is not None
        assert unit.get_item_in_slot(3) is result

    def test_add_item_by_id_occupied_slot_fails(self):
        """测试指定槽位被占时失败。"""
        handle_manager = HandleManager()
        state_context = StateContext(handle_manager)
        player = handle_manager.get_player(0)
        unit = handle_manager.create_unit(0, player, 0.0, 0.0)
        native = UnitAddItemById()

        # 先占用槽位3
        existing_item = handle_manager.create_item("existing", 1.0, 1.0)
        unit.add_item(existing_item, 3)

        # 尝试添加到新槽位3
        item_type_id = 1380010356
        result = native.execute(state_context, unit, item_type_id, 3)

        assert result is None
        # 确认原有物品仍在
        assert unit.get_item_in_slot(3) is existing_item
```

**Step 4: 运行测试**

Run: `pytest tests/natives/test_item_inventory_natives.py::TestUnitAddItemById -v`
Expected: PASS

**Step 5: Commit**

```bash
git add src/jass_runner/natives/item_inventory_natives.py src/jass_runner/natives/__init__.py tests/natives/test_item_inventory_natives.py
git commit -m "feat(natives): add UnitAddItemById native function

- Create item and add to unit inventory
- Support auto slot selection (slot=-1)
- Support specific slot target (slot=0-5)
- Clean up created item on failure"
```

---

## Task 4: 实现 UnitRemoveItem 和 UnitRemoveItemFromSlot

**Files:**
- Modify: `src/jass_runner/natives/item_inventory_natives.py`
- Modify: `src/jass_runner/natives/__init__.py`
- Modify: `tests/natives/test_item_inventory_natives.py`

**Step 1: 添加两个 Remove 函数**

```python
class UnitRemoveItem(NativeFunction):
    """从单位移除并销毁物品。"""

    @property
    def name(self) -> str:
        return "UnitRemoveItem"

    def execute(self, state_context: StateContext, unit: Unit, item: Item) -> bool:
        """执行移除并销毁操作。"""
        result = unit.remove_item(item)
        if result:
            handle_manager = state_context.handle_manager
            handle_manager.destroy_handle(item.id)
            logger.info(f"[UnitRemoveItem] 销毁物品 {item.id}")
            return True
        logger.warning(f"[UnitRemoveItem] 物品 {item.id} 不在单位 {unit.id} 背包中")
        return False


class UnitRemoveItemFromSlot(NativeFunction):
    """从指定槽位移除并销毁物品。"""

    @property
    def name(self) -> str:
        return "UnitRemoveItemFromSlot"

    def execute(self, state_context: StateContext, unit: Unit, slot: int) -> bool:
        """执行从槽位移除并销毁操作。"""
        item = unit.get_item_in_slot(slot)
        if item:
            unit.remove_item_from_slot(slot)
            handle_manager = state_context.handle_manager
            handle_manager.destroy_handle(item.id)
            logger.info(f"[UnitRemoveItemFromSlot] 槽位 {slot} 的物品已销毁")
            return True
        logger.warning(f"[UnitRemoveItemFromSlot] 槽位 {slot} 为空或无效")
        return False
```

**Step 2: 更新 __init__.py**

```python
from jass_runner.natives.item_inventory_natives import (
    UnitAddItem,
    UnitAddItemById,
    UnitRemoveItem,
    UnitRemoveItemFromSlot,
)

__all__.extend([
    "UnitAddItem",
    "UnitAddItemById",
    "UnitRemoveItem",
    "UnitRemoveItemFromSlot",
])
```

**Step 3: 添加测试**

```python
class TestUnitRemoveItem:
    """测试 UnitRemoveItem 函数。"""

    def test_remove_item_success(self):
        """测试成功移除并销毁物品。"""
        handle_manager = HandleManager()
        state_context = StateContext(handle_manager)
        player = handle_manager.get_player(0)
        unit = handle_manager.create_unit(0, player, 0.0, 0.0)
        item = handle_manager.create_item("ratf", 1.0, 1.0)
        unit.add_item(item)
        native = UnitRemoveItem()

        result = native.execute(state_context, unit, item)

        assert result is True
        assert unit.find_item(item) == -1
        # 验证物品已销毁
        assert handle_manager.get_handle(item.id) is None

    def test_remove_item_not_in_inventory_fails(self):
        """测试移除不在背包中的物品失败。"""
        handle_manager = HandleManager()
        state_context = StateContext(handle_manager)
        player = handle_manager.get_player(0)
        unit = handle_manager.create_unit(0, player, 0.0, 0.0)
        item = handle_manager.create_item("ratf", 1.0, 1.0)
        # 不添加到单位
        native = UnitRemoveItem()

        result = native.execute(state_context, unit, item)

        assert result is False
        # 物品未被销毁
        assert handle_manager.get_handle(item.id) is not None


class TestUnitRemoveItemFromSlot:
    """测试 UnitRemoveItemFromSlot 函数。"""

    def test_remove_from_slot_success(self):
        """测试从指定槽位移除成功。"""
        handle_manager = HandleManager()
        state_context = StateContext(handle_manager)
        player = handle_manager.get_player(0)
        unit = handle_manager.create_unit(0, player, 0.0, 0.0)
        item = handle_manager.create_item("ratf", 1.0, 1.0)
        unit.add_item(item, 2)
        native = UnitRemoveItemFromSlot()

        result = native.execute(state_context, unit, 2)

        assert result is True
        assert unit.get_item_in_slot(2) is None

    def test_remove_from_empty_slot_fails(self):
        """测试从空槽位移除失败。"""
        handle_manager = HandleManager()
        state_context = StateContext(handle_manager)
        player = handle_manager.get_player(0)
        unit = handle_manager.create_unit(0, player, 0.0, 0.0)
        native = UnitRemoveItemFromSlot()

        result = native.execute(state_context, unit, 3)

        assert result is False
```

**Step 4: 运行测试**

Run: `pytest tests/natives/test_item_inventory_natives.py::TestUnitRemoveItem tests/natives/test_item_inventory_natives.py::TestUnitRemoveItemFromSlot -v`
Expected: PASS

**Step 5: Commit**

```bash
git add src/jass_runner/natives/item_inventory_natives.py src/jass_runner/natives/__init__.py tests/natives/test_item_inventory_natives.py
git commit -m "feat(natives): add UnitRemoveItem and UnitRemoveItemFromSlot

- Remove and destroy item from unit inventory
- Remove by item reference or by slot index
- Return False if item not found or slot empty"
```

---

## Task 5: 实现 GetItemTypeId 和 UnitItemInSlot

**Files:**
- Modify: `src/jass_runner/natives/item_inventory_natives.py`
- Modify: `src/jass_runner/natives/__init__.py`
- Modify: `tests/natives/test_item_inventory_natives.py`

**Step 1: 添加两个查询函数**

```python
class GetItemTypeId(NativeFunction):
    """获取物品类型ID（FourCC整数）。"""

    @property
    def name(self) -> str:
        return "GetItemTypeId"

    def execute(self, state_context: StateContext, item: Item) -> int:
        """返回物品类型ID。"""
        return string_to_fourcc(item.item_type)


class UnitItemInSlot(NativeFunction):
    """获取单位指定槽位的物品。"""

    @property
    def name(self) -> str:
        return "UnitItemInSlot"

    def execute(self, state_context: StateContext, unit: Unit, slot: int) -> Optional[Item]:
        """返回指定槽位的物品，空槽返回None。"""
        return unit.get_item_in_slot(slot)
```

**Step 2: 更新 __init__.py 导出全部6个函数**

```python
from jass_runner.natives.item_inventory_natives import (
    UnitAddItem,
    UnitAddItemById,
    UnitRemoveItem,
    UnitRemoveItemFromSlot,
    GetItemTypeId,
    UnitItemInSlot,
)

__all__.extend([
    "UnitAddItem",
    "UnitAddItemById",
    "UnitRemoveItem",
    "UnitRemoveItemFromSlot",
    "GetItemTypeId",
    "UnitItemInSlot",
])
```

**Step 3: 添加测试**

```python
class TestGetItemTypeId:
    """测试 GetItemTypeId 函数。"""

    def test_get_item_type_id(self):
        """测试获取物品类型ID正确。"""
        handle_manager = HandleManager()
        state_context = StateContext(handle_manager)
        # 'ratf' = 1380010356 (小端序)
        item = handle_manager.create_item("ratf", 1.0, 1.0)
        native = GetItemTypeId()

        result = native.execute(state_context, item)

        assert result == 1380010356

    def test_get_item_type_id_different_items(self):
        """测试不同类型物品返回不同ID。"""
        handle_manager = HandleManager()
        state_context = StateContext(handle_manager)

        item1 = handle_manager.create_item("ratf", 1.0, 1.0)  # 'ratf'
        item2 = handle_manager.create_item("pghe", 2.0, 2.0)  # 'pghe'

        native = GetItemTypeId()

        assert native.execute(state_context, item1) != native.execute(state_context, item2)


class TestUnitItemInSlot:
    """测试 UnitItemInSlot 函数。"""

    def test_get_item_in_slot_exists(self):
        """测试获取存在的物品。"""
        handle_manager = HandleManager()
        state_context = StateContext(handle_manager)
        player = handle_manager.get_player(0)
        unit = handle_manager.create_unit(0, player, 0.0, 0.0)
        item = handle_manager.create_item("ratf", 1.0, 1.0)
        unit.add_item(item, 4)
        native = UnitItemInSlot()

        result = native.execute(state_context, unit, 4)

        assert result is item

    def test_get_item_in_slot_empty(self):
        """测试空槽返回None。"""
        handle_manager = HandleManager()
        state_context = StateContext(handle_manager)
        player = handle_manager.get_player(0)
        unit = handle_manager.create_unit(0, player, 0.0, 0.0)
        native = UnitItemInSlot()

        result = native.execute(state_context, unit, 2)

        assert result is None
```

**Step 4: 运行全部单元测试**

Run: `pytest tests/natives/test_item_inventory_natives.py -v`
Expected: 12+ tests PASS

**Step 5: Commit**

```bash
git add src/jass_runner/natives/item_inventory_natives.py src/jass_runner/natives/__init__.py tests/natives/test_item_inventory_natives.py
git commit -m "feat(natives): add GetItemTypeId and UnitItemInSlot

- GetItemTypeId: return FourCC integer for item type
- UnitItemInSlot: get item at specific slot (0-5)
- Complete 6 native functions for item inventory system"
```

---

## Task 6: 注册所有 Native 函数到 Factory

**Files:**
- Modify: `src/jass_runner/natives/factory.py`
- Test: `tests/natives/test_factory.py`

**Step 1: 修改 factory.py 添加导入和注册**

在现有导入之后（约第7行）添加:

```python
from jass_runner.natives.item_inventory_natives import (
    UnitAddItem,
    UnitAddItemById,
    UnitRemoveItem,
    UnitRemoveItemFromSlot,
    GetItemTypeId,
    UnitItemInSlot,
)
```

在 create_default_registry 方法中（约第72行之后）添加注册:

```python
registry.register(UnitAddItem())
registry.register(UnitAddItemById())
registry.register(UnitRemoveItem())
registry.register(UnitRemoveItemFromSlot())
registry.register(GetItemTypeId())
registry.register(UnitItemInSlot())
```

**Step 2: 验证 factory 测试更新**

查找现有 factory 测试中的函数数量检查:

Run: `grep -n "count\|len" tests/natives/test_factory.py`

更新测试预期（如果需要）:

```python
def test_default_factory_registers_all_item_natives(self):
    """测试工厂包含所有物品背包 Native 函数。"""
    registry = NativeFactory.create_default_registry()
    names = [cls.__name__ for cls in registry.get_all().values()]
    assert "UnitAddItem" in names
    assert "UnitAddItemById" in names
    assert "UnitRemoveItem" in names
    assert "UnitRemoveItemFromSlot" in names
    assert "GetItemTypeId" in names
    assert "UnitItemInSlot" in names
```

**Step 3: 运行 factory 测试**

Run: `pytest tests/natives/test_factory.py -v`
Expected: PASS

**Step 4: Commit**

```bash
git add src/jass_runner/natives/factory.py tests/natives/test_factory.py
git commit -m "feat(factory): register all 6 item inventory natives

- UnitAddItem, UnitAddItemById
- UnitRemoveItem, UnitRemoveItemFromSlot
- GetItemTypeId, UnitItemInSlot"
```

---

## Task 7: 创建集成测试

**Files:**
- Create: `tests/integration/test_item_inventory_integration.py`

**Step 1: 创建集成测试文件**

```python
"""物品背包系统集成测试。"""

import pytest
from jass_runner.natives.handle import Unit, Item, Player
from jass_runner.natives.manager import HandleManager
from jass_runner.natives.item_inventory_natives import (
    UnitAddItem,
    UnitAddItemById,
    UnitRemoveItem,
    UnitRemoveItemFromSlot,
    GetItemTypeId,
    UnitItemInSlot,
)
from jass_runner.state_context import StateContext


class TestItemInventoryIntegration:
    """物品背包完整生命周期集成测试。"""

    def test_complete_item_lifecycle(self):
        """测试完整物品生命周期：创建→添加→查询→使用→移除。"""
        handle_manager = HandleManager()
        state_context = StateContext(handle_manager)
        player = handle_manager.get_player(0)
        unit = handle_manager.create_unit(0, player, 0.0, 0.0)

        # 1. 通过类型ID创建并添加物品
        item_type_id = 1380010356  # 'ratf'
        item = UnitAddItemById().execute(state_context, unit, item_type_id, -1)
        assert item is not None

        # 2. 查询物品类型
        type_id = GetItemTypeId().execute(state_context, item)
        assert type_id == item_type_id

        # 3. 查找物品所在槽位
        slot = unit.find_item(item)
        assert 0 <= slot < 6

        # 4. 通过槽位获取物品
        found_item = UnitItemInSlot().execute(state_context, unit, slot)
        assert found_item is item

        # 5. 使用 UnitAddItem 再次添加（应该失败，已在此单位中）
        result = UnitAddItem().execute(state_context, unit, item)
        assert result is False

        # 6. 移除物品
        result = UnitRemoveItem().execute(state_context, unit, item)
        assert result is True

        # 7. 确认槽位为空
        assert UnitItemInSlot().execute(state_context, unit, slot) is None

    def test_fill_all_inventory_slots(self):
        """测试填满6个槽位并管理。"""
        handle_manager = HandleManager()
        state_context = StateContext(handle_manager)
        player = handle_manager.get_player(0)
        unit = handle_manager.create_unit(0, player, 0.0, 0.0)

        # 填满6个槽
        items = []
        for i in range(6):
            item = UnitAddItemById().execute(state_context, unit, 1380010356, -1)
            assert item is not None
            items.append(item)

        # 验证所有槽有物品
        for i in range(6):
            assert unit.get_item_in_slot(i) is not None

        # 满槽添加失败
        extra_item = handle_manager.create_item("extra", 10.0, 10.0)
        result = UnitAddItem().execute(state_context, unit, extra_item)
        assert result is False

        # 逐个移除
        for i in range(6):
            result = UnitRemoveItemFromSlot().execute(state_context, unit, i)
            assert result is True

        # 全部为空
        for i in range(6):
            assert unit.get_item_in_slot(i) is None

    def test_item_move_between_units(self):
        """测试物品在两个单位间转移。"""
        handle_manager = HandleManager()
        state_context = StateContext(handle_manager)
        player = handle_manager.get_player(0)
        unit_a = handle_manager.create_unit(0, player, 0.0, 0.0)
        unit_b = handle_manager.create_unit(0, player, 10.0, 10.0)

        # 在Unit A创建物品
        item = handle_manager.create_item("ratf", 1.0, 1.0)
        unit_a.add_item(item)
        assert unit_a.find_item(item) >= 0

        # 在Unit B无法直接添加（已在Unit A中）- 需要先从A移除
        result = UnitAddItem().execute(state_context, unit_b, item)
        assert result is False  # 已在 A 中

        # 错误做法：直接从B移除（物品在A中）
        result = UnitRemoveItem().execute(state_context, unit_b, item)
        assert result is False

        # 正确：从A移除（销毁）
        result = UnitRemoveItem().execute(state_context, unit_a, item)
        assert result is True

        # 重新创建并添加到B
        # 注意：原物品已销毁，需要创建新物品
        item = handle_manager.create_item("ratf", 10.0, 10.0)
        result = UnitAddItem().execute(state_context, unit_b, item)
        assert result is True
        assert unit_b.find_item(item) >= 0
```

**Step 2: 运行集成测试**

Run: `pytest tests/integration/test_item_inventory_integration.py -v`
Expected: PASS

**Step 3: Commit**

```bash
git add tests/integration/test_item_inventory_integration.py
git commit -m "test(integration): add item inventory lifecycle tests

- Complete item lifecycle: create, add, query, remove
- Fill all 6 slots and manage
- Item movement simulation between units"
```

---

## Task 8: 最终验证和文档更新

**Step 1: 运行全部相关测试**

```bash
pytest tests/natives/test_item_inventory_natives.py tests/natives/test_factory.py tests/integration/test_item_inventory_integration.py -v --tb=short
```
Expected: 所有测试通过

**Step 2: 运行项目整体测试确保无回归**

```bash
pytest -x
```
Expected: 所有测试通过（预期增加到约 700+ 测试）

**Step 3: 更新 PROJECT_NOTES.md（可选）**

添加新的进展记录:

```markdown
#### 50. 物品系统Native函数实现完成 (2026-03-03)
- **新增组件**:
  - Unit类背包扩展 - 6槽位物品管理
  - `item_inventory_natives.py` - 6个物品背包Native函数
- **新增Native函数**:
  - 添加物品: UnitAddItem, UnitAddItemById
  - 移除物品: UnitRemoveItem, UnitRemoveItemFromSlot
  - 查询物品: GetItemTypeId, UnitItemInSlot
- **修改文件**:
  - `src/jass_runner/natives/handle.py` - Unit类添加inventory管理方法
  - `src/jass_runner/natives/factory.py` - 注册6个新函数
  - `src/jass_runner/natives/__init__.py` - 导出新函数
- **测试覆盖**:
  - 单元测试: 12+个测试用例覆盖所有函数
  - 集成测试: 3个场景测试完整生命周期
- **测试统计**: 700+个测试通过
```

**Step 4: 最终 Commit（如果更新了 PROJECT_NOTES）**

```bash
git add PROJECT_NOTES.md
git commit -m "docs: update PROJECT_NOTES for item system completion"
```

---

## 实施计划总结

| 任务 | 耗时 | 关键文件 |
|------|------|----------|
| Task 1: Unit类扩展 | 10分钟 | handle.py |
| Task 2: UnitAddItem | 15分钟 | item_inventory_natives.py, test |
| Task 3: UnitAddItemById | 15分钟 | item_inventory_natives.py, test |
| Task 4: Remove函数 | 15分钟 | item_inventory_natives.py, test |
| Task 5: Query函数 | 15分钟 | item_inventory_natives.py, test |
| Task 6: Factory注册 | 10分钟 | factory.py, test |
| Task 7: 集成测试 | 15分钟 | integration test |
| Task 8: 验证和文档 | 10分钟 | 全部测试 |

**总计预估**: 约 90-105 分钟

---

## 验收标准

- [ ] 6 个 Native 函数全部实现并通过测试
- [ ] Unit 类包含完整的 inventory 管理（6槽位）
- [ ] Factory 成功注册所有新函数
- [ ] 单元测试覆盖率 100%（6个函数，每个至少2个测试）
- [ ] 集成测试覆盖完整生命周期
- [ ] 项目整体测试无回归（700+ 测试通过）
- [ ] 代码遵循项目风格（中文注释、符合 flake8）

---

**计划创建者**: Claude Code
**计划状态**: 待执行
