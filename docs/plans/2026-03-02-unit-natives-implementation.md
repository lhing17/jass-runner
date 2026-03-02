# 单位操作 Native API 扩展实施计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 扩展单位操作相关 native 函数，支持单位状态设置、位置控制、朝向控制和单位信息查询

**Architecture:** 创建 Location 类管理位置信息，扩展 Unit handle 支持 z 坐标，新增 unit_property_natives 和 unit_position_natives 模块实现 native 函数

**Tech Stack:** Python 3.8+, pytest, 现有 HandleManager 和 NativeRegistry 框架

---

## 前置信息

### 相关设计文档
- `docs/plans/2026-03-02-unit-natives-design.md` - 详细设计文档

### 关键现有文件
- `src/jass_runner/natives/handle.py` - Unit/Player/Item handle 类
- `src/jass_runner/natives/basic.py` - 已实现的 CreateUnit, GetUnitState
- `src/jass_runner/natives/manager.py` - HandleManager 类
- `src/jass_runner/natives/factory.py` - NativeFactory 注册表

### 现有常量（basic.py 中已定义）
```python
UNIT_STATE_LIFE = 0
UNIT_STATE_MAX_LIFE = 1
UNIT_STATE_MANA = 2
UNIT_STATE_MAX_MANA = 3
```

---

## Task 1: 创建 Location 类

**Files:**
- Create: `src/jass_runner/natives/location.py`
- Test: `tests/natives/test_location.py`

**Step 1: 编写失败测试**

```python
def test_location_creation():
    """测试 Location 对象创建。"""
    from jass_runner.natives.location import Location

    loc = Location(100.0, 200.0)
    assert loc.x == 100.0
    assert loc.y == 200.0
    assert loc.z == 0.0  # 默认 z 为 0


def test_location_creation_with_z():
    """测试带 z 坐标的 Location 创建。"""
    from jass_runner.natives.location import Location

    loc = Location(100.0, 200.0, 50.0)
    assert loc.x == 100.0
    assert loc.y == 200.0
    assert loc.z == 50.0
```

**Step 2: 运行测试验证失败**

```bash
pytest tests/natives/test_location.py -v
```

Expected: FAIL with "ModuleNotFoundError: No module named 'jass_runner.natives.location'"

**Step 3: 实现 Location 类**

```python
"""Location 位置类实现。

此模块包含 JASS location 类型的实现，用于管理游戏世界中的位置坐标。
"""


class Location:
    """位置类，包含 x, y, z 坐标。

    属性：
        x: X 坐标（水平方向）
        y: Y 坐标（垂直方向）
        z: Z 坐标（高度），默认为 0
    """

    def __init__(self, x: float, y: float, z: float = 0.0):
        """初始化位置对象。

        参数：
            x: X 坐标
            y: Y 坐标
            z: Z 坐标（高度，默认为 0）
        """
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    def __repr__(self) -> str:
        """返回位置的字符串表示。"""
        return f"Location({self.x}, {self.y}, {self.z})"
```

**Step 4: 运行测试验证通过**

```bash
pytest tests/natives/test_location.py -v
```

Expected: PASS

**Step 5: 提交**

```bash
git add src/jass_runner/natives/location.py tests/natives/test_location.py
git commit -m "feat(natives): add Location class for position management"
```

---

## Task 2: 扩展 Unit 类添加 z 坐标

**Files:**
- Modify: `src/jass_runner/natives/handle.py`
- Test: `tests/natives/test_handle.py`

**Step 1: 编写失败测试**

```python
def test_unit_has_z_coordinate():
    """测试 Unit 对象有 z 坐标属性。"""
    from jass_runner.natives.handle import Unit

    unit = Unit("unit_001", "hfoo", 0, 100.0, 200.0, 0.0)
    assert hasattr(unit, 'z')
    assert unit.z == 0.0  # 默认 z 为 0


def test_unit_with_custom_z():
    """测试可以设置 Unit 的 z 坐标。"""
    from jass_runner.natives.handle import Unit

    unit = Unit("unit_001", "hfoo", 0, 100.0, 200.0, 0.0)
    unit.z = 50.0
    assert unit.z == 50.0
```

**Step 2: 运行测试验证失败**

```bash
pytest tests/natives/test_handle.py::test_unit_has_z_coordinate -v
```

Expected: FAIL with "AttributeError: 'Unit' object has no attribute 'z'"

**Step 3: 修改 Unit 类添加 z 坐标**

在 `src/jass_runner/natives/handle.py` 的 `Unit.__init__` 方法中添加：

```python
# 在 __init__ 中添加 z 坐标
self.z = 0.0  # Z 轴高度，默认为 0
```

**Step 4: 运行测试验证通过**

```bash
pytest tests/natives/test_handle.py -v
```

Expected: PASS（包括新测试和原有测试）

**Step 5: 提交**

```bash
git add src/jass_runner/natives/handle.py tests/natives/test_handle.py
git commit -m "feat(handle): add z coordinate to Unit class"
```

---

## Task 3: 扩展 HandleManager 支持 set_unit_state

**Files:**
- Modify: `src/jass_runner/natives/manager.py`
- Test: `tests/natives/test_manager.py`

**Step 1: 编写失败测试**

```python
def test_set_unit_state_life():
    """测试设置单位生命值。"""
    from jass_runner.natives.manager import HandleManager
    from jass_runner.natives.handle import Unit

    manager = HandleManager()
    unit = manager.create_unit("hfoo", 0, 100.0, 200.0, 0.0)

    # 设置生命值
    manager.set_unit_state(unit.id, "UNIT_STATE_LIFE", 80.0)

    # 验证
    life = manager.get_unit_state(unit.id, "UNIT_STATE_LIFE")
    assert life == 80.0


def test_set_unit_state_mana():
    """测试设置单位魔法值。"""
    from jass_runner.natives.manager import HandleManager

    manager = HandleManager()
    unit = manager.create_unit("hfoo", 0, 100.0, 200.0, 0.0)

    manager.set_unit_state(unit.id, "UNIT_STATE_MANA", 30.0)

    mana = manager.get_unit_state(unit.id, "UNIT_STATE_MANA")
    assert mana == 30.0
```

**Step 2: 运行测试验证失败**

```bash
pytest tests/natives/test_manager.py::test_set_unit_state_life -v
```

Expected: FAIL with "AttributeError: 'HandleManager' object has no attribute 'set_unit_state'"

**Step 3: 实现 set_unit_state 方法**

在 `src/jass_runner/natives/manager.py` 的 `HandleManager` 类中添加：

```python
def set_unit_state(self, unit_id: str, state_type: str, value: float):
    """设置单位状态值。

    参数：
        unit_id: 单位 ID
        state_type: 状态类型（如 "UNIT_STATE_LIFE"）
        value: 新的状态值

    返回：
        bool: 设置成功返回 True，否则返回 False
    """
    unit = self._handles.get(unit_id)
    if unit is None or not isinstance(unit, Unit):
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

    return False
```

**Step 4: 运行测试验证通过**

```bash
pytest tests/natives/test_manager.py -v
```

Expected: PASS

**Step 5: 提交**

```bash
git add src/jass_runner/natives/manager.py tests/natives/test_manager.py
git commit -m "feat(manager): add set_unit_state method to HandleManager"
```

---

## Task 4: 实现 SetUnitState native 函数

**Files:**
- Create: `src/jass_runner/natives/unit_property_natives.py`
- Modify: `src/jass_runner/natives/factory.py`（注册新函数）
- Test: `tests/natives/test_unit_property_natives.py`

**Step 1: 编写失败测试**

```python
def test_set_unit_state_native():
    """测试 SetUnitState native 函数。"""
    from jass_runner.natives.unit_property_natives import SetUnitState
    from jass_runner.natives.manager import HandleManager
    from jass_runner.natives.handle import Unit

    # 创建 HandleManager 和 unit
    manager = HandleManager()
    unit = manager.create_unit("hfoo", 0, 100.0, 200.0, 0.0)

    # 创建 native 函数
    set_unit_state = SetUnitState()

    # 创建 mock state_context
    class MockStateContext:
        def __init__(self):
            self.handle_manager = manager

    state_context = MockStateContext()

    # 设置生命值（UNIT_STATE_LIFE = 0）
    set_unit_state.execute(state_context, unit, 0, 75.0)

    # 验证
    assert unit.life == 75.0
```

**Step 2: 运行测试验证失败**

```bash
pytest tests/natives/test_unit_property_natives.py::test_set_unit_state_native -v
```

Expected: FAIL with "ModuleNotFoundError: No module named 'jass_runner.natives.unit_property_natives'"

**Step 3: 实现 SetUnitState native 函数**

创建 `src/jass_runner/natives/unit_property_natives.py`：

```python
"""单位属性 native 函数实现。

此模块包含单位属性访问和修改的 native 函数。
"""

import logging
from .base import NativeFunction
from .handle import Unit

logger = logging.getLogger(__name__)

# 单位状态类型常量
UNIT_STATE_LIFE = 0
UNIT_STATE_MAX_LIFE = 1
UNIT_STATE_MANA = 2
UNIT_STATE_MAX_MANA = 3


class SetUnitState(NativeFunction):
    """设置单位状态（生命值/魔法值）。"""

    @property
    def name(self) -> str:
        return "SetUnitState"

    def execute(self, state_context, unit: Unit, state_type: int, value: float):
        """执行 SetUnitState native 函数。

        参数：
            state_context: 状态上下文
            unit: 单位对象
            state_type: 状态类型（0=生命, 1=最大生命, 2=魔法, 3=最大魔法）
            value: 新的状态值
        """
        if unit is None:
            logger.warning("[SetUnitState] 尝试设置 None 单位的状态")
            return

        # 状态类型映射
        state_map = {
            UNIT_STATE_LIFE: "UNIT_STATE_LIFE",
            UNIT_STATE_MAX_LIFE: "UNIT_STATE_MAX_LIFE",
            UNIT_STATE_MANA: "UNIT_STATE_MANA",
            UNIT_STATE_MAX_MANA: "UNIT_STATE_MAX_MANA",
        }

        state_str = state_map.get(state_type)
        if state_str is None:
            logger.warning(f"[SetUnitState] 未知状态类型: {state_type}")
            return

        # 通过 HandleManager 设置状态
        handle_manager = state_context.handle_manager
        handle_manager.set_unit_state(unit.id, state_str, value)

        logger.debug(f"[SetUnitState] 单位 {unit.id} 的 {state_str} 设置为 {value}")
```

**Step 4: 在 Factory 中注册**

在 `src/jass_runner/natives/factory.py` 中添加导入和注册：

```python
# 添加导入
from .unit_property_natives import SetUnitState

# 在 create_default_registry 方法中添加注册
registry.register(SetUnitState())
```

**Step 5: 运行测试验证通过**

```bash
pytest tests/natives/test_unit_property_natives.py -v
```

Expected: PASS

**Step 6: 提交**

```bash
git add src/jass_runner/natives/unit_property_natives.py tests/natives/test_unit_property_natives.py src/jass_runner/natives/factory.py
git commit -m "feat(natives): add SetUnitState native function"
```

---

## Task 5: 实现位置查询函数（GetUnitX, GetUnitY, GetUnitLoc）

**Files:**
- Modify: `src/jass_runner/natives/unit_property_natives.py`
- Modify: `src/jass_runner/natives/factory.py`
- Test: `tests/natives/test_unit_property_natives.py`

**Step 1: 编写失败测试**

```python
def test_get_unit_x():
    """测试 GetUnitX native 函数。"""
    from jass_runner.natives.unit_property_natives import GetUnitX
    from jass_runner.natives.manager import HandleManager

    manager = HandleManager()
    unit = manager.create_unit("hfoo", 0, 150.0, 250.0, 0.0)

    get_unit_x = GetUnitX()

    class MockStateContext:
        def __init__(self):
            self.handle_manager = manager

    result = get_unit_x.execute(MockStateContext(), unit)
    assert result == 150.0


def test_get_unit_y():
    """测试 GetUnitY native 函数。"""
    from jass_runner.natives.unit_property_natives import GetUnitY
    from jass_runner.natives.manager import HandleManager

    manager = HandleManager()
    unit = manager.create_unit("hfoo", 0, 150.0, 250.0, 0.0)

    get_unit_y = GetUnitY()

    class MockStateContext:
        def __init__(self):
            self.handle_manager = manager

    result = get_unit_y.execute(MockStateContext(), unit)
    assert result == 250.0


def test_get_unit_loc():
    """测试 GetUnitLoc native 函数。"""
    from jass_runner.natives.unit_property_natives import GetUnitLoc
    from jass_runner.natives.location import Location
    from jass_runner.natives.manager import HandleManager

    manager = HandleManager()
    unit = manager.create_unit("hfoo", 0, 150.0, 250.0, 0.0)
    unit.z = 30.0  # 设置 z 坐标

    get_unit_loc = GetUnitLoc()

    class MockStateContext:
        def __init__(self):
            self.handle_manager = manager

    result = get_unit_loc.execute(MockStateContext(), unit)
    assert isinstance(result, Location)
    assert result.x == 150.0
    assert result.y == 250.0
    assert result.z == 30.0
```

**Step 2: 运行测试验证失败**

```bash
pytest tests/natives/test_unit_property_natives.py::test_get_unit_x -v
```

Expected: FAIL with "ImportError: cannot import name 'GetUnitX'"

**Step 3: 实现位置查询函数**

在 `src/jass_runner/natives/unit_property_natives.py` 中添加：

```python
from .location import Location


class GetUnitX(NativeFunction):
    """获取单位 X 坐标。"""

    @property
    def name(self) -> str:
        return "GetUnitX"

    def execute(self, state_context, unit: Unit) -> float:
        if unit is None:
            return 0.0
        return unit.x


class GetUnitY(NativeFunction):
    """获取单位 Y 坐标。"""

    @property
    def name(self) -> str:
        return "GetUnitY"

    def execute(self, state_context, unit: Unit) -> float:
        if unit is None:
            return 0.0
        return unit.y


class GetUnitLoc(NativeFunction):
    """获取单位位置（Location 对象）。"""

    @property
    def name(self) -> str:
        return "GetUnitLoc"

    def execute(self, state_context, unit: Unit) -> Location:
        if unit is None:
            return Location(0.0, 0.0, 0.0)
        return Location(unit.x, unit.y, unit.z)
```

**Step 4: 在 Factory 中注册**

在 `src/jass_runner/natives/factory.py` 中添加：

```python
from .unit_property_natives import SetUnitState, GetUnitX, GetUnitY, GetUnitLoc

# 注册
registry.register(GetUnitX())
registry.register(GetUnitY())
registry.register(GetUnitLoc())
```

**Step 5: 运行测试验证通过**

```bash
pytest tests/natives/test_unit_property_natives.py -v
```

Expected: PASS

**Step 6: 提交**

```bash
git add src/jass_runner/natives/unit_property_natives.py tests/natives/test_unit_property_natives.py src/jass_runner/natives/factory.py
git commit -m "feat(natives): add GetUnitX, GetUnitY, GetUnitLoc native functions"
```

---

## Task 6: 实现位置设置函数（SetUnitPosition, SetUnitPositionLoc）

**Files:**
- Create: `src/jass_runner/natives/unit_position_natives.py`
- Modify: `src/jass_runner/natives/factory.py`
- Test: `tests/natives/test_unit_position_natives.py`

**Step 1: 编写失败测试**

```python
def test_set_unit_position():
    """测试 SetUnitPosition native 函数。"""
    from jass_runner.natives.unit_position_natives import SetUnitPosition
    from jass_runner.natives.manager import HandleManager

    manager = HandleManager()
    unit = manager.create_unit("hfoo", 0, 100.0, 200.0, 0.0)

    set_unit_position = SetUnitPosition()

    class MockStateContext:
        def __init__(self):
            self.handle_manager = manager

    set_unit_position.execute(MockStateContext(), unit, 300.0, 400.0)

    assert unit.x == 300.0
    assert unit.y == 400.0


def test_set_unit_position_loc():
    """测试 SetUnitPositionLoc native 函数。"""
    from jass_runner.natives.unit_position_natives import SetUnitPositionLoc
    from jass_runner.natives.location import Location
    from jass_runner.natives.manager import HandleManager

    manager = HandleManager()
    unit = manager.create_unit("hfoo", 0, 100.0, 200.0, 0.0)

    set_unit_position_loc = SetUnitPositionLoc()
    loc = Location(500.0, 600.0, 50.0)

    class MockStateContext:
        def __init__(self):
            self.handle_manager = manager

    set_unit_position_loc.execute(MockStateContext(), unit, loc)

    assert unit.x == 500.0
    assert unit.y == 600.0
    assert unit.z == 50.0
```

**Step 2: 运行测试验证失败**

```bash
pytest tests/natives/test_unit_position_natives.py::test_set_unit_position -v
```

Expected: FAIL with "ModuleNotFoundError"

**Step 3: 实现位置设置函数**

创建 `src/jass_runner/natives/unit_position_natives.py`：

```python
"""单位位置操作 native 函数实现。

此模块包含单位位置设置和修改的 native 函数。
"""

import logging
from .base import NativeFunction
from .handle import Unit
from .location import Location

logger = logging.getLogger(__name__)


class SetUnitPosition(NativeFunction):
    """设置单位位置（使用坐标）。"""

    @property
    def name(self) -> str:
        return "SetUnitPosition"

    def execute(self, state_context, unit: Unit, x: float, y: float):
        """执行 SetUnitPosition native 函数。

        参数：
            state_context: 状态上下文
            unit: 单位对象
            x: 新的 X 坐标
            y: 新的 Y 坐标
        """
        if unit is None:
            logger.warning("[SetUnitPosition] 尝试设置 None 单位的位置")
            return

        unit.x = float(x)
        unit.y = float(y)

        logger.debug(f"[SetUnitPosition] 单位 {unit.id} 位置设置为 ({x}, {y})")


class SetUnitPositionLoc(NativeFunction):
    """设置单位位置（使用 Location）。"""

    @property
    def name(self) -> str:
        return "SetUnitPositionLoc"

    def execute(self, state_context, unit: Unit, loc: Location):
        """执行 SetUnitPositionLoc native 函数。

        参数：
            state_context: 状态上下文
            unit: 单位对象
            loc: Location 位置对象
        """
        if unit is None:
            logger.warning("[SetUnitPositionLoc] 尝试设置 None 单位的位置")
            return

        if loc is None:
            logger.warning("[SetUnitPositionLoc] Location 为 None")
            return

        unit.x = loc.x
        unit.y = loc.y
        unit.z = loc.z

        logger.debug(f"[SetUnitPositionLoc] 单位 {unit.id} 位置设置为 ({loc.x}, {loc.y}, {loc.z})")
```

**Step 4: 在 Factory 中注册**

在 `src/jass_runner/natives/factory.py` 中添加：

```python
from .unit_position_natives import SetUnitPosition, SetUnitPositionLoc

# 注册
registry.register(SetUnitPosition())
registry.register(SetUnitPositionLoc())
```

**Step 5: 运行测试验证通过**

```bash
pytest tests/natives/test_unit_position_natives.py -v
```

Expected: PASS

**Step 6: 提交**

```bash
git add src/jass_runner/natives/unit_position_natives.py tests/natives/test_unit_position_natives.py src/jass_runner/natives/factory.py
git commit -m "feat(natives): add SetUnitPosition and SetUnitPositionLoc native functions"
```

---

## Task 7: 实现 CreateUnitAtLoc native 函数

**Files:**
- Modify: `src/jass_runner/natives/unit_position_natives.py`
- Modify: `src/jass_runner/natives/factory.py`
- Test: `tests/natives/test_unit_position_natives.py`

**Step 1: 编写失败测试**

```python
def test_create_unit_at_loc():
    """测试 CreateUnitAtLoc native 函数。"""
    from jass_runner.natives.unit_position_natives import CreateUnitAtLoc
    from jass_runner.natives.location import Location
    from jass_runner.natives.manager import HandleManager

    manager = HandleManager()

    create_unit_at_loc = CreateUnitAtLoc()
    loc = Location(300.0, 400.0, 25.0)

    class MockStateContext:
        def __init__(self):
            self.handle_manager = manager

    # 创建单位（unit_type 使用 fourcc 整数）
    unit = create_unit_at_loc.execute(MockStateContext(), 0, 1213484355, loc, 90.0)

    assert unit is not None
    assert unit.x == 300.0
    assert unit.y == 400.0
    assert unit.z == 25.0
    assert unit.facing == 90.0
```

**Step 2: 运行测试验证失败**

```bash
pytest tests/natives/test_unit_position_natives.py::test_create_unit_at_loc -v
```

Expected: FAIL with "ImportError: cannot import name 'CreateUnitAtLoc'"

**Step 3: 实现 CreateUnitAtLoc**

在 `src/jass_runner/natives/unit_position_natives.py` 中添加：

```python
from .utils import int_to_fourcc


class CreateUnitAtLoc(NativeFunction):
    """在指定位置创建单位（使用 Location）。"""

    @property
    def name(self) -> str:
        return "CreateUnitAtLoc"

    def execute(self, state_context, player_id: int, unit_type: int,
                loc: Location, facing: float):
        """执行 CreateUnitAtLoc native 函数。

        参数：
            state_context: 状态上下文
            player_id: 玩家 ID
            unit_type: 单位类型代码（fourcc 整数格式）
            loc: Location 位置对象
            facing: 面向角度

        返回：
            Unit: 创建的单位对象
        """
        if loc is None:
            logger.warning("[CreateUnitAtLoc] Location 为 None")
            return None

        # 将 fourcc 整数转换为字符串
        unit_type_str = int_to_fourcc(unit_type)

        # 通过 HandleManager 创建单位
        handle_manager = state_context.handle_manager
        unit = handle_manager.create_unit(unit_type_str, player_id,
                                          loc.x, loc.y, facing)

        # 设置 z 坐标
        unit.z = loc.z

        logger.info(f"[CreateUnitAtLoc] 为玩家 {player_id} 在 {loc} 创建 {unit_type_str}，单位 ID: {unit.id}")
        return unit
```

**Step 4: 在 Factory 中注册**

在 `src/jass_runner/natives/factory.py` 中添加：

```python
from .unit_position_natives import SetUnitPosition, SetUnitPositionLoc, CreateUnitAtLoc

# 注册
registry.register(CreateUnitAtLoc())
```

**Step 5: 运行测试验证通过**

```bash
pytest tests/natives/test_unit_position_natives.py -v
```

Expected: PASS

**Step 6: 提交**

```bash
git add src/jass_runner/natives/unit_position_natives.py tests/natives/test_unit_position_natives.py src/jass_runner/natives/factory.py
git commit -m "feat(natives): add CreateUnitAtLoc native function"
```

---

## Task 8: 实现朝向控制函数（GetUnitFacing, SetUnitFacing）

**Files:**
- Modify: `src/jass_runner/natives/unit_position_natives.py`
- Modify: `src/jass_runner/natives/factory.py`
- Test: `tests/natives/test_unit_position_natives.py`

**Step 1: 编写失败测试**

```python
def test_get_unit_facing():
    """测试 GetUnitFacing native 函数。"""
    from jass_runner.natives.unit_position_natives import GetUnitFacing
    from jass_runner.natives.manager import HandleManager

    manager = HandleManager()
    unit = manager.create_unit("hfoo", 0, 100.0, 200.0, 45.0)

    get_unit_facing = GetUnitFacing()

    class MockStateContext:
        def __init__(self):
            self.handle_manager = manager

    result = get_unit_facing.execute(MockStateContext(), unit)
    assert result == 45.0


def test_set_unit_facing():
    """测试 SetUnitFacing native 函数。"""
    from jass_runner.natives.unit_position_natives import SetUnitFacing
    from jass_runner.natives.manager import HandleManager

    manager = HandleManager()
    unit = manager.create_unit("hfoo", 0, 100.0, 200.0, 0.0)

    set_unit_facing = SetUnitFacing()

    class MockStateContext:
        def __init__(self):
            self.handle_manager = manager

    set_unit_facing.execute(MockStateContext(), unit, 180.0)
    assert unit.facing == 180.0
```

**Step 2: 运行测试验证失败**

```bash
pytest tests/natives/test_unit_position_natives.py::test_get_unit_facing -v
```

Expected: FAIL with "ImportError"

**Step 3: 实现朝向控制函数**

在 `src/jass_runner/natives/unit_position_natives.py` 中添加：

```python
class GetUnitFacing(NativeFunction):
    """获取单位朝向角度。"""

    @property
    def name(self) -> str:
        return "GetUnitFacing"

    def execute(self, state_context, unit: Unit) -> float:
        """执行 GetUnitFacing native 函数。

        参数：
            state_context: 状态上下文
            unit: 单位对象

        返回：
            float: 单位朝向角度（度）
        """
        if unit is None:
            return 0.0
        return unit.facing


class SetUnitFacing(NativeFunction):
    """设置单位朝向角度。"""

    @property
    def name(self) -> str:
        return "SetUnitFacing"

    def execute(self, state_context, unit: Unit, facing_angle: float):
        """执行 SetUnitFacing native 函数。

        参数：
            state_context: 状态上下文
            unit: 单位对象
            facing_angle: 新的朝向角度（度）
        """
        if unit is None:
            logger.warning("[SetUnitFacing] 尝试设置 None 单位的朝向")
            return

        unit.facing = float(facing_angle)
        logger.debug(f"[SetUnitFacing] 单位 {unit.id} 朝向设置为 {facing_angle}")
```

**Step 4: 在 Factory 中注册**

在 `src/jass_runner/natives/factory.py` 中添加：

```python
from .unit_position_natives import (
    SetUnitPosition, SetUnitPositionLoc, CreateUnitAtLoc,
    GetUnitFacing, SetUnitFacing
)

# 注册
registry.register(GetUnitFacing())
registry.register(SetUnitFacing())
```

**Step 5: 运行测试验证通过**

```bash
pytest tests/natives/test_unit_position_natives.py -v
```

Expected: PASS

**Step 6: 提交**

```bash
git add src/jass_runner/natives/unit_position_natives.py tests/natives/test_unit_position_natives.py src/jass_runner/natives/factory.py
git commit -m "feat(natives): add GetUnitFacing and SetUnitFacing native functions"
```

---

## Task 9: 实现单位信息查询函数（GetUnitTypeId, GetUnitName）

**Files:**
- Modify: `src/jass_runner/natives/unit_property_natives.py`
- Modify: `src/jass_runner/natives/handle.py`（添加 name 属性）
- Modify: `src/jass_runner/natives/factory.py`
- Test: `tests/natives/test_unit_property_natives.py`

**Step 1: 扩展 Unit 类添加 name 属性**

首先修改 `src/jass_runner/natives/handle.py` 中的 `Unit` 类：

```python
# 在 Unit.__init__ 中添加 name 参数
def __init__(self, handle_id: str, unit_type: str, player_id: int,
             x: float, y: float, facing: float, name: str = None):
    # ... 现有代码 ...
    self.name = name or unit_type  # 如果没有提供名称，使用单位类型
```

**Step 2: 编写失败测试**

```python
def test_get_unit_type_id():
    """测试 GetUnitTypeId native 函数。"""
    from jass_runner.natives.unit_property_natives import GetUnitTypeId
    from jass_runner.natives.manager import HandleManager
    from jass_runner.utils import fourcc_to_int

    manager = HandleManager()
    unit = manager.create_unit("hfoo", 0, 100.0, 200.0, 0.0)

    get_unit_type_id = GetUnitTypeId()

    class MockStateContext:
        def __init__(self):
            self.handle_manager = manager

    result = get_unit_type_id.execute(MockStateContext(), unit)

    # "hfoo" 转换为整数
    expected = fourcc_to_int("hfoo")
    assert result == expected


def test_get_unit_name():
    """测试 GetUnitName native 函数。"""
    from jass_runner.natives.unit_property_natives import GetUnitName
    from jass_runner.natives.manager import HandleManager

    manager = HandleManager()
    unit = manager.create_unit("hfoo", 0, 100.0, 200.0, 0.0)

    get_unit_name = GetUnitName()

    class MockStateContext:
        def __init__(self):
            self.handle_manager = manager

    result = get_unit_name.execute(MockStateContext(), unit)
    assert result == "hfoo"  # 默认使用 unit_type 作为名称
```

**Step 3: 运行测试验证失败**

```bash
pytest tests/natives/test_unit_property_natives.py::test_get_unit_type_id -v
```

Expected: FAIL with "ImportError"

**Step 4: 实现单位信息查询函数**

在 `src/jass_runner/natives/unit_property_natives.py` 中添加：

```python
from .utils import fourcc_to_int


class GetUnitTypeId(NativeFunction):
    """获取单位类型 ID。"""

    @property
    def name(self) -> str:
        return "GetUnitTypeId"

    def execute(self, state_context, unit: Unit) -> int:
        """执行 GetUnitTypeId native 函数。

        参数：
            state_context: 状态上下文
            unit: 单位对象

        返回：
            int: 单位类型 ID（fourcc 整数格式）
        """
        if unit is None:
            return 0
        return fourcc_to_int(unit.unit_type)


class GetUnitName(NativeFunction):
    """获取单位名称。"""

    @property
    def name(self) -> str:
        return "GetUnitName"

    def execute(self, state_context, unit: Unit) -> str:
        """执行 GetUnitName native 函数。

        参数：
            state_context: 状态上下文
            unit: 单位对象

        返回：
            str: 单位名称
        """
        if unit is None:
            return ""
        return unit.name
```

**Step 5: 在 Factory 中注册**

在 `src/jass_runner/natives/factory.py` 中添加：

```python
from .unit_property_natives import (
    SetUnitState, GetUnitX, GetUnitY, GetUnitLoc,
    GetUnitTypeId, GetUnitName
)

# 注册
registry.register(GetUnitTypeId())
registry.register(GetUnitName())
```

**Step 6: 运行测试验证通过**

```bash
pytest tests/natives/test_unit_property_natives.py -v
```

Expected: PASS

**Step 7: 提交**

```bash
git add src/jass_runner/natives/unit_property_natives.py src/jass_runner/natives/handle.py tests/natives/test_unit_property_natives.py src/jass_runner/natives/factory.py
git commit -m "feat(natives): add GetUnitTypeId and GetUnitName native functions"
```

---

## Task 10: 实现 CreateUnitAtLocByName native 函数

**Files:**
- Modify: `src/jass_runner/natives/unit_position_natives.py`
- Modify: `src/jass_runner/natives/factory.py`
- Test: `tests/natives/test_unit_position_natives.py`

**Step 1: 编写失败测试**

```python
def test_create_unit_at_loc_by_name():
    """测试 CreateUnitAtLocByName native 函数。"""
    from jass_runner.natives.unit_position_natives import CreateUnitAtLocByName
    from jass_runner.natives.location import Location
    from jass_runner.natives.manager import HandleManager

    manager = HandleManager()

    create_unit_at_loc_by_name = CreateUnitAtLocByName()
    loc = Location(700.0, 800.0, 0.0)

    class MockStateContext:
        def __init__(self):
            self.handle_manager = manager

    # 使用单位名称创建（如 "footman"）
    unit = create_unit_at_loc_by_name.execute(MockStateContext(), 0, "footman", loc, 270.0)

    assert unit is not None
    assert unit.x == 700.0
    assert unit.y == 800.0
    assert unit.facing == 270.0
```

**Step 2: 运行测试验证失败**

```bash
pytest tests/natives/test_unit_position_natives.py::test_create_unit_at_loc_by_name -v
```

Expected: FAIL with "ImportError"

**Step 3: 实现 CreateUnitAtLocByName**

在 `src/jass_runner/natives/unit_position_natives.py` 中添加：

```python
class CreateUnitAtLocByName(NativeFunction):
    """在指定位置按名称创建单位。"""

    @property
    def name(self) -> str:
        return "CreateUnitAtLocByName"

    def execute(self, state_context, player_id: int, unit_name: str,
                loc: Location, facing: float):
        """执行 CreateUnitAtLocByName native 函数。

        参数：
            state_context: 状态上下文
            player_id: 玩家 ID
            unit_name: 单位名称（如 "footman"）
            loc: Location 位置对象
            facing: 面向角度

        返回：
            Unit: 创建的单位对象
        """
        if loc is None:
            logger.warning("[CreateUnitAtLocByName] Location 为 None")
            return None

        if not unit_name:
            logger.warning("[CreateUnitAtLocByName] 单位名称为空")
            return None

        # 名称到单位类型的映射（简化实现）
        name_to_type = {
            "footman": "hfoo",
            "peasant": "hpea",
            "knight": "hkni",
            "archer": "earc",
            "grunt": "ogru",
        }

        unit_type = name_to_type.get(unit_name.lower(), unit_name[:4].lower())

        # 通过 HandleManager 创建单位
        handle_manager = state_context.handle_manager
        unit = handle_manager.create_unit(unit_type, player_id,
                                          loc.x, loc.y, facing)

        # 设置 z 坐标和名称
        unit.z = loc.z
        unit.name = unit_name

        logger.info(f"[CreateUnitAtLocByName] 为玩家 {player_id} 在 {loc} 创建 {unit_name} ({unit_type})，单位 ID: {unit.id}")
        return unit
```

**Step 4: 在 Factory 中注册**

在 `src/jass_runner/natives/factory.py` 中添加：

```python
from .unit_position_natives import (
    SetUnitPosition, SetUnitPositionLoc, CreateUnitAtLoc,
    GetUnitFacing, SetUnitFacing, CreateUnitAtLocByName
)

# 注册
registry.register(CreateUnitAtLocByName())
```

**Step 5: 运行测试验证通过**

```bash
pytest tests/natives/test_unit_position_natives.py -v
```

Expected: PASS

**Step 6: 提交**

```bash
git add src/jass_runner/natives/unit_position_natives.py tests/natives/test_unit_position_natives.py src/jass_runner/natives/factory.py
git commit -m "feat(natives): add CreateUnitAtLocByName native function"
```

---

## Task 11: 创建集成测试

**Files:**
- Create: `tests/integration/test_unit_natives.py`

**Step 1: 编写集成测试**

```python
"""单位操作 native 函数集成测试。"""

from jass_runner.vm.jass_vm import JassVM


class TestUnitNativesIntegration:
    """测试单位 native 函数完整工作流。"""

    def test_unit_lifecycle_workflow(self):
        """测试单位完整生命周期。"""
        code = '''
        function main takes nothing returns nothing
            local unit u
            // 创建单位
            set u = CreateUnit(Player(0), 'hfoo', 100.0, 200.0, 0.0)

            // 获取并设置状态
            call SetUnitState(u, UNIT_STATE_LIFE, 80.0)

            // 获取位置
            local real x = GetUnitX(u)
            local real y = GetUnitY(u)

            // 设置新位置
            call SetUnitPosition(u, 300.0, 400.0)

            // 设置朝向
            call SetUnitFacing(u, 90.0)
            local real facing = GetUnitFacing(u)

            // 获取单位信息
            local integer type_id = GetUnitTypeId(u)
            local string name = GetUnitName(u)

            // 杀死单位
            call KillUnit(u)
        endfunction
        '''

        vm = JassVM()
        vm.load_script(code)
        vm.execute()

    def test_create_unit_at_loc_workflow(self):
        """测试使用 Location 创建单位。"""
        code = '''
        function main takes nothing returns nothing
            local location loc = Location(500.0, 600.0)
            local unit u = CreateUnitAtLoc(Player(0), 'hfoo', loc, 45.0)

            // 验证位置
            local real x = GetUnitX(u)
            local real y = GetUnitY(u)

            // 清理
            call RemoveLocation(loc)
            call KillUnit(u)
        endfunction
        '''

        vm = JassVM()
        vm.load_script(code)
        vm.execute()
```

**Step 2: 运行测试验证通过**

```bash
pytest tests/integration/test_unit_natives.py -v
```

Expected: PASS（可能需要先实现 Location 和 RemoveLocation）

**Step 3: 提交**

```bash
git add tests/integration/test_unit_natives.py
git commit -m "test(integration): add unit natives integration tests"
```

---

## Task 12: 更新项目文档

**Files:**
- Modify: `PROJECT_NOTES.md`
- Modify: `TODO.md`

**Step 1: 更新 PROJECT_NOTES.md**

在文档末尾添加：

```markdown
#### 43. 单位操作 Native API 扩展完成 (2026-03-02)
- **新增组件**:
  - `Location` 类 - 位置管理（x, y, z 坐标）
  - `unit_property_natives.py` - 单位属性操作
  - `unit_position_natives.py` - 单位位置操作
- **新增 Native 函数**（13 个）:
  - 状态管理: SetUnitState
  - 位置查询: GetUnitX, GetUnitY, GetUnitLoc
  - 位置设置: SetUnitPosition, SetUnitPositionLoc, CreateUnitAtLoc
  - 朝向控制: GetUnitFacing, SetUnitFacing
  - 单位信息: GetUnitTypeId, GetUnitName, CreateUnitAtLocByName
- **Unit 类扩展**:
  - 添加 z 坐标属性（默认为 0）
  - 添加 name 属性
- **HandleManager 扩展**:
  - 添加 set_unit_state 方法
- **测试覆盖**:
  - 单元测试: Location, Unit handle, 每个 native 函数
  - 集成测试: 完整单位生命周期工作流
```

**Step 2: 更新 TODO.md**

更新 native API 实现状态：

```markdown
### Native API 实现状态

- [x] **基础单位操作**: CreateUnit, KillUnit, GetUnitState, SetUnitState
- [x] **位置操作**: GetUnitX/Y/Loc, SetUnitPosition, CreateUnitAtLoc
- [x] **朝向控制**: GetUnitFacing, SetUnitFacing
- [x] **单位信息**: GetUnitTypeId, GetUnitName
- [ ] **单位组操作**: CreateGroup, GroupAddUnit, ForGroup（未来版本）
- [ ] **技能系统**: UnitAddAbility, GetUnitAbilityLevel（未来版本）
```

**Step 3: 提交**

```bash
git add PROJECT_NOTES.md TODO.md
git commit -m "docs: update project notes for unit natives completion"
```

---

## 实施完成检查清单

- [ ] Task 1: Location 类
- [ ] Task 2: Unit 类扩展 z 坐标
- [ ] Task 3: HandleManager set_unit_state
- [ ] Task 4: SetUnitState native
- [ ] Task 5: GetUnitX/Y/Loc natives
- [ ] Task 6: SetUnitPosition/SetUnitPositionLoc natives
- [ ] Task 7: CreateUnitAtLoc native
- [ ] Task 8: GetUnitFacing/SetUnitFacing natives
- [ ] Task 9: GetUnitTypeId/GetUnitName natives
- [ ] Task 10: CreateUnitAtLocByName native
- [ ] Task 11: 集成测试
- [ ] Task 12: 更新文档

---

## 注意事项

1. **与现有代码兼容**: 所有新函数不应破坏现有的 CreateUnit/GetUnitState 功能
2. **HandleManager 依赖**: Task 3 必须在 Task 4 之前完成
3. **Location 依赖**: Task 1 必须在 Task 5 之前完成
4. **测试策略**: 每个 native 函数都有独立测试 + 集成测试
5. **fourcc 转换**: 使用现有的 `int_to_fourcc` 和 `fourcc_to_int` 工具函数
