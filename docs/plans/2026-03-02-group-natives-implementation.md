# 单位组Native函数实现计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 实现第一批单位组核心Native函数（CreateGroup, DestroyGroup, GroupAddUnit, GroupRemoveUnit, GroupClear, FirstOfGroup, IsUnitInGroup, ForGroup）

**Architecture:** 创建Group类管理单位集合，实现单位组生命周期管理和基本操作。Group作为Handle的子类，由HandleManager统一管理。

**Tech Stack:** Python 3.8+, pytest, 现有Native函数框架

---

## 前置信息

### 相关设计文档
- `resources/common.j` - Native函数定义参考
- `docs/plans/2026-03-02-parser-nested-calls-design.md` - 解析器设计文档

### 关键现有文件
- `src/jass_runner/natives/handle.py` - Handle基类和Unit类定义
- `src/jass_runner/natives/manager.py` - HandleManager类
- `src/jass_runner/natives/base.py` - NativeFunction基类
- `src/jass_runner/natives/factory.py` - Native函数注册工厂
- `src/jass_runner/natives/basic.py` - 基础Native函数实现示例

### Group数据结构
```python
class Group(Handle):
    """单位组，包含一组单位的引用。"""
    def __init__(self, group_id: str):
        super().__init__(group_id, "group")
        self._units: Set[str] = set()  # 存储单位ID集合
```

---

## Task 1: 创建Group类和HandleManager支持

**Files:**
- Modify: `src/jass_runner/natives/handle.py`
- Modify: `src/jass_runner/natives/manager.py`
- Test: `tests/natives/test_handle.py`（新建或修改）

**Step 1: 编写失败测试**

创建 `tests/natives/test_group_handle.py`：

```python
"""单位组Handle测试。"""

import pytest
from jass_runner.natives.handle import Group, Unit
from jass_runner.natives.manager import HandleManager


class TestGroupHandle:
    """测试Group类功能。"""

    def test_create_group(self):
        """测试创建Group对象。"""
        group = Group("group_1")
        assert group.id == "group_1"
        assert group.type_name == "group"
        assert len(group.get_units()) == 0

    def test_add_unit_to_group(self):
        """测试添加单位到组。"""
        group = Group("group_1")
        unit = Unit("unit_1", "hfoo", 0, 100.0, 200.0, 0.0)

        result = group.add_unit(unit)

        assert result is True
        assert len(group.get_units()) == 1
        assert unit.id in group.get_units()

    def test_remove_unit_from_group(self):
        """测试从组移除单位。"""
        group = Group("group_1")
        unit = Unit("unit_1", "hfoo", 0, 100.0, 200.0, 0.0)
        group.add_unit(unit)

        result = group.remove_unit(unit)

        assert result is True
        assert len(group.get_units()) == 0

    def test_clear_group(self):
        """测试清空单位组。"""
        group = Group("group_1")
        unit1 = Unit("unit_1", "hfoo", 0, 100.0, 200.0, 0.0)
        unit2 = Unit("unit_2", "hfoo", 0, 150.0, 250.0, 0.0)
        group.add_unit(unit1)
        group.add_unit(unit2)

        group.clear()

        assert len(group.get_units()) == 0

    def test_first_of_group(self):
        """测试获取组内第一个单位。"""
        group = Group("group_1")
        unit = Unit("unit_1", "hfoo", 0, 100.0, 200.0, 0.0)
        group.add_unit(unit)

        first = group.first()

        assert first == unit.id

    def test_is_unit_in_group(self):
        """测试检查单位是否在组内。"""
        group = Group("group_1")
        unit = Unit("unit_1", "hfoo", 0, 100.0, 200.0, 0.0)
        group.add_unit(unit)

        assert group.contains(unit) is True

        other_unit = Unit("unit_2", "hfoo", 0, 150.0, 250.0, 0.0)
        assert group.contains(other_unit) is False
```

**Step 2: 运行测试验证失败**

```bash
pytest tests/natives/test_group_handle.py -v
```

Expected: FAIL（Group类不存在）

**Step 3: 实现Group类**

在 `src/jass_runner/natives/handle.py` 中添加Group类：

```python
class Group(Handle):
    """单位组，包含一组单位的引用。

    用于管理一组相关单位，支持添加、移除、遍历等操作。
    """

    def __init__(self, group_id: str):
        """初始化单位组。

        参数：
            group_id: 组的唯一标识符
        """
        super().__init__(group_id, "group")
        self._units: Set[str] = set()  # 存储单位ID集合

    def add_unit(self, unit: 'Unit') -> bool:
        """添加单位到组。

        参数：
            unit: 要添加的单位

        返回：
            如果添加成功返回True，单位已在组中返回False
        """
        if not unit or not unit.is_alive():
            return False
        if unit.id in self._units:
            return False
        self._units.add(unit.id)
        return True

    def remove_unit(self, unit: 'Unit') -> bool:
        """从组中移除单位。

        参数：
            unit: 要移除的单位

        返回：
            如果移除成功返回True，单位不在组中返回False
        """
        if not unit:
            return False
        if unit.id not in self._units:
            return False
        self._units.remove(unit.id)
        return True

    def clear(self):
        """清空单位组，移除所有单位。"""
        self._units.clear()

    def first(self) -> Optional[str]:
        """获取组内第一个单位的ID。

        返回：
            第一个单位的ID，如果组为空返回None
        """
        if not self._units:
            return None
        return next(iter(self._units))

    def contains(self, unit: 'Unit') -> bool:
        """检查单位是否在组内。

        参数：
            unit: 要检查的单位

        返回：
            如果单位在组中返回True，否则返回False
        """
        if not unit:
            return False
        return unit.id in self._units

    def get_units(self) -> Set[str]:
        """获取组内所有单位的ID集合。

        返回：
            单位ID的集合副本
        """
        return self._units.copy()

    def size(self) -> int:
        """获取组内单位数量。

        返回：
            单位数量
        """
        return len(self._units)
```

**Step 4: 在HandleManager中添加Group支持**

在 `src/jass_runner/natives/manager.py` 中添加：

```python
from .handle import Handle, Unit, Player, Item, Group  # 添加Group导入

# 在HandleManager类中添加以下方法：

def create_group(self) -> Group:
    """创建一个新的单位组。"""
    handle_id = f"group_{self._generate_id()}"
    group = Group(handle_id)
    self._register_handle(group)
    return group

def get_group(self, group_id: str) -> Optional[Group]:
    """获取单位组对象，进行类型检查。"""
    handle = self.get_handle(group_id)
    if isinstance(handle, Group):
        return handle
    return None
```

**Step 5: 运行测试验证通过**

```bash
pytest tests/natives/test_group_handle.py -v
```

Expected: PASS

**Step 6: 提交**

```bash
git add src/jass_runner/natives/handle.py src/jass_runner/natives/manager.py tests/natives/test_group_handle.py
git commit -m "feat(handle): add Group class and HandleManager support"
```

---

## Task 2: 实现CreateGroup和DestroyGroup

**Files:**
- Create: `src/jass_runner/natives/group_natives.py`
- Modify: `src/jass_runner/natives/factory.py`
- Test: `tests/natives/test_group_natives.py`

**Step 1: 编写失败测试**

创建 `tests/natives/test_group_natives.py`：

```python
"""单位组Native函数测试。"""

import pytest
from jass_runner.natives.state import StateContext
from jass_runner.natives.group_natives import CreateGroup, DestroyGroup


class TestCreateGroup:
    """测试CreateGroup native函数。"""

    def test_create_group_returns_group(self):
        """测试CreateGroup返回group handle。"""
        state = StateContext()
        create_group = CreateGroup()

        result = create_group.execute(state)

        assert result is not None
        assert result.type_name == "group"
        # 验证组已注册到HandleManager
        group_from_manager = state.handle_manager.get_group(result.id)
        assert group_from_manager is not None
        assert group_from_manager.id == result.id


class TestDestroyGroup:
    """测试DestroyGroup native函数。"""

    def test_destroy_group_removes_group(self):
        """测试DestroyGroup销毁单位组。"""
        state = StateContext()
        create_group = CreateGroup()
        destroy_group = DestroyGroup()

        # 先创建组
        group = create_group.execute(state)
        group_id = group.id

        # 销毁组
        result = destroy_group.execute(state, group)

        assert result is True
        # 验证组已被销毁
        group_from_manager = state.handle_manager.get_group(group_id)
        assert group_from_manager is None

    def test_destroy_nonexistent_group_returns_false(self):
        """测试销毁不存在的组返回False。"""
        state = StateContext()
        destroy_group = DestroyGroup()

        # 创建一个组然后手动销毁
        from jass_runner.natives.handle import Group
        group = Group("group_test")
        group.destroy()

        result = destroy_group.execute(state, group)

        assert result is False
```

**Step 2: 运行测试验证失败**

```bash
pytest tests/natives/test_group_natives.py::TestCreateGroup -v
```

Expected: FAIL（group_natives.py不存在）

**Step 3: 实现CreateGroup和DestroyGroup**

创建 `src/jass_runner/natives/group_natives.py`：

```python
"""单位组Native函数实现。

此模块包含JASS单位组相关native函数的实现。
"""

import logging
from .base import NativeFunction
from .handle import Group

logger = logging.getLogger(__name__)


class CreateGroup(NativeFunction):
    """创建一个新的单位组。

    对应JASS native函数: group CreateGroup()
    """

    @property
    def name(self) -> str:
        """获取函数名称。"""
        return "CreateGroup"

    def execute(self, state_context) -> Group:
        """执行CreateGroup native函数。

        参数：
            state_context: 状态上下文

        返回：
            新创建的Group对象
        """
        handle_manager = state_context.handle_manager
        group = handle_manager.create_group()

        logger.info(f"[CreateGroup] 创建单位组，ID: {group.id}")
        return group


class DestroyGroup(NativeFunction):
    """销毁一个单位组。

    对应JASS native函数: void DestroyGroup(group whichGroup)

    注意: 销毁组不会销毁组内的单位，只是解散组。
    """

    @property
    def name(self) -> str:
        """获取函数名称。"""
        return "DestroyGroup"

    def execute(self, state_context, group: Group) -> bool:
        """执行DestroyGroup native函数。

        参数：
            state_context: 状态上下文
            group: 要销毁的单位组

        返回：
            成功销毁返回True，否则返回False
        """
        if group is None:
            logger.warning("[DestroyGroup] 尝试销毁None组")
            return False

        handle_manager = state_context.handle_manager
        success = handle_manager.destroy_handle(group.id)

        if success:
            logger.info(f"[DestroyGroup] 单位组{group.id}已销毁")
        else:
            logger.warning(f"[DestroyGroup] 单位组{group.id}不存在或已被销毁")

        return success
```

**Step 4: 注册到NativeFactory**

在 `src/jass_runner/natives/factory.py` 中添加：

```python
from .group_natives import CreateGroup, DestroyGroup

# 在create_default_registry方法中添加：
registry.register(CreateGroup())
registry.register(DestroyGroup())
```

**Step 5: 运行测试验证通过**

```bash
pytest tests/natives/test_group_natives.py -v
```

Expected: PASS

**Step 6: 提交**

```bash
git add src/jass_runner/natives/group_natives.py src/jass_runner/natives/factory.py tests/natives/test_group_natives.py
git commit -m "feat(natives): add CreateGroup and DestroyGroup native functions"
```

---

## Task 3: 实现GroupAddUnit, GroupRemoveUnit, GroupClear

**Files:**
- Modify: `src/jass_runner/natives/group_natives.py`
- Modify: `src/jass_runner/natives/factory.py`
- Test: `tests/natives/test_group_natives.py`

**Step 1: 编写失败测试**

在 `tests/natives/test_group_natives.py` 中添加：

```python
from jass_runner.natives.handle import Unit


class TestGroupAddUnit:
    """测试GroupAddUnit native函数。"""

    def test_add_unit_to_group(self):
        """测试添加单位到组。"""
        state = StateContext()
        from jass_runner.natives.group_natives import CreateGroup, GroupAddUnit

        create_group = CreateGroup()
        add_unit = GroupAddUnit()

        group = create_group.execute(state)
        unit = state.handle_manager.create_unit("hfoo", 0, 100.0, 200.0, 0.0)

        result = add_unit.execute(state, group, unit)

        assert result is True
        assert group.contains(unit) is True

    def test_add_same_unit_twice_returns_false(self):
        """测试重复添加同一单位返回False。"""
        state = StateContext()
        from jass_runner.natives.group_natives import CreateGroup, GroupAddUnit

        create_group = CreateGroup()
        add_unit = GroupAddUnit()

        group = create_group.execute(state)
        unit = state.handle_manager.create_unit("hfoo", 0, 100.0, 200.0, 0.0)

        add_unit.execute(state, group, unit)
        result = add_unit.execute(state, group, unit)

        assert result is False


class TestGroupRemoveUnit:
    """测试GroupRemoveUnit native函数。"""

    def test_remove_unit_from_group(self):
        """测试从组移除单位。"""
        state = StateContext()
        from jass_runner.natives.group_natives import CreateGroup, GroupAddUnit, GroupRemoveUnit

        create_group = CreateGroup()
        add_unit = GroupAddUnit()
        remove_unit = GroupRemoveUnit()

        group = create_group.execute(state)
        unit = state.handle_manager.create_unit("hfoo", 0, 100.0, 200.0, 0.0)
        add_unit.execute(state, group, unit)

        result = remove_unit.execute(state, group, unit)

        assert result is True
        assert group.contains(unit) is False


class TestGroupClear:
    """测试GroupClear native函数。"""

    def test_clear_group_removes_all_units(self):
        """测试清空组移除所有单位。"""
        state = StateContext()
        from jass_runner.natives.group_natives import CreateGroup, GroupAddUnit, GroupClear

        create_group = CreateGroup()
        add_unit = GroupAddUnit()
        clear_group = GroupClear()

        group = create_group.execute(state)
        unit1 = state.handle_manager.create_unit("hfoo", 0, 100.0, 200.0, 0.0)
        unit2 = state.handle_manager.create_unit("hfoo", 0, 150.0, 250.0, 0.0)
        add_unit.execute(state, group, unit1)
        add_unit.execute(state, group, unit2)

        result = clear_group.execute(state, group)

        assert result is True
        assert group.size() == 0
```

**Step 2: 运行测试验证失败**

```bash
pytest tests/natives/test_group_natives.py::TestGroupAddUnit -v
```

Expected: FAIL（GroupAddUnit不存在）

**Step 3: 实现GroupAddUnit, GroupRemoveUnit, GroupClear**

在 `src/jass_runner/natives/group_natives.py` 中添加：

```python
from .handle import Group, Unit  # 添加Unit导入


class GroupAddUnit(NativeFunction):
    """添加单位到单位组。

    对应JASS native函数: boolean GroupAddUnit(group whichGroup, unit whichUnit)
    """

    @property
    def name(self) -> str:
        """获取函数名称。"""
        return "GroupAddUnit"

    def execute(self, state_context, group: Group, unit: Unit) -> bool:
        """执行GroupAddUnit native函数。

        参数：
            state_context: 状态上下文
            group: 目标单位组
            unit: 要添加的单位

        返回：
            添加成功返回True，单位已在组中返回False
        """
        if group is None or unit is None:
            logger.warning("[GroupAddUnit] 组或单位为None")
            return False

        result = group.add_unit(unit)

        if result:
            logger.debug(f"[GroupAddUnit] 单位{unit.id}添加到组{group.id}")

        return result


class GroupRemoveUnit(NativeFunction):
    """从单位组移除单位。

    对应JASS native函数: boolean GroupRemoveUnit(group whichGroup, unit whichUnit)
    """

    @property
    def name(self) -> str:
        """获取函数名称。"""
        return "GroupRemoveUnit"

    def execute(self, state_context, group: Group, unit: Unit) -> bool:
        """执行GroupRemoveUnit native函数。

        参数：
            state_context: 状态上下文
            group: 目标单位组
            unit: 要移除的单位

        返回：
            移除成功返回True，单位不在组中返回False
        """
        if group is None or unit is None:
            logger.warning("[GroupRemoveUnit] 组或单位为None")
            return False

        result = group.remove_unit(unit)

        if result:
            logger.debug(f"[GroupRemoveUnit] 单位{unit.id}从组{group.id}移除")

        return result


class GroupClear(NativeFunction):
    """清空单位组，移除所有单位。

    对应JASS native函数: void GroupClear(group whichGroup)
    """

    @property
    def name(self) -> str:
        """获取函数名称。"""
        return "GroupClear"

    def execute(self, state_context, group: Group) -> bool:
        """执行GroupClear native函数。

        参数：
            state_context: 状态上下文
            group: 要清空的单位组

        返回：
            清空成功返回True
        """
        if group is None:
            logger.warning("[GroupClear] 组为None")
            return False

        group.clear()
        logger.debug(f"[GroupClear] 组{group.id}已清空")

        return True
```

**Step 4: 注册到NativeFactory**

在 `src/jass_runner/natives/factory.py` 中添加：

```python
from .group_natives import CreateGroup, DestroyGroup, GroupAddUnit, GroupRemoveUnit, GroupClear

# 在create_default_registry方法中添加：
registry.register(GroupAddUnit())
registry.register(GroupRemoveUnit())
registry.register(GroupClear())
```

**Step 5: 运行测试验证通过**

```bash
pytest tests/natives/test_group_natives.py -v
```

Expected: PASS

**Step 6: 提交**

```bash
git add src/jass_runner/natives/group_natives.py src/jass_runner/natives/factory.py tests/natives/test_group_natives.py
git commit -m "feat(natives): add GroupAddUnit, GroupRemoveUnit, GroupClear native functions"
```

---

## Task 4: 实现FirstOfGroup和IsUnitInGroup

**Files:**
- Modify: `src/jass_runner/natives/group_natives.py`
- Modify: `src/jass_runner/natives/factory.py`
- Test: `tests/natives/test_group_natives.py`

**Step 1: 编写失败测试**

在 `tests/natives/test_group_natives.py` 中添加：

```python
class TestFirstOfGroup:
    """测试FirstOfGroup native函数。"""

    def test_first_of_group_returns_unit(self):
        """测试FirstOfGroup返回组内第一个单位。"""
        state = StateContext()
        from jass_runner.natives.group_natives import CreateGroup, GroupAddUnit, FirstOfGroup

        create_group = CreateGroup()
        add_unit = GroupAddUnit()
        first_of_group = FirstOfGroup()

        group = create_group.execute(state)
        unit = state.handle_manager.create_unit("hfoo", 0, 100.0, 200.0, 0.0)
        add_unit.execute(state, group, unit)

        result = first_of_group.execute(state, group)

        assert result == unit

    def test_first_of_empty_group_returns_none(self):
        """测试空组返回None。"""
        state = StateContext()
        from jass_runner.natives.group_natives import CreateGroup, FirstOfGroup

        create_group = CreateGroup()
        first_of_group = FirstOfGroup()

        group = create_group.execute(state)

        result = first_of_group.execute(state, group)

        assert result is None


class TestIsUnitInGroup:
    """测试IsUnitInGroup native函数。"""

    def test_unit_in_group_returns_true(self):
        """测试单位在组内返回True。"""
        state = StateContext()
        from jass_runner.natives.group_natives import CreateGroup, GroupAddUnit, IsUnitInGroup

        create_group = CreateGroup()
        add_unit = GroupAddUnit()
        is_unit_in_group = IsUnitInGroup()

        group = create_group.execute(state)
        unit = state.handle_manager.create_unit("hfoo", 0, 100.0, 200.0, 0.0)
        add_unit.execute(state, group, unit)

        result = is_unit_in_group.execute(state, unit, group)

        assert result is True

    def test_unit_not_in_group_returns_false(self):
        """测试单位不在组内返回False。"""
        state = StateContext()
        from jass_runner.natives.group_natives import CreateGroup, IsUnitInGroup

        create_group = CreateGroup()
        is_unit_in_group = IsUnitInGroup()

        group = create_group.execute(state)
        unit = state.handle_manager.create_unit("hfoo", 0, 100.0, 200.0, 0.0)
        # 不添加到组

        result = is_unit_in_group.execute(state, unit, group)

        assert result is False
```

**Step 2: 运行测试验证失败**

```bash
pytest tests/natives/test_group_natives.py::TestFirstOfGroup -v
```

Expected: FAIL（FirstOfGroup不存在）

**Step 3: 实现FirstOfGroup和IsUnitInGroup**

在 `src/jass_runner/natives/group_natives.py` 中添加：

```python
class FirstOfGroup(NativeFunction):
    """获取单位组中的第一个单位。

    对应JASS native函数: unit FirstOfGroup(group whichGroup)

    注意: 由于Python的set是无序的，"第一个"是任意的。
    """

    @property
    def name(self) -> str:
        """获取函数名称。"""
        return "FirstOfGroup"

    def execute(self, state_context, group: Group) -> Optional[Unit]:
        """执行FirstOfGroup native函数。

        参数：
            state_context: 状态上下文
            group: 单位组

        返回：
            组内第一个单位，如果组为空返回None
        """
        if group is None:
            logger.warning("[FirstOfGroup] 组为None")
            return None

        first_unit_id = group.first()
        if first_unit_id is None:
            return None

        # 通过HandleManager获取单位对象
        handle_manager = state_context.handle_manager
        unit = handle_manager.get_unit(first_unit_id)

        return unit


class IsUnitInGroup(NativeFunction):
    """检查单位是否在单位组中。

    对应JASS native函数: boolean IsUnitInGroup(unit whichUnit, group whichGroup)
    """

    @property
    def name(self) -> str:
        """获取函数名称。"""
        return "IsUnitInGroup"

    def execute(self, state_context, unit: Unit, group: Group) -> bool:
        """执行IsUnitInGroup native函数。

        参数：
            state_context: 状态上下文
            unit: 要检查的单位
            group: 单位组

        返回：
            单位在组中返回True，否则返回False
        """
        if group is None or unit is None:
            return False

        return group.contains(unit)
```

**Step 4: 注册到NativeFactory**

在 `src/jass_runner/natives/factory.py` 中添加导入和注册：

```python
from .group_natives import (
    CreateGroup, DestroyGroup, GroupAddUnit, GroupRemoveUnit,
    GroupClear, FirstOfGroup, IsUnitInGroup
)

# 注册：
registry.register(FirstOfGroup())
registry.register(IsUnitInGroup())
```

**Step 5: 运行测试验证通过**

```bash
pytest tests/natives/test_group_natives.py -v
```

Expected: PASS

**Step 6: 提交**

```bash
git add src/jass_runner/natives/group_natives.py src/jass_runner/natives/factory.py tests/natives/test_group_natives.py
git commit -m "feat(natives): add FirstOfGroup and IsUnitInGroup native functions"
```

---

## Task 5: 实现ForGroup

**Files:**
- Modify: `src/jass_runner/natives/group_natives.py`
- Modify: `src/jass_runner/natives/factory.py`
- Test: `tests/natives/test_group_natives.py`

**Step 1: 编写失败测试**

在 `tests/natives/test_group_natives.py` 中添加：

```python
class TestForGroup:
    """测试ForGroup native函数。"""

    def test_for_group_calls_callback_for_each_unit(self):
        """测试ForGroup为每个单位调用回调。"""
        state = StateContext()
        from jass_runner.natives.group_natives import CreateGroup, GroupAddUnit, ForGroup

        create_group = CreateGroup()
        add_unit = GroupAddUnit()
        for_group = ForGroup()

        group = create_group.execute(state)
        unit1 = state.handle_manager.create_unit("hfoo", 0, 100.0, 200.0, 0.0)
        unit2 = state.handle_manager.create_unit("hfoo", 0, 150.0, 250.0, 0.0)
        add_unit.execute(state, group, unit1)
        add_unit.execute(state, group, unit2)

        # 记录被调用的单位
        called_units = []
        def callback(u):
            called_units.append(u)

        for_group.execute(state, group, callback)

        assert len(called_units) == 2
        assert unit1 in called_units
        assert unit2 in called_units

    def test_for_group_with_empty_group(self):
        """测试ForGroup处理空组。"""
        state = StateContext()
        from jass_runner.natives.group_natives import CreateGroup, ForGroup

        create_group = CreateGroup()
        for_group = ForGroup()

        group = create_group.execute(state)

        called = False
        def callback(u):
            nonlocal called
            called = True

        for_group.execute(state, group, callback)

        assert called is False
```

**Step 2: 运行测试验证失败**

```bash
pytest tests/natives/test_group_natives.py::TestForGroup -v
```

Expected: FAIL（ForGroup不存在）

**Step 3: 实现ForGroup**

在 `src/jass_runner/natives/group_natives.py` 中添加：

```python
from typing import Callable  # 添加导入


class ForGroup(NativeFunction):
    """遍历单位组中的每个单位并执行回调函数。

    对应JASS native函数: void ForGroup(group whichGroup, code callback)

    注意: 在真实JASS中，callback是code类型（函数引用）。
    这里我们使用Python的Callable来模拟。
    """

    @property
    def name(self) -> str:
        """获取函数名称。"""
        return "ForGroup"

    def execute(self, state_context, group: Group, callback: Callable[[Unit], None]):
        """执行ForGroup native函数。

        参数：
            state_context: 状态上下文
            group: 要遍历的单位组
            callback: 对每个单位执行的回调函数，接收unit参数
        """
        if group is None:
            logger.warning("[ForGroup] 组为None")
            return

        if callback is None:
            logger.warning("[ForGroup] 回调为None")
            return

        handle_manager = state_context.handle_manager
        unit_ids = group.get_units()

        for unit_id in unit_ids:
            unit = handle_manager.get_unit(unit_id)
            if unit and unit.is_alive():
                try:
                    callback(unit)
                except Exception as e:
                    logger.error(f"[ForGroup] 回调执行错误: {e}")

        logger.debug(f"[ForGroup] 遍历组{group.id}完成，处理了{len(unit_ids)}个单位")
```

**Step 4: 注册到NativeFactory**

在 `src/jass_runner/natives/factory.py` 中更新导入：

```python
from .group_natives import (
    CreateGroup, DestroyGroup, GroupAddUnit, GroupRemoveUnit,
    GroupClear, FirstOfGroup, IsUnitInGroup, ForGroup
)

# 注册：
registry.register(ForGroup())
```

**Step 5: 运行测试验证通过**

```bash
pytest tests/natives/test_group_natives.py -v
```

Expected: PASS

**Step 6: 提交**

```bash
git add src/jass_runner/natives/group_natives.py src/jass_runner/natives/factory.py tests/natives/test_group_natives.py
git commit -m "feat(natives): add ForGroup native function"
```

---

## Task 6: 添加集成测试和更新工厂测试计数

**Files:**
- Create: `tests/integration/test_group_natives.py`
- Modify: `tests/natives/test_factory.py`

**Step 1: 编写集成测试**

创建 `tests/integration/test_group_natives.py`：

```python
"""单位组Native函数集成测试。"""

from jass_runner.vm.jass_vm import JassVM


class TestGroupNativesIntegration:
    """测试单位组native函数完整工作流。"""

    def test_group_lifecycle_workflow(self):
        """测试单位组完整生命周期。"""
        code = '''
        function main takes nothing returns nothing
            local group g
            local unit u1
            local unit u2

            // 创建单位组
            set g = CreateGroup()

            // 创建单位
            set u1 = CreateUnit(Player(0), 1213484355, 100.0, 200.0, 0.0)
            set u2 = CreateUnit(Player(0), 1213484355, 150.0, 250.0, 0.0)

            // 添加单位到组
            call GroupAddUnit(g, u1)
            call GroupAddUnit(g, u2)

            // 验证单位在组中
            // (实际JASS中会用条件判断，这里仅测试native函数调用)

            // 清空组
            call GroupClear(g)

            // 销毁组
            call DestroyGroup(g)
        endfunction
        '''

        vm = JassVM()
        vm.load_script(code)
        vm.execute()

    def test_group_with_nested_calls(self):
        """测试嵌套调用创建单位和组操作。"""
        code = '''
        function main takes nothing returns nothing
            local group g
            local unit first

            // 创建组并添加单位（使用嵌套调用）
            set g = CreateGroup()
            call GroupAddUnit(g, CreateUnit(Player(0), 1213484355, 100.0, 200.0, 0.0))

            // 获取第一个单位
            set first = FirstOfGroup(g)

            // 清理
            call GroupClear(g)
            call DestroyGroup(g)
        endfunction
        '''

        vm = JassVM()
        vm.load_script(code)
        vm.execute()
```

**Step 2: 更新工厂测试计数**

修改 `tests/natives/test_factory.py` 中的测试计数：

找到测试 `test_create_default_registry` 中的断言：
```python
# 检查基础函数数量（原来是57个，现在增加8个单位组函数）
all_funcs = registry.get_all()
assert len(all_funcs) == 65  # 更新为65
```

**Step 3: 运行所有测试**

```bash
pytest tests/natives/test_group_natives.py tests/integration/test_group_natives.py tests/natives/test_factory.py -v
```

Expected: PASS

**Step 4: 提交**

```bash
git add tests/integration/test_group_natives.py tests/natives/test_factory.py
git commit -m "test: add group natives integration tests and update factory test count"
```

---

## Task 7: 运行完整测试套件

**Files:**
- 所有测试文件

**Step 1: 运行完整测试套件**

```bash
pytest tests/ -v
```

Expected: 所有测试通过（520+ 测试）

**Step 2: 提交（如有必要）**

如果有任何修复，提交更改。

---

## Task 8: 更新项目文档

**Files:**
- Modify: `PROJECT_NOTES.md`
- Modify: `TODO.md`

**Step 1: 添加完成记录到PROJECT_NOTES.md**

在末尾添加：

```markdown
#### 45. 单位组Native函数实现完成 (2026-03-02)
- **新增组件**:
  - `Group` 类 - 单位组管理（添加、移除、遍历）
  - `group_natives.py` - 8个单位组Native函数
- **新增Native函数**:
  - 生命周期: CreateGroup, DestroyGroup
  - 基本操作: GroupAddUnit, GroupRemoveUnit, GroupClear
  - 查询: FirstOfGroup, IsUnitInGroup
  - 遍历: ForGroup
- **修改文件**:
  - `src/jass_runner/natives/handle.py` - 添加Group类
  - `src/jass_runner/natives/manager.py` - 添加Group管理支持
  - `src/jass_runner/natives/group_natives.py` - 新建，实现8个函数
  - `src/jass_runner/natives/factory.py` - 注册新函数
- **测试覆盖**:
  - 单元测试: Group类、8个native函数
  - 集成测试: 完整单位组工作流
- **测试统计**: 所有测试通过
```

**Step 2: 更新TODO.md**

在Native API实现状态部分添加：
```markdown
- [x] **单位组操作**: CreateGroup, DestroyGroup, GroupAddUnit, GroupRemoveUnit, GroupClear, FirstOfGroup, IsUnitInGroup, ForGroup
```

**Step 3: 提交**

```bash
git add PROJECT_NOTES.md TODO.md
git commit -m "docs: update project notes for group natives implementation"
```

---

## 实施完成检查清单

- [ ] Task 1: 创建Group类和HandleManager支持
- [ ] Task 2: 实现CreateGroup和DestroyGroup
- [ ] Task 3: 实现GroupAddUnit, GroupRemoveUnit, GroupClear
- [ ] Task 4: 实现FirstOfGroup和IsUnitInGroup
- [ ] Task 5: 实现ForGroup
- [ ] Task 6: 添加集成测试和更新工厂测试计数
- [ ] Task 7: 运行完整测试套件
- [ ] Task 8: 更新项目文档

---

## 注意事项

1. **Group类设计**: Group继承自Handle，使用set存储单位ID，确保唯一性
2. **ForGroup实现**: 使用Python Callable模拟JASS的code类型回调
3. **错误处理**: 所有函数都检查None参数，记录警告日志
4. **测试覆盖**: 每个函数都有正面和负面测试用例
5. **向后兼容**: 不影响现有功能，所有现有测试应继续通过
