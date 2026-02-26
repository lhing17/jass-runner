# JASS模拟器状态管理系统 - 阶段1：基础架构实施计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 实现Handle类体系和HandleManager核心功能，为状态管理系统奠定基础。

**Architecture:** 创建Handle类继承层次结构（Handle → Unit等），实现HandleManager集中式管理器，支持handle的创建、查询、销毁和类型安全操作。

**Tech Stack:** Python 3.8+, pytest, 自定义解析器和解释器框架

---

### Task 1: 创建Handle基类

**Files:**
- Create: `src/jass_runner/natives/handle.py`
- Test: `tests/natives/test_handle.py`

**Step 1: Write the failing test**

```python
"""Handle基类测试。"""

def test_handle_base_class():
    """测试Handle基类的创建和基本属性。"""
    from jass_runner.natives.handle import Handle

    # 创建Handle实例
    handle = Handle("test_001", "test_type")

    # 验证基本属性
    assert handle.id == "test_001"
    assert handle.type_name == "test_type"
    assert handle.alive is True
    assert handle.is_alive() is True

def test_handle_destroy():
    """测试Handle销毁功能。"""
    from jass_runner.natives.handle import Handle

    handle = Handle("test_002", "test_type")
    assert handle.is_alive() is True

    # 销毁handle
    handle.destroy()
    assert handle.alive is False
    assert handle.is_alive() is False
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/natives/test_handle.py::test_handle_base_class -v`
Expected: FAIL with "ModuleNotFoundError: No module named 'jass_runner.natives.handle'"

**Step 3: Write minimal implementation**

```python
"""JASS handle类体系。

此模块包含所有JASS handle的基类和具体实现。
"""


class Handle:
    """所有JASS handle的基类。

    属性：
        id: 唯一标识符（字符串）
        type_name: handle类型名称
        alive: 是否存活
    """

    def __init__(self, handle_id: str, type_name: str):
        self.id = handle_id
        self.type_name = type_name
        self.alive = True

    def destroy(self):
        """标记handle为销毁状态。"""
        self.alive = False

    def is_alive(self) -> bool:
        """检查handle是否存活。"""
        return self.alive
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/natives/test_handle.py::test_handle_base_class -v`
Expected: PASS

**Step 5: Commit**

```bash
git add tests/natives/test_handle.py src/jass_runner/natives/handle.py
git commit -m "feat: add Handle base class"
```

---

### Task 2: 创建Unit类

**Files:**
- Modify: `src/jass_runner/natives/handle.py`
- Test: `tests/natives/test_handle.py`

**Step 1: Write the failing test**

```python
def test_unit_class():
    """测试Unit类的创建和属性。"""
    from jass_runner.natives.handle import Unit

    # 创建Unit实例
    unit = Unit("unit_001", "hfoo", 0, 100.0, 200.0, 270.0)

    # 验证继承自Handle
    assert isinstance(unit, Handle)
    assert unit.id == "unit_001"
    assert unit.type_name == "unit"
    assert unit.alive is True

    # 验证Unit特有属性
    assert unit.unit_type == "hfoo"
    assert unit.player_id == 0
    assert unit.x == 100.0
    assert unit.y == 200.0
    assert unit.facing == 270.0
    assert unit.life == 100.0
    assert unit.max_life == 100.0
    assert unit.mana == 50.0
    assert unit.max_mana == 50.0

def test_unit_destroy():
    """测试Unit销毁功能。"""
    from jass_runner.natives.handle import Unit

    unit = Unit("unit_002", "hfoo", 0, 0.0, 0.0, 0.0)
    assert unit.is_alive() is True
    assert unit.life == 100.0

    # 销毁unit
    unit.destroy()
    assert unit.alive is False
    assert unit.is_alive() is False
    assert unit.life == 0  # 生命值应设为0
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/natives/test_handle.py::test_unit_class -v`
Expected: FAIL with "NameError: name 'Unit' is not defined"

**Step 3: Write minimal implementation**

```python
class Unit(Handle):
    """单位handle。

    属性：
        unit_type: 单位类型代码（如'hfoo'）
        player_id: 所属玩家ID
        x, y: 位置坐标
        facing: 面向角度
        life: 当前生命值
        max_life: 最大生命值
        mana: 当前魔法值
        max_mana: 最大魔法值
    """

    def __init__(self, handle_id: str, unit_type: str, player_id: int,
                 x: float, y: float, facing: float):
        super().__init__(handle_id, "unit")
        self.unit_type = unit_type
        self.player_id = player_id
        self.x = x
        self.y = y
        self.facing = facing
        self.life = 100.0
        self.max_life = 100.0
        self.mana = 50.0
        self.max_mana = 50.0

    def destroy(self):
        """销毁单位，将生命值设为0。"""
        self.life = 0
        super().destroy()
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/natives/test_handle.py::test_unit_class -v`
Expected: PASS

**Step 5: Commit**

```bash
git add src/jass_runner/natives/handle.py tests/natives/test_handle.py
git commit -m "feat: add Unit class"
```

---

### Task 3: 创建HandleManager核心类

**Files:**
- Create: `src/jass_runner/natives/manager.py`
- Test: `tests/natives/test_manager.py`

**Step 1: Write the failing test**

```python
"""HandleManager测试。"""

def test_handle_manager_creation():
    """测试HandleManager创建和基本属性。"""
    from jass_runner.natives.manager import HandleManager

    manager = HandleManager()
    assert manager._handles == {}
    assert manager._type_index == {}
    assert manager._next_id == 1

def test_handle_manager_create_unit():
    """测试HandleManager创建单位功能。"""
    from jass_runner.natives.manager import HandleManager

    manager = HandleManager()

    # 创建单位
    unit_id = manager.create_unit("hfoo", 0, 100.0, 200.0, 270.0)

    # 验证返回的ID格式
    assert isinstance(unit_id, str)
    assert unit_id.startswith("unit_")

    # 验证单位已注册
    unit = manager.get_unit(unit_id)
    assert unit is not None
    assert unit.id == unit_id
    assert unit.unit_type == "hfoo"
    assert unit.player_id == 0
    assert unit.x == 100.0
    assert unit.y == 200.0
    assert unit.facing == 270.0
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/natives/test_manager.py::test_handle_manager_creation -v`
Expected: FAIL with "ModuleNotFoundError: No module named 'jass_runner.natives.manager'"

**Step 3: Write minimal implementation**

```python
"""Handle管理器。

此模块包含HandleManager类，负责所有handle的生命周期管理。
"""

from typing import Dict, List, Optional
from .handle import Handle, Unit


class HandleManager:
    """集中式handle管理器。

    负责所有handle的生命周期管理。
    """

    def __init__(self):
        self._handles: Dict[str, Handle] = {}  # id -> handle对象
        self._type_index: Dict[str, List[str]] = {}  # 类型索引
        self._next_id = 1

    def _generate_id(self) -> int:
        """生成下一个ID。"""
        current_id = self._next_id
        self._next_id += 1
        return current_id

    def _register_handle(self, handle: Handle):
        """注册handle到管理器中。"""
        self._handles[handle.id] = handle

        # 更新类型索引
        if handle.type_name not in self._type_index:
            self._type_index[handle.type_name] = []
        self._type_index[handle.type_name].append(handle.id)

    def create_unit(self, unit_type: str, player_id: int,
                   x: float, y: float, facing: float) -> str:
        """创建一个单位并返回handle ID。"""
        handle_id = f"unit_{self._generate_id()}"
        unit = Unit(handle_id, unit_type, player_id, x, y, facing)
        self._register_handle(unit)
        return handle_id

    def get_handle(self, handle_id: str) -> Optional[Handle]:
        """通过ID获取handle对象。"""
        handle = self._handles.get(handle_id)
        if handle and handle.is_alive():
            return handle
        return None

    def get_unit(self, unit_id: str) -> Optional[Unit]:
        """获取单位对象，进行类型检查。"""
        handle = self.get_handle(unit_id)
        if isinstance(handle, Unit):
            return handle
        return None
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/natives/test_manager.py::test_handle_manager_creation -v`
Expected: PASS

**Step 5: Commit**

```bash
git add src/jass_runner/natives/manager.py tests/natives/test_manager.py
git commit -m "feat: add HandleManager core class"
```

---

### Task 4: 实现HandleManager查询和销毁功能

**Files:**
- Modify: `src/jass_runner/natives/manager.py`
- Test: `tests/natives/test_manager.py`

**Step 1: Write the failing test**

```python
def test_handle_manager_get_handle():
    """测试HandleManager获取handle功能。"""
    from jass_runner.natives.manager import HandleManager

    manager = HandleManager()

    # 创建单位
    unit_id = manager.create_unit("hfoo", 0, 0.0, 0.0, 0.0)

    # 测试获取handle
    handle = manager.get_handle(unit_id)
    assert handle is not None
    assert handle.id == unit_id

    # 测试获取不存在的handle
    assert manager.get_handle("nonexistent") is None

def test_handle_manager_destroy_handle():
    """测试HandleManager销毁handle功能。"""
    from jass_runner.natives.manager import HandleManager

    manager = HandleManager()

    # 创建单位
    unit_id = manager.create_unit("hfoo", 0, 0.0, 0.0, 0.0)

    # 验证单位存活
    unit = manager.get_unit(unit_id)
    assert unit is not None
    assert unit.is_alive() is True

    # 销毁单位
    result = manager.destroy_handle(unit_id)
    assert result is True

    # 验证单位已销毁
    unit = manager.get_unit(unit_id)
    assert unit is None  # 已销毁的单位不应返回

    # 测试销毁不存在的handle
    result = manager.destroy_handle("nonexistent")
    assert result is False

def test_handle_manager_type_index():
    """测试HandleManager类型索引功能。"""
    from jass_runner.natives.manager import HandleManager

    manager = HandleManager()

    # 创建多个单位
    unit_id1 = manager.create_unit("hfoo", 0, 0.0, 0.0, 0.0)
    unit_id2 = manager.create_unit("hkni", 1, 100.0, 100.0, 90.0)

    # 验证类型索引
    assert "unit" in manager._type_index
    assert unit_id1 in manager._type_index["unit"]
    assert unit_id2 in manager._type_index["unit"]
    assert len(manager._type_index["unit"]) == 2
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/natives/test_manager.py::test_handle_manager_get_handle -v`
Expected: FAIL with "AttributeError: 'HandleManager' object has no attribute 'destroy_handle'"

**Step 3: Write minimal implementation**

```python
    def destroy_handle(self, handle_id: str) -> bool:
        """销毁指定的handle。"""
        handle = self._handles.get(handle_id)
        if handle and handle.is_alive():
            handle.destroy()
            return True
        return False
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/natives/test_manager.py::test_handle_manager_get_handle -v`
Expected: PASS

**Step 5: Commit**

```bash
git add src/jass_runner/natives/manager.py tests/natives/test_manager.py
git commit -m "feat: add handle query and destroy methods to HandleManager"
```

---

### Task 5: 创建StateContext类

**Files:**
- Create: `src/jass_runner/natives/state.py`
- Test: `tests/natives/test_state.py`

**Step 1: Write the failing test**

```python
"""StateContext测试。"""

def test_state_context_creation():
    """测试StateContext创建和基本属性。"""
    from jass_runner.natives.state import StateContext

    context = StateContext()
    assert context.handle_manager is not None
    assert context.global_vars == {}
    assert context.local_stores == {}

def test_state_context_get_context_store():
    """测试StateContext获取上下文存储功能。"""
    from jass_runner.natives.state import StateContext

    context = StateContext()

    # 获取不存在的上下文存储
    store = context.get_context_store("test_context")
    assert store == {}

    # 验证存储已创建
    assert "test_context" in context.local_stores
    assert context.local_stores["test_context"] == {}

    # 修改存储并验证
    store["key"] = "value"
    assert context.local_stores["test_context"]["key"] == "value"

    # 再次获取相同上下文存储
    store2 = context.get_context_store("test_context")
    assert store2["key"] == "value"
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/natives/test_state.py::test_state_context_creation -v`
Expected: FAIL with "ModuleNotFoundError: No module named 'jass_runner.natives.state'"

**Step 3: Write minimal implementation**

```python
"""状态上下文。

此模块包含StateContext类，管理全局和局部状态。
"""

from typing import Dict
from .manager import HandleManager


class StateContext:
    """状态上下文，管理全局和局部状态。

    采用混合方案：
    - 全局状态（handle引用）由HandleManager管理
    - 局部状态（临时变量）由ExecutionContext管理
    """

    def __init__(self):
        self.handle_manager = HandleManager()
        self.global_vars = {}  # 全局变量存储
        self.local_stores = {}  # 上下文局部存储

    def get_context_store(self, context_id: str) -> Dict:
        """获取指定上下文的局部存储。"""
        if context_id not in self.local_stores:
            self.local_stores[context_id] = {}
        return self.local_stores[context_id]
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/natives/test_state.py::test_state_context_creation -v`
Expected: PASS

**Step 5: Commit**

```bash
git add src/jass_runner/natives/state.py tests/natives/test_state.py
git commit -m "feat: add StateContext class"
```

---

### Task 6: 添加HandleManager单位状态查询功能

**Files:**
- Modify: `src/jass_runner/natives/manager.py`
- Test: `tests/natives/test_manager.py`

**Step 1: Write the failing test**

```python
def test_handle_manager_get_unit_state():
    """测试HandleManager获取单位状态功能。"""
    from jass_runner.natives.manager import HandleManager

    manager = HandleManager()

    # 创建单位
    unit_id = manager.create_unit("hfoo", 0, 0.0, 0.0, 0.0)

    # 测试获取生命值
    life = manager.get_unit_state(unit_id, "UNIT_STATE_LIFE")
    assert life == 100.0

    # 测试获取魔法值
    mana = manager.get_unit_state(unit_id, "UNIT_STATE_MANA")
    assert mana == 50.0

    # 测试获取最大生命值
    max_life = manager.get_unit_state(unit_id, "UNIT_STATE_MAX_LIFE")
    assert max_life == 100.0

    # 测试获取最大魔法值
    max_mana = manager.get_unit_state(unit_id, "UNIT_STATE_MAX_MANA")
    assert max_mana == 50.0

    # 测试未知状态类型
    unknown = manager.get_unit_state(unit_id, "UNKNOWN_STATE")
    assert unknown == 0.0

    # 测试不存在的单位
    nonexistent = manager.get_unit_state("nonexistent", "UNIT_STATE_LIFE")
    assert nonexistent == 0.0

    # 测试已销毁的单位
    manager.destroy_handle(unit_id)
    destroyed = manager.get_unit_state(unit_id, "UNIT_STATE_LIFE")
    assert destroyed == 0.0
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/natives/test_manager.py::test_handle_manager_get_unit_state -v`
Expected: FAIL with "AttributeError: 'HandleManager' object has no attribute 'get_unit_state'"

**Step 3: Write minimal implementation**

```python
    def get_unit_state(self, unit_id: str, state_type: str) -> float:
        """获取单位状态值。"""
        unit = self.get_unit(unit_id)
        if not unit:
            return 0.0

        if state_type == "UNIT_STATE_LIFE":
            return unit.life
        elif state_type == "UNIT_STATE_MAX_LIFE":
            return unit.max_life
        elif state_type == "UNIT_STATE_MANA":
            return unit.mana
        elif state_type == "UNIT_STATE_MAX_MANA":
            return unit.max_mana
        else:
            return 0.0
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/natives/test_manager.py::test_handle_manager_get_unit_state -v`
Expected: PASS

**Step 5: Commit**

```bash
git add src/jass_runner/natives/manager.py tests/natives/test_manager.py
git commit -m "feat: add unit state query methods to HandleManager"
```

---

### Task 7: 添加HandleManager单位状态修改功能

**Files:**
- Modify: `src/jass_runner/natives/manager.py`
- Test: `tests/natives/test_manager.py`

**Step 1: Write the failing test**

```python
def test_handle_manager_set_unit_state():
    """测试HandleManager设置单位状态功能。"""
    from jass_runner.natives.manager import HandleManager

    manager = HandleManager()

    # 创建单位
    unit_id = manager.create_unit("hfoo", 0, 0.0, 0.0, 0.0)

    # 测试设置生命值
    result = manager.set_unit_state(unit_id, "UNIT_STATE_LIFE", 75.0)
    assert result is True
    assert manager.get_unit_state(unit_id, "UNIT_STATE_LIFE") == 75.0

    # 测试设置魔法值
    result = manager.set_unit_state(unit_id, "UNIT_STATE_MANA", 30.0)
    assert result is True
    assert manager.get_unit_state(unit_id, "UNIT_STATE_MANA") == 30.0

    # 测试设置最大生命值
    result = manager.set_unit_state(unit_id, "UNIT_STATE_MAX_LIFE", 150.0)
    assert result is True
    assert manager.get_unit_state(unit_id, "UNIT_STATE_MAX_LIFE") == 150.0

    # 测试设置最大魔法值
    result = manager.set_unit_state(unit_id, "UNIT_STATE_MAX_MANA", 75.0)
    assert result is True
    assert manager.get_unit_state(unit_id, "UNIT_STATE_MAX_MANA") == 75.0

    # 测试未知状态类型
    result = manager.set_unit_state(unit_id, "UNKNOWN_STATE", 100.0)
    assert result is False

    # 测试不存在的单位
    result = manager.set_unit_state("nonexistent", "UNIT_STATE_LIFE", 100.0)
    assert result is False

    # 测试已销毁的单位
    manager.destroy_handle(unit_id)
    result = manager.set_unit_state(unit_id, "UNIT_STATE_LIFE", 100.0)
    assert result is False
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/natives/test_manager.py::test_handle_manager_set_unit_state -v`
Expected: FAIL with "AttributeError: 'HandleManager' object has no attribute 'set_unit_state'"

**Step 3: Write minimal implementation**

```python
    def set_unit_state(self, unit_id: str, state_type: str, value: float) -> bool:
        """设置单位状态值。"""
        unit = self.get_unit(unit_id)
        if not unit:
            return False

        if state_type == "UNIT_STATE_LIFE":
            unit.life = value
            return True
        elif state_type == "UNIT_STATE_MAX_LIFE":
            unit.max_life = value
            return True
        elif state_type == "UNIT_STATE_MANA":
            unit.mana = value
            return True
        elif state_type == "UNIT_STATE_MAX_MANA":
            unit.max_mana = value
            return True
        else:
            return False
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/natives/test_manager.py::test_handle_manager_set_unit_state -v`
Expected: PASS

**Step 5: Commit**

```bash
git add src/jass_runner/natives/manager.py tests/natives/test_manager.py
git commit -m "feat: add unit state modification methods to HandleManager"
```

---

### Task 8: 添加HandleManager统计功能

**Files:**
- Modify: `src/jass_runner/natives/manager.py`
- Test: `tests/natives/test_manager.py`

**Step 1: Write the failing test**

```python
def test_handle_manager_statistics():
    """测试HandleManager统计功能。"""
    from jass_runner.natives.manager import HandleManager

    manager = HandleManager()

    # 初始状态
    assert manager.get_total_handles() == 0
    assert manager.get_alive_handles() == 0
    assert manager.get_handle_type_count("unit") == 0

    # 创建单位
    unit_id1 = manager.create_unit("hfoo", 0, 0.0, 0.0, 0.0)
    unit_id2 = manager.create_unit("hkni", 1, 100.0, 100.0, 90.0)

    # 验证统计
    assert manager.get_total_handles() == 2
    assert manager.get_alive_handles() == 2
    assert manager.get_handle_type_count("unit") == 2

    # 销毁一个单位
    manager.destroy_handle(unit_id1)

    # 验证统计更新
    assert manager.get_total_handles() == 2  # 总数不变
    assert manager.get_alive_handles() == 1  # 存活数减少
    assert manager.get_handle_type_count("unit") == 2  # 类型计数不变

    # 测试不存在的类型
    assert manager.get_handle_type_count("nonexistent") == 0
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/natives/test_manager.py::test_handle_manager_statistics -v`
Expected: FAIL with "AttributeError: 'HandleManager' object has no attribute 'get_total_handles'"

**Step 3: Write minimal implementation**

```python
    def get_total_handles(self) -> int:
        """获取总handle数量。"""
        return len(self._handles)

    def get_alive_handles(self) -> int:
        """获取存活handle数量。"""
        count = 0
        for handle in self._handles.values():
            if handle.is_alive():
                count += 1
        return count

    def get_handle_type_count(self, type_name: str) -> int:
        """获取指定类型的handle数量。"""
        if type_name not in self._type_index:
            return 0
        return len(self._type_index[type_name])
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/natives/test_manager.py::test_handle_manager_statistics -v`
Expected: PASS

**Step 5: Commit**

```bash
git add src/jass_runner/natives/manager.py tests/natives/test_manager.py
git commit -m "feat: add statistics methods to HandleManager"
```

---

### Task 9: 创建阶段1集成测试

**Files:**
- Create: `tests/integration/test_state_management_phase1.py`
- Test: `tests/integration/test_state_management_phase1.py`

**Step 1: Write the failing test**

```python
"""状态管理系统阶段1集成测试。"""

def test_handle_lifecycle_integration():
    """测试handle完整生命周期集成。"""
    from jass_runner.natives.manager import HandleManager

    manager = HandleManager()

    # 创建单位
    unit_id = manager.create_unit("hfoo", 0, 100.0, 200.0, 270.0)

    # 验证单位创建
    unit = manager.get_unit(unit_id)
    assert unit is not None
    assert unit.unit_type == "hfoo"
    assert unit.player_id == 0
    assert unit.x == 100.0
    assert unit.y == 200.0
    assert unit.facing == 270.0
    assert unit.life == 100.0
    assert unit.is_alive() is True

    # 验证状态查询
    assert manager.get_unit_state(unit_id, "UNIT_STATE_LIFE") == 100.0
    assert manager.get_unit_state(unit_id, "UNIT_STATE_MANA") == 50.0

    # 修改状态
    assert manager.set_unit_state(unit_id, "UNIT_STATE_LIFE", 75.0) is True
    assert manager.get_unit_state(unit_id, "UNIT_STATE_LIFE") == 75.0

    # 销毁单位
    assert manager.destroy_handle(unit_id) is True
    assert unit.is_alive() is False
    assert unit.life == 0

    # 验证销毁后查询
    assert manager.get_unit(unit_id) is None
    assert manager.get_unit_state(unit_id, "UNIT_STATE_LIFE") == 0.0

    # 验证统计
    assert manager.get_total_handles() == 1
    assert manager.get_alive_handles() == 0
    assert manager.get_handle_type_count("unit") == 1

def test_multiple_units_integration():
    """测试多个单位的集成。"""
    from jass_runner.natives.manager import HandleManager

    manager = HandleManager()

    # 创建多个单位
    unit_ids = []
    for i in range(3):
        unit_id = manager.create_unit(f"unit_type_{i}", i, i * 100.0, i * 100.0, i * 90.0)
        unit_ids.append(unit_id)

    # 验证所有单位
    for i, unit_id in enumerate(unit_ids):
        unit = manager.get_unit(unit_id)
        assert unit is not None
        assert unit.unit_type == f"unit_type_{i}"
        assert unit.player_id == i
        assert unit.x == i * 100.0
        assert unit.y == i * 100.0
        assert unit.facing == i * 90.0

    # 验证统计
    assert manager.get_total_handles() == 3
    assert manager.get_alive_handles() == 3
    assert manager.get_handle_type_count("unit") == 3

    # 销毁部分单位
    assert manager.destroy_handle(unit_ids[0]) is True
    assert manager.destroy_handle(unit_ids[1]) is True

    # 验证统计更新
    assert manager.get_total_handles() == 3
    assert manager.get_alive_handles() == 1
    assert manager.get_handle_type_count("unit") == 3
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/integration/test_state_management_phase1.py::test_handle_lifecycle_integration -v`
Expected: PASS (因为所有组件都已实现)

**Step 3: Write minimal implementation**

测试文件已完整，无需额外实现。

**Step 4: Run test to verify it passes**

Run: `pytest tests/integration/test_state_management_phase1.py::test_handle_lifecycle_integration -v`
Expected: PASS

**Step 5: Commit**

```bash
git add tests/integration/test_state_management_phase1.py
git commit -m "feat: add phase 1 integration tests for state management"
```

---

### Task 10: 更新natives模块初始化文件

**Files:**
- Modify: `src/jass_runner/natives/__init__.py`
- Test: `tests/natives/test_imports.py`

**Step 1: Write the failing test**

```python
"""natives模块导入测试。"""

def test_natives_module_imports():
    """测试natives模块的所有导出。"""
    # 测试基础导入
    from jass_runner.natives import NativeFunction, NativeRegistry, NativeFactory

    # 测试新模块导入
    from jass_runner.natives import Handle, Unit, HandleManager, StateContext

    # 验证类型
    assert NativeFunction is not None
    assert NativeRegistry is not None
    assert NativeFactory is not None
    assert Handle is not None
    assert Unit is not None
    assert HandleManager is not None
    assert StateContext is not None
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/natives/test_imports.py::test_natives_module_imports -v`
Expected: FAIL with "ImportError: cannot import name 'Handle' from 'jass_runner.natives'"

**Step 3: Write minimal implementation**

```python
"""JASS native函数框架。

此包包含JASS native函数的模拟实现和状态管理系统。
"""

from .base import NativeFunction
from .registry import NativeRegistry
from .factory import NativeFactory
from .handle import Handle, Unit
from .manager import HandleManager
from .state import StateContext

__all__ = [
    "NativeFunction",
    "NativeRegistry",
    "NativeFactory",
    "Handle",
    "Unit",
    "HandleManager",
    "StateContext",
]
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/natives/test_imports.py::test_natives_module_imports -v`
Expected: PASS

**Step 5: Commit**

```bash
git add src/jass_runner/natives/__init__.py tests/natives/test_imports.py
git commit -m "feat: update natives module exports for state management"
```

---

### Task 11: 运行阶段1完整测试套件

**Files:**
- Test: 所有相关测试文件

**Step 1: 运行所有阶段1测试**

Run: `pytest tests/natives/test_handle.py tests/natives/test_manager.py tests/natives/test_state.py tests/integration/test_state_management_phase1.py -v`
Expected: 所有测试通过

**Step 2: 验证测试覆盖率**

Run: `pytest --cov=src/jass_runner/natives --cov-report=term-missing tests/natives/test_handle.py tests/natives/test_manager.py tests/natives/test_state.py tests/integration/test_state_management_phase1.py`
Expected: 显示覆盖率报告，关键模块应达到90%以上

**Step 3: 运行完整项目测试确保无回归**

Run: `pytest tests/ -v`
Expected: 所有现有测试通过，无回归

**Step 4: 提交最终状态**

```bash
git add .
git commit -m "feat: complete phase 1 of state management system - handle hierarchy and manager"
```

---

## 阶段1完成标准

1. ✅ **Handle类体系**：实现Handle基类和Unit子类
2. ✅ **HandleManager核心功能**：支持handle创建、查询、销毁、状态管理
3. ✅ **StateContext类**：管理全局和局部状态
4. ✅ **类型安全**：get_unit()等方法进行类型检查
5. ✅ **完整测试覆盖**：单元测试和集成测试
6. ✅ **无回归**：所有现有测试通过

## 下一步：阶段2实施计划

阶段2将专注于接口改造：
1. 修改NativeFunction基类，添加context参数
2. 修改ExecutionContext，集成StateContext
3. 修改Evaluator，传递context给native函数

计划保存为：`docs/plans/2026-02-26-jass-simulator-state-management-phase2-implementation.md`