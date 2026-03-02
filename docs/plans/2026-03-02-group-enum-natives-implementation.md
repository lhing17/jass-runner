# 单位组枚举Native函数实现计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 实现第三批单位组枚举Native函数（GroupEnumUnitsOfPlayer, GroupEnumUnitsInRange, GroupEnumUnitsInRangeOfLoc, GroupEnumUnitsInRect, BlzGroupGetSize, BlzGroupUnitAt）

**Architecture:** 扩展Group类和HandleManager，支持按条件筛选单位并添加到组中。枚举函数通过查询HandleManager中的单位，根据条件（玩家、范围、矩形区域）筛选后添加到指定组。

**Tech Stack:** Python 3.8+, pytest, 现有Native函数框架

---

## 前置信息

### 相关设计文档
- `resources/common.j` - Native函数定义参考（第4635-4669行）
- `docs/plans/2026-03-02-group-natives-implementation.md` - 单位组核心实现参考

### 关键现有文件
- `src/jass_runner/natives/handle.py` - Handle基类、Unit类、Group类
- `src/jass_runner/natives/manager.py` - HandleManager类
- `src/jass_runner/natives/group_natives.py` - 单位组Native函数实现
- `src/jass_runner/natives/location.py` - Location类

### 枚举函数原型（来自common.j）
```jass
native GroupEnumUnitsOfPlayer takes group whichGroup, player whichPlayer, boolexpr filter returns nothing
native GroupEnumUnitsInRange takes group whichGroup, real x, real y, real radius, boolexpr filter returns nothing
native GroupEnumUnitsInRangeOfLoc takes group whichGroup, location whichLocation, real radius, boolexpr filter returns nothing
native GroupEnumUnitsInRect takes group whichGroup, rect r, boolexpr filter returns nothing
native BlzGroupGetSize takes group whichGroup returns integer
native BlzGroupUnitAt takes group whichGroup, integer index returns unit
```

---

## Task 1: 在Group类中添加枚举支持

**Files:**
- Modify: `src/jass_runner/natives/handle.py`
- Test: `tests/natives/test_group_enum.py`（新建）

**Step 1: 编写失败测试**

创建 `tests/natives/test_group_enum.py`：

```python
"""单位组枚举功能测试。"""

import pytest
from jass_runner.natives.handle import Group, Unit


class TestGroupEnumSupport:
    """测试Group类枚举支持功能。"""

    def test_group_get_size_empty(self):
        """测试获取空组大小。"""
        group = Group("group_1")
        assert group.get_size() == 0

    def test_group_get_size_with_units(self):
        """测试获取有单位的组大小。"""
        group = Group("group_1")
        unit1 = Unit("unit_1", "hfoo", 0, 100.0, 200.0, 0.0)
        unit2 = Unit("unit_2", "hfoo", 0, 150.0, 250.0, 0.0)
        group.add_unit(unit1)
        group.add_unit(unit2)

        assert group.get_size() == 2

    def test_group_unit_at_valid_index(self):
        """测试获取有效索引的单位。"""
        group = Group("group_1")
        unit = Unit("unit_1", "hfoo", 0, 100.0, 200.0, 0.0)
        group.add_unit(unit)

        result = group.unit_at(0)

        assert result == unit.id

    def test_group_unit_at_invalid_index(self):
        """测试获取无效索引返回None。"""
        group = Group("group_1")

        result = group.unit_at(0)

        assert result is None

    def test_group_unit_at_negative_index(self):
        """测试获取负索引返回None。"""
        group = Group("group_1")
        unit = Unit("unit_1", "hfoo", 0, 100.0, 200.0, 0.0)
        group.add_unit(unit)

        result = group.unit_at(-1)

        assert result is None
```

**Step 2: 运行测试验证失败**

```bash
pytest tests/natives/test_group_enum.py -v
```

Expected: FAIL（Group类没有get_size和unit_at方法）

**Step 3: 在Group类中添加枚举支持**

在 `src/jass_runner/natives/handle.py` 的Group类中添加以下方法（在size方法之后）：

```python
def get_size(self) -> int:
    """获取组内单位数量。

    返回：
        单位数量
    """
    return len(self._units)

def unit_at(self, index: int) -> Optional[str]:
    """获取指定索引位置的单位ID。

    注意: 由于set是无序的，索引位置不保证稳定。
    这个方法主要用于BlzGroupUnitAt的兼容性实现。

    参数：
        index: 索引位置（从0开始）

    返回：
        单位ID，如果索引无效返回None
    """
    if index < 0 or index >= len(self._units):
        return None

    # 将set转换为list进行索引访问
    # 注意: 顺序不保证稳定
    units_list = list(self._units)
    return units_list[index]
```

**Step 4: 运行测试验证通过**

```bash
pytest tests/natives/test_group_enum.py -v
```

Expected: PASS

**Step 5: 提交**

```bash
git add src/jass_runner/natives/handle.py tests/natives/test_group_enum.py
git commit -m "feat(handle): add get_size and unit_at methods to Group class"
```

---

## Task 2: 在HandleManager中添加单位枚举支持

**Files:**
- Modify: `src/jass_runner/natives/manager.py`
- Test: `tests/natives/test_manager_enum.py`（新建）

**Step 1: 编写失败测试**

创建 `tests/natives/test_manager_enum.py`：

```python
"""HandleManager枚举功能测试。"""

import pytest
from jass_runner.natives.manager import HandleManager


class TestHandleManagerEnum:
    """测试HandleManager单位枚举功能。"""

    def test_enum_units_of_player(self):
        """测试按玩家枚举单位。"""
        manager = HandleManager()
        unit1 = manager.create_unit("hfoo", 0, 100.0, 200.0, 0.0)
        unit2 = manager.create_unit("hfoo", 0, 150.0, 250.0, 0.0)
        unit3 = manager.create_unit("hfoo", 1, 300.0, 400.0, 0.0)  # 不同玩家

        result = manager.enum_units_of_player(0)

        assert len(result) == 2
        assert unit1.id in result
        assert unit2.id in result
        assert unit3.id not in result

    def test_enum_units_in_range(self):
        """测试在范围内枚举单位。"""
        manager = HandleManager()
        unit1 = manager.create_unit("hfoo", 0, 100.0, 200.0, 0.0)  # 距离0
        unit2 = manager.create_unit("hfoo", 0, 150.0, 200.0, 0.0)  # 距离50
        unit3 = manager.create_unit("hfoo", 0, 300.0, 200.0, 0.0)  # 距离200，超出范围

        result = manager.enum_units_in_range(100.0, 200.0, 100.0)  # 中心(100,200)，半径100

        assert len(result) == 2
        assert unit1.id in result
        assert unit2.id in result
        assert unit3.id not in result

    def test_enum_units_in_range_no_units(self):
        """测试在范围内没有单位。"""
        manager = HandleManager()
        manager.create_unit("hfoo", 0, 1000.0, 2000.0, 0.0)  # 远离中心

        result = manager.enum_units_in_range(0.0, 0.0, 100.0)

        assert len(result) == 0
```

**Step 2: 运行测试验证失败**

```bash
pytest tests/natives/test_manager_enum.py -v
```

Expected: FAIL（HandleManager没有enum方法）

**Step 3: 在HandleManager中添加枚举支持**

在 `src/jass_runner/natives/manager.py` 中添加以下方法（在文件末尾，kill_unit方法之后）：

```python
def enum_units_of_player(self, player_id: int) -> List[str]:
    """枚举指定玩家的所有单位。

    参数：
        player_id: 玩家ID

    返回：
        单位ID列表
    """
    result = []
    type_name = "unit"

    if type_name not in self._type_index:
        return result

    for handle_id in self._type_index[type_name]:
        handle = self._handles.get(handle_id)
        if handle and handle.is_alive() and isinstance(handle, Unit):
            if handle.player_id == player_id:
                result.append(handle_id)

    return result

def enum_units_in_range(self, x: float, y: float, radius: float) -> List[str]:
    """枚举指定范围内的所有单位。

    参数：
        x: 中心X坐标
        y: 中心Y坐标
        radius: 半径

    返回：
        单位ID列表
    """
    result = []
    type_name = "unit"

    if type_name not in self._type_index:
        return result

    radius_sq = radius * radius

    for handle_id in self._type_index[type_name]:
        handle = self._handles.get(handle_id)
        if handle and handle.is_alive() and isinstance(handle, Unit):
            # 计算距离平方（避免开方）
            dx = handle.x - x
            dy = handle.y - y
            dist_sq = dx * dx + dy * dy

            if dist_sq <= radius_sq:
                result.append(handle_id)

    return result

def enum_units_of_type(self, unit_type: str) -> List[str]:
    """枚举指定类型的所有单位。

    参数：
        unit_type: 单位类型代码（如'hfoo'）

    返回：
        单位ID列表
    """
    result = []
    type_name = "unit"

    if type_name not in self._type_index:
        return result

    for handle_id in self._type_index[type_name]:
        handle = self._handles.get(handle_id)
        if handle and handle.is_alive() and isinstance(handle, Unit):
            if handle.unit_type == unit_type:
                result.append(handle_id)

    return result
```

注意：需要在文件顶部添加导入：
```python
from typing import Dict, List, Optional  # 添加List
```

**Step 4: 运行测试验证通过**

```bash
pytest tests/natives/test_manager_enum.py -v
```

Expected: PASS

**Step 5: 提交**

```bash
git add src/jass_runner/natives/manager.py tests/natives/test_manager_enum.py
git commit -m "feat(manager): add unit enumeration methods to HandleManager"
```

---

## Task 3: 实现BlzGroupGetSize和BlzGroupUnitAt

**Files:**
- Modify: `src/jass_runner/natives/group_natives.py`
- Modify: `src/jass_runner/natives/factory.py`
- Test: `tests/natives/test_group_blz.py`（新建）

**Step 1: 编写失败测试**

创建 `tests/natives/test_group_blz.py`：

```python
"""Blz单位组Native函数测试。"""

import pytest
from jass_runner.natives.state import StateContext
from jass_runner.natives.group_natives import (
    CreateGroup, GroupAddUnit, BlzGroupGetSize, BlzGroupUnitAt
)


class TestBlzGroupGetSize:
    """测试BlzGroupGetSize native函数。"""

    def test_get_size_of_empty_group(self):
        """测试获取空组大小。"""
        state = StateContext()
        create_group = CreateGroup()
        get_size = BlzGroupGetSize()

        group = create_group.execute(state)
        result = get_size.execute(state, group)

        assert result == 0

    def test_get_size_of_group_with_units(self):
        """测试获取有单位的组大小。"""
        state = StateContext()
        create_group = CreateGroup()
        add_unit = GroupAddUnit()
        get_size = BlzGroupGetSize()

        group = create_group.execute(state)
        unit1 = state.handle_manager.create_unit("hfoo", 0, 100.0, 200.0, 0.0)
        unit2 = state.handle_manager.create_unit("hfoo", 0, 150.0, 250.0, 0.0)
        add_unit.execute(state, group, unit1)
        add_unit.execute(state, group, unit2)

        result = get_size.execute(state, group)

        assert result == 2


class TestBlzGroupUnitAt:
    """测试BlzGroupUnitAt native函数。"""

    def test_get_unit_at_valid_index(self):
        """测试获取有效索引的单位。"""
        state = StateContext()
        create_group = CreateGroup()
        add_unit = GroupAddUnit()
        get_unit = BlzGroupUnitAt()

        group = create_group.execute(state)
        unit = state.handle_manager.create_unit("hfoo", 0, 100.0, 200.0, 0.0)
        add_unit.execute(state, group, unit)

        result = get_unit.execute(state, group, 0)

        assert result == unit

    def test_get_unit_at_invalid_index(self):
        """测试获取无效索引返回None。"""
        state = StateContext()
        create_group = CreateGroup()
        get_unit = BlzGroupUnitAt()

        group = create_group.execute(state)

        result = get_unit.execute(state, group, 0)

        assert result is None
```

**Step 2: 运行测试验证失败**

```bash
pytest tests/natives/test_group_blz.py -v
```

Expected: FAIL（BlzGroupGetSize和BlzGroupUnitAt不存在）

**Step 3: 实现两个Native函数**

在 `src/jass_runner/natives/group_natives.py` 中添加（放在ForGroup类之后）：

```python
class BlzGroupGetSize(NativeFunction):
    """获取单位组的大小（单位数量）。

    对应JASS native函数: integer BlzGroupGetSize(group whichGroup)

    这是暴雪扩展函数（Blz前缀），用于获取组内单位数量。
    """

    @property
    def name(self) -> str:
        """获取函数名称。"""
        return "BlzGroupGetSize"

    def execute(self, state_context, group: Group) -> int:
        """执行BlzGroupGetSize native函数。

        参数：
            state_context: 状态上下文
            group: 单位组

        返回：
            组内单位数量，如果组为None返回0
        """
        if group is None:
            return 0

        return group.get_size()


class BlzGroupUnitAt(NativeFunction):
    """获取单位组中指定索引的单位。

    对应JASS native函数: unit BlzGroupUnitAt(group whichGroup, integer index)

    这是暴雪扩展函数（Blz前缀），用于按索引访问组内单位。
    注意: 由于set是无序的，索引位置不保证稳定。
    """

    @property
    def name(self) -> str:
        """获取函数名称。"""
        return "BlzGroupUnitAt"

    def execute(self, state_context, group: Group, index: int) -> Optional[Unit]:
        """执行BlzGroupUnitAt native函数。

        参数：
            state_context: 状态上下文
            group: 单位组
            index: 索引位置（从0开始）

        返回：
            单位对象，如果索引无效或组为None返回None
        """
        if group is None:
            return None

        unit_id = group.unit_at(index)
        if unit_id is None:
            return None

        # 通过HandleManager获取单位对象
        handle_manager = state_context.handle_manager
        unit = handle_manager.get_unit(unit_id)

        return unit
```

**Step 4: 注册到NativeFactory**

在 `src/jass_runner/natives/factory.py` 中：

1. 更新group_natives导入，添加BlzGroupGetSize和BlzGroupUnitAt

2. 添加注册：
```python
registry.register(BlzGroupGetSize())
registry.register(BlzGroupUnitAt())
```

**Step 5: 运行测试验证通过**

```bash
pytest tests/natives/test_group_blz.py -v
```

Expected: PASS

**Step 6: 提交**

```bash
git add src/jass_runner/natives/group_natives.py src/jass_runner/natives/factory.py tests/natives/test_group_blz.py
git commit -m "feat(natives): add BlzGroupGetSize and BlzGroupUnitAt native functions"
```

---

## Task 4: 实现GroupEnumUnitsOfPlayer

**Files:**
- Modify: `src/jass_runner/natives/group_natives.py`
- Modify: `src/jass_runner/natives/factory.py`
- Test: `tests/natives/test_group_enum_natives.py`（新建）

**Step 1: 编写失败测试**

创建 `tests/natives/test_group_enum_natives.py`：

```python
"""单位组枚举Native函数测试。"""

import pytest
from jass_runner.natives.state import StateContext
from jass_runner.natives.group_natives import (
    CreateGroup, GroupEnumUnitsOfPlayer, BlzGroupGetSize
)


class TestGroupEnumUnitsOfPlayer:
    """测试GroupEnumUnitsOfPlayer native函数。"""

    def test_enum_units_of_player(self):
        """测试按玩家枚举单位到组。"""
        state = StateContext()
        create_group = CreateGroup()
        enum_units = GroupEnumUnitsOfPlayer()
        get_size = BlzGroupGetSize()

        group = create_group.execute(state)
        # 创建玩家0的单位
        unit1 = state.handle_manager.create_unit("hfoo", 0, 100.0, 200.0, 0.0)
        unit2 = state.handle_manager.create_unit("hfoo", 0, 150.0, 250.0, 0.0)
        # 创建玩家1的单位
        unit3 = state.handle_manager.create_unit("hfoo", 1, 300.0, 400.0, 0.0)

        # 枚举玩家0的单位到组
        player = state.handle_manager.get_player(0)
        enum_units.execute(state, group, player, None)

        result = get_size.execute(state, group)
        assert result == 2

    def test_enum_units_of_player_with_filter(self):
        """测试按玩家枚举单位并应用过滤器。"""
        state = StateContext()
        create_group = CreateGroup()
        enum_units = GroupEnumUnitsOfPlayer()
        get_size = BlzGroupGetSize()

        group = create_group.execute(state)
        # 创建不同类型的单位
        unit1 = state.handle_manager.create_unit("hfoo", 0, 100.0, 200.0, 0.0)  # 步兵
        unit2 = state.handle_manager.create_unit("hkni", 0, 150.0, 250.0, 0.0)  # 骑士

        # 只枚举步兵类型的单位
        player = state.handle_manager.get_player(0)
        filter_func = lambda u: u.unit_type == "hfoo"
        enum_units.execute(state, group, player, filter_func)

        result = get_size.execute(state, group)
        assert result == 1
```

**Step 2: 运行测试验证失败**

```bash
pytest tests/natives/test_group_enum_natives.py::TestGroupEnumUnitsOfPlayer -v
```

Expected: FAIL（GroupEnumUnitsOfPlayer不存在）

**Step 3: 实现GroupEnumUnitsOfPlayer**

在 `src/jass_runner/natives/group_natives.py` 中添加：

```python
from .handle import Player  # 添加Player导入


class GroupEnumUnitsOfPlayer(NativeFunction):
    """枚举指定玩家的所有单位并添加到组。

    对应JASS native函数: void GroupEnumUnitsOfPlayer(group whichGroup, player whichPlayer, boolexpr filter)

    注意: 在真实JASS中，filter是boolexpr类型（条件表达式）。
    这里我们使用Python的Callable来模拟。
    """

    @property
    def name(self) -> str:
        """获取函数名称。"""
        return "GroupEnumUnitsOfPlayer"

    def execute(self, state_context, group: Group, player: Player,
                filter_func: Optional[Callable[['Unit'], bool]] = None):
        """执行GroupEnumUnitsOfPlayer native函数。

        参数：
            state_context: 状态上下文
            group: 目标单位组
            player: 要枚举的玩家
            filter_func: 可选的过滤函数，接收unit参数返回bool
        """
        if group is None:
            logger.warning("[GroupEnumUnitsOfPlayer] 组为None")
            return

        if player is None:
            logger.warning("[GroupEnumUnitsOfPlayer] 玩家为None")
            return

        handle_manager = state_context.handle_manager

        # 先清空组
        group.clear()

        # 获取该玩家的所有单位
        unit_ids = handle_manager.enum_units_of_player(player.player_id)

        added_count = 0
        for unit_id in unit_ids:
            unit = handle_manager.get_unit(unit_id)
            if unit and unit.is_alive():
                # 应用过滤器（如果有）
                if filter_func is None or filter_func(unit):
                    group.add_unit(unit)
                    added_count += 1

        logger.debug(f"[GroupEnumUnitsOfPlayer] 玩家{player.player_id}的{added_count}个单位添加到组{group.id}")
```

**Step 4: 注册到NativeFactory**

在 `src/jass_runner/natives/factory.py` 中：

1. 更新group_natives导入，添加GroupEnumUnitsOfPlayer

2. 添加注册：
```python
registry.register(GroupEnumUnitsOfPlayer())
```

**Step 5: 运行测试验证通过**

```bash
pytest tests/natives/test_group_enum_natives.py::TestGroupEnumUnitsOfPlayer -v
```

Expected: PASS

**Step 6: 提交**

```bash
git add src/jass_runner/natives/group_natives.py src/jass_runner/natives/factory.py tests/natives/test_group_enum_natives.py
git commit -m "feat(natives): add GroupEnumUnitsOfPlayer native function"
```

---

## Task 5: 实现GroupEnumUnitsInRange和GroupEnumUnitsInRangeOfLoc

**Files:**
- Modify: `src/jass_runner/natives/group_natives.py`
- Modify: `src/jass_runner/natives/factory.py`
- Test: `tests/natives/test_group_enum_natives.py`

**Step 1: 编写失败测试**

在 `tests/natives/test_group_enum_natives.py` 中添加：

```python
from jass_runner.natives.location import LocationConstructor


class TestGroupEnumUnitsInRange:
    """测试GroupEnumUnitsInRange native函数。"""

    def test_enum_units_in_range(self):
        """测试在范围内枚举单位。"""
        state = StateContext()
        create_group = CreateGroup()
        enum_units = GroupEnumUnitsInRange()
        get_size = BlzGroupGetSize()

        group = create_group.execute(state)
        # 在范围内创建单位
        unit1 = state.handle_manager.create_unit("hfoo", 0, 100.0, 200.0, 0.0)  # 距离0
        unit2 = state.handle_manager.create_unit("hfoo", 0, 150.0, 200.0, 0.0)  # 距离50
        # 在范围外创建单位
        unit3 = state.handle_manager.create_unit("hfoo", 0, 300.0, 200.0, 0.0)  # 距离200

        # 枚举中心(100, 200)半径100范围内的单位
        enum_units.execute(state, group, 100.0, 200.0, 100.0, None)

        result = get_size.execute(state, group)
        assert result == 2


class TestGroupEnumUnitsInRangeOfLoc:
    """测试GroupEnumUnitsInRangeOfLoc native函数。"""

    def test_enum_units_in_range_of_loc(self):
        """测试在Location范围内枚举单位。"""
        state = StateContext()
        create_group = CreateGroup()
        create_loc = LocationConstructor()
        enum_units = GroupEnumUnitsInRangeOfLoc()
        get_size = BlzGroupGetSize()

        group = create_group.execute(state)
        # 创建Location
        loc = create_loc.execute(state, 100.0, 200.0)
        # 在范围内创建单位
        unit1 = state.handle_manager.create_unit("hfoo", 0, 100.0, 200.0, 0.0)
        unit2 = state.handle_manager.create_unit("hfoo", 0, 150.0, 200.0, 0.0)

        # 枚举Location半径100范围内的单位
        enum_units.execute(state, group, loc, 100.0, None)

        result = get_size.execute(state, group)
        assert result == 2
```

**Step 2: 运行测试验证失败**

```bash
pytest tests/natives/test_group_enum_natives.py::TestGroupEnumUnitsInRange -v
```

Expected: FAIL（GroupEnumUnitsInRange不存在）

**Step 3: 实现两个Native函数**

在 `src/jass_runner/natives/group_natives.py` 中添加：

```python
from .location import Location  # 添加Location导入


class GroupEnumUnitsInRange(NativeFunction):
    """枚举指定范围内的所有单位并添加到组。

    对应JASS native函数: void GroupEnumUnitsInRange(group whichGroup, real x, real y, real radius, boolexpr filter)
    """

    @property
    def name(self) -> str:
        """获取函数名称。"""
        return "GroupEnumUnitsInRange"

    def execute(self, state_context, group: Group, x: float, y: float,
                radius: float, filter_func: Optional[Callable[['Unit'], bool]] = None):
        """执行GroupEnumUnitsInRange native函数。

        参数：
            state_context: 状态上下文
            group: 目标单位组
            x: 中心X坐标
            y: 中心Y坐标
            radius: 半径
            filter_func: 可选的过滤函数
        """
        if group is None:
            logger.warning("[GroupEnumUnitsInRange] 组为None")
            return

        if radius < 0:
            logger.warning("[GroupEnumUnitsInRange] 半径不能为负数")
            return

        handle_manager = state_context.handle_manager

        # 先清空组
        group.clear()

        # 获取范围内的所有单位
        unit_ids = handle_manager.enum_units_in_range(x, y, radius)

        added_count = 0
        for unit_id in unit_ids:
            unit = handle_manager.get_unit(unit_id)
            if unit and unit.is_alive():
                # 应用过滤器（如果有）
                if filter_func is None or filter_func(unit):
                    group.add_unit(unit)
                    added_count += 1

        logger.debug(f"[GroupEnumUnitsInRange] 范围({x}, {y})半径{radius}内的{added_count}个单位添加到组{group.id}")


class GroupEnumUnitsInRangeOfLoc(NativeFunction):
    """枚举Location范围内的所有单位并添加到组。

    对应JASS native函数: void GroupEnumUnitsInRangeOfLoc(group whichGroup, location whichLocation, real radius, boolexpr filter)
    """

    @property
    def name(self) -> str:
        """获取函数名称。"""
        return "GroupEnumUnitsInRangeOfLoc"

    def execute(self, state_context, group: Group, location: 'Location',
                radius: float, filter_func: Optional[Callable[['Unit'], bool]] = None):
        """执行GroupEnumUnitsInRangeOfLoc native函数。

        参数：
            state_context: 状态上下文
            group: 目标单位组
            location: 中心位置
            radius: 半径
            filter_func: 可选的过滤函数
        """
        if group is None:
            logger.warning("[GroupEnumUnitsInRangeOfLoc] 组为None")
            return

        if location is None:
            logger.warning("[GroupEnumUnitsInRangeOfLoc] Location为None")
            return

        # 调用GroupEnumUnitsInRange，传入Location的坐标
        enum_in_range = GroupEnumUnitsInRange()
        enum_in_range.execute(state_context, group, location.x, location.y, radius, filter_func)
```

**Step 4: 注册到NativeFactory**

在 `src/jass_runner/natives/factory.py` 中：

1. 更新group_natives导入

2. 添加注册：
```python
registry.register(GroupEnumUnitsInRange())
registry.register(GroupEnumUnitsInRangeOfLoc())
```

**Step 5: 运行测试验证通过**

```bash
pytest tests/natives/test_group_enum_natives.py -v
```

Expected: PASS

**Step 6: 提交**

```bash
git add src/jass_runner/natives/group_natives.py src/jass_runner/natives/factory.py tests/natives/test_group_enum_natives.py
git commit -m "feat(natives): add GroupEnumUnitsInRange and GroupEnumUnitsInRangeOfLoc native functions"
```

---

## Task 6: 实现GroupEnumUnitsInRect

**Files:**
- Modify: `src/jass_runner/natives/group_natives.py`
- Modify: `src/jass_runner/natives/factory.py`
- Test: `tests/natives/test_group_enum_natives.py`

**Step 1: 编写失败测试**

在 `tests/natives/test_group_enum_natives.py` 中添加：

```python
class TestGroupEnumUnitsInRect:
    """测试GroupEnumUnitsInRect native函数。"""

    def test_enum_units_in_rect(self):
        """测试在矩形区域内枚举单位。"""
        state = StateContext()
        create_group = CreateGroup()
        enum_units = GroupEnumUnitsInRect()
        get_size = BlzGroupGetSize()

        group = create_group.execute(state)
        # 在矩形内创建单位
        unit1 = state.handle_manager.create_unit("hfoo", 0, 100.0, 100.0, 0.0)
        unit2 = state.handle_manager.create_unit("hfoo", 0, 200.0, 200.0, 0.0)
        # 在矩形外创建单位
        unit3 = state.handle_manager.create_unit("hfoo", 0, 400.0, 400.0, 0.0)

        # 创建矩形 (minX=50, minY=50, maxX=250, maxY=250)
        from jass_runner.natives.handle import Rect
        rect = Rect("rect_1", 50.0, 50.0, 250.0, 250.0)

        # 枚举矩形内的单位
        enum_units.execute(state, group, rect, None)

        result = get_size.execute(state, group)
        assert result == 2
```

**Step 2: 运行测试验证失败**

```bash
pytest tests/natives/test_group_enum_natives.py::TestGroupEnumUnitsInRect -v
```

Expected: FAIL（Rect类或GroupEnumUnitsInRect不存在）

**Step 3: 先在handle.py中添加Rect类**

在 `src/jass_runner/natives/handle.py` 中添加Rect类（在Group类之后）：

```python
class Rect(Handle):
    """矩形区域handle。

    属性：
        min_x: 最小X坐标（左边界）
        min_y: 最小Y坐标（下边界）
        max_x: 最大X坐标（右边界）
        max_y: 最大Y坐标（上边界）
    """

    def __init__(self, rect_id: str, min_x: float, min_y: float,
                 max_x: float, max_y: float):
        """初始化矩形区域。

        参数：
            rect_id: 矩形ID
            min_x: 最小X坐标
            min_y: 最小Y坐标
            max_x: 最大X坐标
            max_y: 最大Y坐标
        """
        super().__init__(rect_id, "rect")
        self.min_x = min_x
        self.min_y = min_y
        self.max_x = max_x
        self.max_y = max_y

    def contains(self, x: float, y: float) -> bool:
        """检查点是否在矩形内。

        参数：
            x: X坐标
            y: Y坐标

        返回：
            点在矩形内返回True
        """
        return (self.min_x <= x <= self.max_x and
                self.min_y <= y <= self.max_y)
```

**Step 4: 在HandleManager中添加Rect支持**

在 `src/jass_runner/natives/manager.py` 中：

1. 从handle导入Rect

2. 添加方法：
```python
def create_rect(self, min_x: float, min_y: float, max_x: float, max_y: float) -> 'Rect':
    """创建一个新的矩形区域。"""
    handle_id = f"rect_{self._generate_id()}"
    from .handle import Rect
    rect = Rect(handle_id, min_x, min_y, max_x, max_y)
    self._register_handle(rect)
    return rect

def get_rect(self, rect_id: str) -> Optional['Rect']:
    """获取矩形区域对象，进行类型检查。"""
    handle = self.get_handle(rect_id)
    if isinstance(handle, Rect):
        return handle
    return None

def enum_units_in_rect(self, rect: 'Rect') -> List[str]:
    """枚举矩形区域内的所有单位。

    参数：
        rect: 矩形区域

    返回：
        单位ID列表
    """
    result = []
    type_name = "unit"

    if type_name not in self._type_index:
        return result

    for handle_id in self._type_index[type_name]:
        handle = self._handles.get(handle_id)
        if handle and handle.is_alive() and isinstance(handle, Unit):
            if rect.contains(handle.x, handle.y):
                result.append(handle_id)

    return result
```

**Step 5: 实现GroupEnumUnitsInRect**

在 `src/jass_runner/natives/group_natives.py` 中添加：

```python
from .handle import Rect  # 添加Rect导入


class GroupEnumUnitsInRect(NativeFunction):
    """枚举矩形区域内的所有单位并添加到组。

    对应JASS native函数: void GroupEnumUnitsInRect(group whichGroup, rect r, boolexpr filter)
    """

    @property
    def name(self) -> str:
        """获取函数名称。"""
        return "GroupEnumUnitsInRect"

    def execute(self, state_context, group: Group, rect: Rect,
                filter_func: Optional[Callable[['Unit'], bool]] = None):
        """执行GroupEnumUnitsInRect native函数。

        参数：
            state_context: 状态上下文
            group: 目标单位组
            rect: 矩形区域
            filter_func: 可选的过滤函数
        """
        if group is None:
            logger.warning("[GroupEnumUnitsInRect] 组为None")
            return

        if rect is None:
            logger.warning("[GroupEnumUnitsInRect] 矩形为None")
            return

        handle_manager = state_context.handle_manager

        # 先清空组
        group.clear()

        # 获取矩形内的所有单位
        unit_ids = handle_manager.enum_units_in_rect(rect)

        added_count = 0
        for unit_id in unit_ids:
            unit = handle_manager.get_unit(unit_id)
            if unit and unit.is_alive():
                # 应用过滤器（如果有）
                if filter_func is None or filter_func(unit):
                    group.add_unit(unit)
                    added_count += 1

        logger.debug(f"[GroupEnumUnitsInRect] 矩形区域内的{added_count}个单位添加到组{group.id}")
```

**Step 6: 注册到NativeFactory**

在 `src/jass_runner/natives/factory.py` 中：

1. 更新group_natives导入

2. 添加注册：
```python
registry.register(GroupEnumUnitsInRect())
```

**Step 7: 运行测试验证通过**

```bash
pytest tests/natives/test_group_enum_natives.py::TestGroupEnumUnitsInRect -v
```

Expected: PASS

**Step 8: 提交**

```bash
git add src/jass_runner/natives/handle.py src/jass_runner/natives/manager.py src/jass_runner/natives/group_natives.py src/jass_runner/natives/factory.py tests/natives/test_group_enum_natives.py
git commit -m "feat(natives): add GroupEnumUnitsInRect native function and Rect support"
```

---

## Task 7: 添加集成测试和更新工厂测试计数

**Files:**
- Create: `tests/integration/test_group_enum_integration.py`
- Modify: `tests/natives/test_factory.py`

**Step 1: 编写集成测试**

创建 `tests/integration/test_group_enum_integration.py`：

```python
"""单位组枚举Native函数集成测试。"""

from jass_runner.vm.jass_vm import JassVM


class TestGroupEnumIntegration:
    """测试单位组枚举native函数完整工作流。"""

    def test_group_enum_units_of_player_workflow(self):
        """测试按玩家枚举单位工作流。"""
        code = '''
        function main takes nothing returns nothing
            local group g
            local player p

            // 创建单位组
            set g = CreateGroup()
            set p = Player(0)

            // 创建一些单位
            call CreateUnit(p, 1213484355, 100.0, 200.0, 0.0)
            call CreateUnit(p, 1213484355, 150.0, 250.0, 0.0)

            // 枚举玩家0的单位到组
            call GroupEnumUnitsOfPlayer(g, p, null)

            // 验证组大小
            // (实际JASS中会用条件判断，这里仅测试native函数调用)

            // 清理
            call DestroyGroup(g)
        endfunction
        '''

        vm = JassVM()
        vm.load_script(code)
        vm.execute()

    def test_group_enum_units_in_range_workflow(self):
        """测试范围内枚举单位工作流。"""
        code = '''
        function main takes nothing returns nothing
            local group g

            // 创建单位组
            set g = CreateGroup()

            // 创建一些单位
            call CreateUnit(Player(0), 1213484355, 100.0, 200.0, 0.0)
            call CreateUnit(Player(0), 1213484355, 150.0, 200.0, 0.0)

            // 枚举范围内的单位
            call GroupEnumUnitsInRange(g, 100.0, 200.0, 100.0, null)

            // 清理
            call DestroyGroup(g)
        endfunction
        '''

        vm = JassVM()
        vm.load_script(code)
        vm.execute()
```

**Step 2: 更新工厂测试计数**

修改 `tests/natives/test_factory.py`：

找到测试计数行：
```python
# 检查基础函数数量（7个基础 + 19个触发器 + 15个数学 + 2个异步 + 14个单位操作 + 8个单位组 + 7个技能 = 72）
all_funcs = registry.get_all()
assert len(all_funcs) == 72
```

修改为：
```python
# 检查基础函数数量（7个基础 + 19个触发器 + 15个数学 + 2个异步 + 14个单位操作 + 8个单位组 + 7个技能 + 6个单位组枚举 = 78）
all_funcs = registry.get_all()
assert len(all_funcs) == 78
```

**Step 3: 运行所有相关测试**

```bash
pytest tests/natives/test_group_enum.py tests/natives/test_manager_enum.py tests/natives/test_group_blz.py tests/natives/test_group_enum_natives.py tests/integration/test_group_enum_integration.py tests/natives/test_factory.py -v
```

Expected: PASS

**Step 4: 提交**

```bash
git add tests/integration/test_group_enum_integration.py tests/natives/test_factory.py
git commit -m "test: add group enum integration tests and update factory test count"
```

---

## Task 8: 运行完整测试套件和更新文档

**Files:**
- 所有测试文件
- PROJECT_NOTES.md
- TODO.md

**Step 1: 运行完整测试套件**

```bash
pytest tests/ -v
```

Expected: 所有测试通过（572+ 测试）

**Step 2: 更新PROJECT_NOTES.md**

在文件末尾添加：

```markdown
#### 47. 单位组枚举Native函数实现完成 (2026-03-02)
- **新增组件**:
  - `Rect` 类 - 矩形区域支持
  - 单位组枚举函数 - 6个函数
- **新增Native函数**:
  - 组大小查询: BlzGroupGetSize, BlzGroupUnitAt
  - 按玩家枚举: GroupEnumUnitsOfPlayer
  - 按范围枚举: GroupEnumUnitsInRange, GroupEnumUnitsInRangeOfLoc
  - 按区域枚举: GroupEnumUnitsInRect
- **修改文件**:
  - `src/jass_runner/natives/handle.py` - 添加Rect类和Group枚举支持
  - `src/jass_runner/natives/manager.py` - 添加单位枚举方法
  - `src/jass_runner/natives/group_natives.py` - 添加6个枚举函数
  - `src/jass_runner/natives/factory.py` - 注册新函数
- **测试覆盖**:
  - 单元测试: Rect类、枚举方法、6个native函数
  - 集成测试: 完整枚举工作流
- **测试统计**: 所有测试通过
```

**Step 3: 更新TODO.md**

找到第三批任务：
```markdown
  - [ ] 第三批：单位组枚举（GroupEnumUnitsOfPlayer, GroupEnumUnitsInRange, GroupEnumUnitsInRangeOfLoc, GroupEnumUnitsInRect, BlzGroupGetSize, BlzGroupUnitAt）
```

改为：
```markdown
  - [x] 第三批：单位组枚举（GroupEnumUnitsOfPlayer, GroupEnumUnitsInRange, GroupEnumUnitsInRangeOfLoc, GroupEnumUnitsInRect, BlzGroupGetSize, BlzGroupUnitAt）✅ 已完成
```

**Step 4: 提交**

```bash
git add PROJECT_NOTES.md TODO.md
git commit -m "docs: update project notes for group enum natives implementation"
```

---

## 实施完成检查清单

- [ ] Task 1: 在Group类中添加枚举支持
- [ ] Task 2: 在HandleManager中添加单位枚举支持
- [ ] Task 3: 实现BlzGroupGetSize和BlzGroupUnitAt
- [ ] Task 4: 实现GroupEnumUnitsOfPlayer
- [ ] Task 5: 实现GroupEnumUnitsInRange和GroupEnumUnitsInRangeOfLoc
- [ ] Task 6: 实现GroupEnumUnitsInRect
- [ ] Task 7: 添加集成测试和更新工厂测试计数
- [ ] Task 8: 运行完整测试套件和更新文档

---

## 注意事项

1. **Rect类**: 新增Rect handle类型，用于表示矩形区域
2. **过滤器支持**: 枚举函数支持可选的filter参数（Python Callable）
3. **性能考虑**: 范围查询使用距离平方比较避免开方运算
4. **向后兼容**: 不影响现有功能，所有现有测试应继续通过
