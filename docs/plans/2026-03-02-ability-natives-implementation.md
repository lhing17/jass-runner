# 技能系统Native函数实现计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 实现第二批技能系统核心Native函数（UnitAddAbility, UnitRemoveAbility, GetUnitAbilityLevel, SetUnitAbilityLevel, IncUnitAbilityLevel, DecUnitAbilityLevel, UnitMakeAbilityPermanent）

**Architecture:** 在Unit类中添加技能存储字典，使用技能ID（fourcc整数）作为键，技能等级作为值。创建ability_natives.py实现相关Native函数。

**Tech Stack:** Python 3.8+, pytest, 现有Native函数框架

---

## 前置信息

### 相关设计文档
- `resources/common.j` - Native函数定义参考
- `docs/plans/2026-03-02-group-natives-implementation.md` - 单位组实现参考

### 关键现有文件
- `src/jass_runner/natives/handle.py` - Handle基类和Unit类定义
- `src/jass_runner/natives/manager.py` - HandleManager类
- `src/jass_runner/natives/base.py` - NativeFunction基类
- `src/jass_runner/natives/factory.py` - Native函数注册工厂
- `src/jass_runner/natives/group_natives.py` - Native函数实现示例

### 技能数据结构
```python
# 在Unit类中添加：
self._abilities: Dict[int, int] = {}  # 技能ID -> 技能等级
```

---

## Task 1: 在Unit类中添加技能支持

**Files:**
- Modify: `src/jass_runner/natives/handle.py`
- Test: `tests/natives/test_unit_ability.py`（新建）

**Step 1: 编写失败测试**

创建 `tests/natives/test_unit_ability.py`：

```python
"""单位技能系统测试。"""

import pytest
from jass_runner.natives.handle import Unit


class TestUnitAbility:
    """测试Unit类技能功能。"""

    def test_add_ability_to_unit(self):
        """测试给单位添加技能。"""
        unit = Unit("unit_1", "hfoo", 0, 100.0, 200.0, 0.0)
        ability_id = 1097699445  # 'AHhb' - 圣光术

        result = unit.add_ability(ability_id)

        assert result is True
        assert unit.has_ability(ability_id) is True
        assert unit.get_ability_level(ability_id) == 1

    def test_add_duplicate_ability_fails(self):
        """测试重复添加技能失败。"""
        unit = Unit("unit_1", "hfoo", 0, 100.0, 200.0, 0.0)
        ability_id = 1097699445

        unit.add_ability(ability_id)
        result = unit.add_ability(ability_id)

        assert result is False

    def test_remove_ability_from_unit(self):
        """测试从单位移除技能。"""
        unit = Unit("unit_1", "hfoo", 0, 100.0, 200.0, 0.0)
        ability_id = 1097699445
        unit.add_ability(ability_id)

        result = unit.remove_ability(ability_id)

        assert result is True
        assert unit.has_ability(ability_id) is False

    def test_remove_nonexistent_ability_fails(self):
        """测试移除不存在的技能失败。"""
        unit = Unit("unit_1", "hfoo", 0, 100.0, 200.0, 0.0)
        ability_id = 1097699445

        result = unit.remove_ability(ability_id)

        assert result is False

    def test_set_ability_level(self):
        """测试设置技能等级。"""
        unit = Unit("unit_1", "hfoo", 0, 100.0, 200.0, 0.0)
        ability_id = 1097699445
        unit.add_ability(ability_id)

        result = unit.set_ability_level(ability_id, 3)

        assert result is True
        assert unit.get_ability_level(ability_id) == 3

    def test_increment_ability_level(self):
        """测试增加技能等级。"""
        unit = Unit("unit_1", "hfoo", 0, 100.0, 200.0, 0.0)
        ability_id = 1097699445
        unit.add_ability(ability_id)

        result = unit.inc_ability_level(ability_id)

        assert result is True
        assert unit.get_ability_level(ability_id) == 2

    def test_decrement_ability_level(self):
        """测试降低技能等级。"""
        unit = Unit("unit_1", "hfoo", 0, 100.0, 200.0, 0.0)
        ability_id = 1097699445
        unit.add_ability(ability_id)
        unit.set_ability_level(ability_id, 3)

        result = unit.dec_ability_level(ability_id)

        assert result is True
        assert unit.get_ability_level(ability_id) == 2

    def test_get_ability_level_nonexistent(self):
        """测试获取不存在技能的等级返回0。"""
        unit = Unit("unit_1", "hfoo", 0, 100.0, 200.0, 0.0)
        ability_id = 1097699445

        level = unit.get_ability_level(ability_id)

        assert level == 0
```

**Step 2: 运行测试验证失败**

```bash
pytest tests/natives/test_unit_ability.py -v
```

Expected: FAIL（Unit类没有技能相关方法）

**Step 3: 在Unit类中添加技能支持**

在 `src/jass_runner/natives/handle.py` 中：

1. 在文件顶部添加导入：
```python
from typing import Set, Optional, Dict  # 添加Dict
```

2. 在Unit类的`__init__`方法中添加（第60行之后）：
```python
self._abilities: Dict[int, int] = {}  # 技能ID -> 技能等级
```

3. 在Unit类末尾添加以下方法（在destroy方法之后）：

```python
def add_ability(self, ability_id: int) -> bool:
    """给单位添加技能。

    参数：
        ability_id: 技能ID（fourcc整数格式）

    返回：
        添加成功返回True，技能已存在返回False
    """
    if ability_id in self._abilities:
        return False
    self._abilities[ability_id] = 1  # 默认等级1
    return True

def remove_ability(self, ability_id: int) -> bool:
    """从单位移除技能。

    参数：
        ability_id: 技能ID

    返回：
        移除成功返回True，技能不存在返回False
    """
    if ability_id not in self._abilities:
        return False
    del self._abilities[ability_id]
    return True

def has_ability(self, ability_id: int) -> bool:
    """检查单位是否拥有指定技能。

    参数：
        ability_id: 技能ID

    返回：
        拥有技能返回True，否则返回False
    """
    return ability_id in self._abilities

def get_ability_level(self, ability_id: int) -> int:
    """获取技能等级。

    参数：
        ability_id: 技能ID

    返回：
        技能等级，技能不存在返回0
    """
    return self._abilities.get(ability_id, 0)

def set_ability_level(self, ability_id: int, level: int) -> bool:
    """设置技能等级。

    参数：
        ability_id: 技能ID
        level: 新等级（必须>0）

    返回：
        设置成功返回True，技能不存在或等级无效返回False
    """
    if ability_id not in self._abilities:
        return False
    if level <= 0:
        return False
    self._abilities[ability_id] = level
    return True

def inc_ability_level(self, ability_id: int) -> bool:
    """增加技能等级。

    参数：
        ability_id: 技能ID

    返回：
        增加成功返回True，技能不存在返回False
    """
    if ability_id not in self._abilities:
        return False
    self._abilities[ability_id] += 1
    return True

def dec_ability_level(self, ability_id: int) -> bool:
    """降低技能等级。

    参数：
        ability_id: 技能ID

    返回：
        降低成功返回True，技能不存在或等级已为1返回False
    """
    if ability_id not in self._abilities:
        return False
    if self._abilities[ability_id] <= 1:
        return False
    self._abilities[ability_id] -= 1
    return True
```

**Step 4: 运行测试验证通过**

```bash
pytest tests/natives/test_unit_ability.py -v
```

Expected: PASS

**Step 5: 提交**

```bash
git add src/jass_runner/natives/handle.py tests/natives/test_unit_ability.py
git commit -m "feat(handle): add ability support to Unit class"
```

---

## Task 2: 实现UnitAddAbility和UnitRemoveAbility

**Files:**
- Create: `src/jass_runner/natives/ability_natives.py`
- Modify: `src/jass_runner/natives/factory.py`
- Test: `tests/natives/test_ability_natives.py`

**Step 1: 编写失败测试**

创建 `tests/natives/test_ability_natives.py`：

```python
"""技能Native函数测试。"""

import pytest
from jass_runner.natives.state import StateContext
from jass_runner.natives.ability_natives import UnitAddAbility, UnitRemoveAbility


class TestUnitAddAbility:
    """测试UnitAddAbility native函数。"""

    def test_add_ability_to_unit(self):
        """测试给单位添加技能。"""
        state = StateContext()
        add_ability = UnitAddAbility()
        unit = state.handle_manager.create_unit("hfoo", 0, 100.0, 200.0, 0.0)
        ability_id = 1097699445  # 'AHhb'

        result = add_ability.execute(state, unit, ability_id)

        assert result is True
        assert unit.has_ability(ability_id) is True

    def test_add_ability_to_none_unit_returns_false(self):
        """测试给None单位添加技能返回False。"""
        state = StateContext()
        add_ability = UnitAddAbility()

        result = add_ability.execute(state, None, 1097699445)

        assert result is False


class TestUnitRemoveAbility:
    """测试UnitRemoveAbility native函数。"""

    def test_remove_ability_from_unit(self):
        """测试从单位移除技能。"""
        state = StateContext()
        add_ability = UnitAddAbility()
        remove_ability = UnitRemoveAbility()
        unit = state.handle_manager.create_unit("hfoo", 0, 100.0, 200.0, 0.0)
        ability_id = 1097699445

        add_ability.execute(state, unit, ability_id)
        result = remove_ability.execute(state, unit, ability_id)

        assert result is True
        assert unit.has_ability(ability_id) is False

    def test_remove_nonexistent_ability_returns_false(self):
        """测试移除不存在的技能返回False。"""
        state = StateContext()
        remove_ability = UnitRemoveAbility()
        unit = state.handle_manager.create_unit("hfoo", 0, 100.0, 200.0, 0.0)

        result = remove_ability.execute(state, unit, 1097699445)

        assert result is False
```

**Step 2: 运行测试验证失败**

```bash
pytest tests/natives/test_ability_natives.py::TestUnitAddAbility -v
```

Expected: FAIL（ability_natives.py不存在）

**Step 3: 实现UnitAddAbility和UnitRemoveAbility**

创建 `src/jass_runner/natives/ability_natives.py`：

```python
"""技能系统Native函数实现。

此模块包含JASS技能相关native函数的实现。
"""

import logging
from .base import NativeFunction
from .handle import Unit

logger = logging.getLogger(__name__)


class UnitAddAbility(NativeFunction):
    """给单位添加技能。

    对应JASS native函数: boolean UnitAddAbility(unit whichUnit, integer abilityId)
    """

    @property
    def name(self) -> str:
        """获取函数名称。"""
        return "UnitAddAbility"

    def execute(self, state_context, unit: Unit, ability_id: int) -> bool:
        """执行UnitAddAbility native函数。

        参数：
            state_context: 状态上下文
            unit: 目标单位
            ability_id: 技能ID（fourcc整数）

        返回：
            添加成功返回True，否则返回False
        """
        if unit is None:
            logger.warning("[UnitAddAbility] 单位为None")
            return False

        if not isinstance(unit, Unit):
            logger.warning("[UnitAddAbility] 参数类型错误")
            return False

        result = unit.add_ability(ability_id)

        if result:
            logger.info(f"[UnitAddAbility] 单位{unit.id}添加技能{ability_id}")
        else:
            logger.debug(f"[UnitAddAbility] 单位{unit.id}已拥有技能{ability_id}")

        return result


class UnitRemoveAbility(NativeFunction):
    """从单位移除技能。

    对应JASS native函数: boolean UnitRemoveAbility(unit whichUnit, integer abilityId)
    """

    @property
    def name(self) -> str:
        """获取函数名称。"""
        return "UnitRemoveAbility"

    def execute(self, state_context, unit: Unit, ability_id: int) -> bool:
        """执行UnitRemoveAbility native函数。

        参数：
            state_context: 状态上下文
            unit: 目标单位
            ability_id: 技能ID

        返回：
            移除成功返回True，否则返回False
        """
        if unit is None:
            logger.warning("[UnitRemoveAbility] 单位为None")
            return False

        if not isinstance(unit, Unit):
            logger.warning("[UnitRemoveAbility] 参数类型错误")
            return False

        result = unit.remove_ability(ability_id)

        if result:
            logger.info(f"[UnitRemoveAbility] 单位{unit.id}移除技能{ability_id}")
        else:
            logger.debug(f"[UnitRemoveAbility] 单位{unit.id}没有技能{ability_id}")

        return result
```

**Step 4: 注册到NativeFactory**

在 `src/jass_runner/natives/factory.py` 中：

1. 添加导入（在第38行附近）：
```python
from .ability_natives import UnitAddAbility, UnitRemoveAbility
```

2. 在 `create_default_registry` 方法中添加注册：
```python
# 注册技能系统native函数
registry.register(UnitAddAbility())
registry.register(UnitRemoveAbility())
```

**Step 5: 运行测试验证通过**

```bash
pytest tests/natives/test_ability_natives.py -v
```

Expected: PASS

**Step 6: 提交**

```bash
git add src/jass_runner/natives/ability_natives.py src/jass_runner/natives/factory.py tests/natives/test_ability_natives.py
git commit -m "feat(natives): add UnitAddAbility and UnitRemoveAbility native functions"
```

---

## Task 3: 实现GetUnitAbilityLevel和SetUnitAbilityLevel

**Files:**
- Modify: `src/jass_runner/natives/ability_natives.py`
- Modify: `src/jass_runner/natives/factory.py`
- Test: `tests/natives/test_ability_natives.py`

**Step 1: 编写失败测试**

在 `tests/natives/test_ability_natives.py` 中添加：

```python
class TestGetUnitAbilityLevel:
    """测试GetUnitAbilityLevel native函数。"""

    def test_get_ability_level_returns_level(self):
        """测试获取技能等级。"""
        state = StateContext()
        add_ability = UnitAddAbility()
        get_level = GetUnitAbilityLevel()
        unit = state.handle_manager.create_unit("hfoo", 0, 100.0, 200.0, 0.0)
        ability_id = 1097699445

        add_ability.execute(state, unit, ability_id)
        result = get_level.execute(state, unit, ability_id)

        assert result == 1  # 默认等级1

    def test_get_nonexistent_ability_level_returns_zero(self):
        """测试获取不存在技能的等级返回0。"""
        state = StateContext()
        get_level = GetUnitAbilityLevel()
        unit = state.handle_manager.create_unit("hfoo", 0, 100.0, 200.0, 0.0)

        result = get_level.execute(state, unit, 1097699445)

        assert result == 0


class TestSetUnitAbilityLevel:
    """测试SetUnitAbilityLevel native函数。"""

    def test_set_ability_level(self):
        """测试设置技能等级。"""
        state = StateContext()
        add_ability = UnitAddAbility()
        set_level = SetUnitAbilityLevel()
        unit = state.handle_manager.create_unit("hfoo", 0, 100.0, 200.0, 0.0)
        ability_id = 1097699445

        add_ability.execute(state, unit, ability_id)
        result = set_level.execute(state, unit, ability_id, 3)

        assert result is True
        assert unit.get_ability_level(ability_id) == 3

    def test_set_nonexistent_ability_level_fails(self):
        """测试设置不存在技能的等级失败。"""
        state = StateContext()
        set_level = SetUnitAbilityLevel()
        unit = state.handle_manager.create_unit("hfoo", 0, 100.0, 200.0, 0.0)

        result = set_level.execute(state, unit, 1097699445, 3)

        assert result is False
```

**Step 2: 运行测试验证失败**

```bash
pytest tests/natives/test_ability_natives.py::TestGetUnitAbilityLevel -v
```

Expected: FAIL（GetUnitAbilityLevel不存在）

**Step 3: 实现两个Native函数**

在 `src/jass_runner/natives/ability_natives.py` 中添加（放在UnitRemoveAbility类之后）：

```python
class GetUnitAbilityLevel(NativeFunction):
    """获取单位技能等级。

    对应JASS native函数: integer GetUnitAbilityLevel(unit whichUnit, integer abilityId)
    """

    @property
    def name(self) -> str:
        """获取函数名称。"""
        return "GetUnitAbilityLevel"

    def execute(self, state_context, unit: Unit, ability_id: int) -> int:
        """执行GetUnitAbilityLevel native函数。

        参数：
            state_context: 状态上下文
            unit: 目标单位
            ability_id: 技能ID

        返回：
            技能等级，单位不存在或技能不存在返回0
        """
        if unit is None:
            return 0

        if not isinstance(unit, Unit):
            return 0

        level = unit.get_ability_level(ability_id)
        return level


class SetUnitAbilityLevel(NativeFunction):
    """设置单位技能等级。

    对应JASS native函数: boolean SetUnitAbilityLevel(unit whichUnit, integer abilityId, integer level)
    """

    @property
    def name(self) -> str:
        """获取函数名称。"""
        return "SetUnitAbilityLevel"

    def execute(self, state_context, unit: Unit, ability_id: int, level: int) -> bool:
        """执行SetUnitAbilityLevel native函数。

        参数：
            state_context: 状态上下文
            unit: 目标单位
            ability_id: 技能ID
            level: 新等级

        返回：
            设置成功返回True，否则返回False
        """
        if unit is None:
            logger.warning("[SetUnitAbilityLevel] 单位为None")
            return False

        if not isinstance(unit, Unit):
            logger.warning("[SetUnitAbilityLevel] 参数类型错误")
            return False

        result = unit.set_ability_level(ability_id, level)

        if result:
            logger.info(f"[SetUnitAbilityLevel] 单位{unit.id}技能{ability_id}等级设为{level}")

        return result
```

**Step 4: 注册到NativeFactory**

在 `src/jass_runner/natives/factory.py` 中：

1. 更新导入：
```python
from .ability_natives import UnitAddAbility, UnitRemoveAbility, GetUnitAbilityLevel, SetUnitAbilityLevel
```

2. 添加注册：
```python
registry.register(GetUnitAbilityLevel())
registry.register(SetUnitAbilityLevel())
```

**Step 5: 运行测试验证通过**

```bash
pytest tests/natives/test_ability_natives.py -v
```

Expected: PASS

**Step 6: 提交**

```bash
git add src/jass_runner/natives/ability_natives.py src/jass_runner/natives/factory.py tests/natives/test_ability_natives.py
git commit -m "feat(natives): add GetUnitAbilityLevel and SetUnitAbilityLevel native functions"
```

---

## Task 4: 实现IncUnitAbilityLevel和DecUnitAbilityLevel

**Files:**
- Modify: `src/jass_runner/natives/ability_natives.py`
- Modify: `src/jass_runner/natives/factory.py`
- Test: `tests/natives/test_ability_natives.py`

**Step 1: 编写失败测试**

在 `tests/natives/test_ability_natives.py` 中添加：

```python
class TestIncUnitAbilityLevel:
    """测试IncUnitAbilityLevel native函数。"""

    def test_increment_ability_level(self):
        """测试增加技能等级。"""
        state = StateContext()
        add_ability = UnitAddAbility()
        inc_level = IncUnitAbilityLevel()
        unit = state.handle_manager.create_unit("hfoo", 0, 100.0, 200.0, 0.0)
        ability_id = 1097699445

        add_ability.execute(state, unit, ability_id)
        result = inc_level.execute(state, unit, ability_id)

        assert result is True
        assert unit.get_ability_level(ability_id) == 2

    def test_increment_nonexistent_ability_fails(self):
        """测试增加不存在技能等级失败。"""
        state = StateContext()
        inc_level = IncUnitAbilityLevel()
        unit = state.handle_manager.create_unit("hfoo", 0, 100.0, 200.0, 0.0)

        result = inc_level.execute(state, unit, 1097699445)

        assert result is False


class TestDecUnitAbilityLevel:
    """测试DecUnitAbilityLevel native函数。"""

    def test_decrement_ability_level(self):
        """测试降低技能等级。"""
        state = StateContext()
        add_ability = UnitAddAbility()
        set_level = SetUnitAbilityLevel()
        dec_level = DecUnitAbilityLevel()
        unit = state.handle_manager.create_unit("hfoo", 0, 100.0, 200.0, 0.0)
        ability_id = 1097699445

        add_ability.execute(state, unit, ability_id)
        set_level.execute(state, unit, ability_id, 3)
        result = dec_level.execute(state, unit, ability_id)

        assert result is True
        assert unit.get_ability_level(ability_id) == 2

    def test_decrement_at_level_one_fails(self):
        """测试在等级1时降低技能等级失败。"""
        state = StateContext()
        add_ability = UnitAddAbility()
        dec_level = DecUnitAbilityLevel()
        unit = state.handle_manager.create_unit("hfoo", 0, 100.0, 200.0, 0.0)
        ability_id = 1097699445

        add_ability.execute(state, unit, ability_id)
        result = dec_level.execute(state, unit, ability_id)

        assert result is False  # 等级1时不能降低
```

**Step 2: 运行测试验证失败**

```bash
pytest tests/natives/test_ability_natives.py::TestIncUnitAbilityLevel -v
```

Expected: FAIL（IncUnitAbilityLevel不存在）

**Step 3: 实现两个Native函数**

在 `src/jass_runner/natives/ability_natives.py` 中添加：

```python
class IncUnitAbilityLevel(NativeFunction):
    """增加单位技能等级。

    对应JASS native函数: boolean IncUnitAbilityLevel(unit whichUnit, integer abilityId)
    """

    @property
    def name(self) -> str:
        """获取函数名称。"""
        return "IncUnitAbilityLevel"

    def execute(self, state_context, unit: Unit, ability_id: int) -> bool:
        """执行IncUnitAbilityLevel native函数。

        参数：
            state_context: 状态上下文
            unit: 目标单位
            ability_id: 技能ID

        返回：
            增加成功返回True，否则返回False
        """
        if unit is None:
            logger.warning("[IncUnitAbilityLevel] 单位为None")
            return False

        if not isinstance(unit, Unit):
            logger.warning("[IncUnitAbilityLevel] 参数类型错误")
            return False

        result = unit.inc_ability_level(ability_id)

        if result:
            new_level = unit.get_ability_level(ability_id)
            logger.info(f"[IncUnitAbilityLevel] 单位{unit.id}技能{ability_id}等级增加到{new_level}")

        return result


class DecUnitAbilityLevel(NativeFunction):
    """降低单位技能等级。

    对应JASS native函数: boolean DecUnitAbilityLevel(unit whichUnit, integer abilityId)
    """

    @property
    def name(self) -> str:
        """获取函数名称。"""
        return "DecUnitAbilityLevel"

    def execute(self, state_context, unit: Unit, ability_id: int) -> bool:
        """执行DecUnitAbilityLevel native函数。

        参数：
            state_context: 状态上下文
            unit: 目标单位
            ability_id: 技能ID

        返回：
            降低成功返回True，否则返回False（等级已为1或技能不存在）
        """
        if unit is None:
            logger.warning("[DecUnitAbilityLevel] 单位为None")
            return False

        if not isinstance(unit, Unit):
            logger.warning("[DecUnitAbilityLevel] 参数类型错误")
            return False

        result = unit.dec_ability_level(ability_id)

        if result:
            new_level = unit.get_ability_level(ability_id)
            logger.info(f"[DecUnitAbilityLevel] 单位{unit.id}技能{ability_id}等级降低到{new_level}")

        return result
```

**Step 4: 注册到NativeFactory**

在 `src/jass_runner/natives/factory.py` 中：

1. 更新导入：
```python
from .ability_natives import (
    UnitAddAbility, UnitRemoveAbility, GetUnitAbilityLevel,
    SetUnitAbilityLevel, IncUnitAbilityLevel, DecUnitAbilityLevel
)
```

2. 添加注册：
```python
registry.register(IncUnitAbilityLevel())
registry.register(DecUnitAbilityLevel())
```

**Step 5: 运行测试验证通过**

```bash
pytest tests/natives/test_ability_natives.py -v
```

Expected: PASS

**Step 6: 提交**

```bash
git add src/jass_runner/natives/ability_natives.py src/jass_runner/natives/factory.py tests/natives/test_ability_natives.py
git commit -m "feat(natives): add IncUnitAbilityLevel and DecUnitAbilityLevel native functions"
```

---

## Task 5: 实现UnitMakeAbilityPermanent

**Files:**
- Modify: `src/jass_runner/natives/ability_natives.py`
- Modify: `src/jass_runner/natives/factory.py`
- Test: `tests/natives/test_ability_natives.py`

**Step 1: 编写失败测试**

在 `tests/natives/test_ability_natives.py` 中添加：

```python
class TestUnitMakeAbilityPermanent:
    """测试UnitMakeAbilityPermanent native函数。"""

    def test_make_ability_permanent(self):
        """测试使技能永久。"""
        state = StateContext()
        add_ability = UnitAddAbility()
        make_permanent = UnitMakeAbilityPermanent()
        unit = state.handle_manager.create_unit("hfoo", 0, 100.0, 200.0, 0.0)
        ability_id = 1097699445

        add_ability.execute(state, unit, ability_id)
        result = make_permanent.execute(state, unit, ability_id, True)

        assert result is True
        # 在当前实现中，我们只是记录状态，不做实际限制

    def test_make_nonexistent_ability_permanent_fails(self):
        """测试使不存在的技能永久失败。"""
        state = StateContext()
        make_permanent = UnitMakeAbilityPermanent()
        unit = state.handle_manager.create_unit("hfoo", 0, 100.0, 200.0, 0.0)

        result = make_permanent.execute(state, unit, 1097699445, True)

        assert result is False
```

**Step 2: 运行测试验证失败**

```bash
pytest tests/natives/test_ability_natives.py::TestUnitMakeAbilityPermanent -v
```

Expected: FAIL（UnitMakeAbilityPermanent不存在）

**Step 3: 先在Unit类中添加永久技能支持**

在 `src/jass_runner/natives/handle.py` 的Unit类中：

1. 在`__init__`方法中添加（在`_abilities`定义之后）：
```python
self._permanent_abilities: Set[int] = set()  # 永久技能ID集合
```

2. 添加以下方法：

```python
def make_ability_permanent(self, ability_id: int, permanent: bool) -> bool:
    """设置技能是否为永久技能。

    参数：
        ability_id: 技能ID
        permanent: True表示设为永久，False表示取消永久

    返回：
        设置成功返回True，技能不存在返回False
    """
    if ability_id not in self._abilities:
        return False

    if permanent:
        self._permanent_abilities.add(ability_id)
    else:
        self._permanent_abilities.discard(ability_id)

    return True

def is_ability_permanent(self, ability_id: int) -> bool:
    """检查技能是否为永久技能。

    参数：
        ability_id: 技能ID

    返回：
        是永久技能返回True，否则返回False
    """
    return ability_id in self._permanent_abilities
```

**Step 4: 实现UnitMakeAbilityPermanent Native函数**

在 `src/jass_runner/natives/ability_natives.py` 中添加：

```python
class UnitMakeAbilityPermanent(NativeFunction):
    """设置单位技能是否为永久技能。

    对应JASS native函数: boolean UnitMakeAbilityPermanent(unit whichUnit, integer abilityId, boolean permanent)

    注意: 永久技能通常不会被某些游戏机制（如变身结束）移除。
    在当前模拟实现中，我们只是记录这个状态。
    """

    @property
    def name(self) -> str:
        """获取函数名称。"""
        return "UnitMakeAbilityPermanent"

    def execute(self, state_context, unit: Unit, ability_id: int, permanent: bool) -> bool:
        """执行UnitMakeAbilityPermanent native函数。

        参数：
            state_context: 状态上下文
            unit: 目标单位
            ability_id: 技能ID
            permanent: 是否设为永久

        返回：
            设置成功返回True，否则返回False
        """
        if unit is None:
            logger.warning("[UnitMakeAbilityPermanent] 单位为None")
            return False

        if not isinstance(unit, Unit):
            logger.warning("[UnitMakeAbilityPermanent] 参数类型错误")
            return False

        result = unit.make_ability_permanent(ability_id, permanent)

        if result:
            status = "永久" if permanent else "非永久"
            logger.info(f"[UnitMakeAbilityPermanent] 单位{unit.id}技能{ability_id}设为{status}")

        return result
```

**Step 5: 注册到NativeFactory**

在 `src/jass_runner/natives/factory.py` 中：

1. 更新导入，添加`UnitMakeAbilityPermanent`

2. 添加注册：
```python
registry.register(UnitMakeAbilityPermanent())
```

**Step 6: 运行测试验证通过**

```bash
pytest tests/natives/test_ability_natives.py -v
```

Expected: PASS

**Step 7: 提交**

```bash
git add src/jass_runner/natives/handle.py src/jass_runner/natives/ability_natives.py src/jass_runner/natives/factory.py tests/natives/test_ability_natives.py
git commit -m "feat(natives): add UnitMakeAbilityPermanent native function"
```

---

## Task 6: 添加集成测试和更新工厂测试计数

**Files:**
- Create: `tests/integration/test_ability_natives.py`
- Modify: `tests/natives/test_factory.py`

**Step 1: 编写集成测试**

创建 `tests/integration/test_ability_natives.py`：

```python
"""技能系统Native函数集成测试。"""

from jass_runner.vm.jass_vm import JassVM


class TestAbilityNativesIntegration:
    """测试技能系统native函数完整工作流。"""

    def test_ability_lifecycle_workflow(self):
        """测试技能完整生命周期。"""
        code = '''
        function main takes nothing returns nothing
            local unit u
            local integer ability_id

            // 创建单位
            set u = CreateUnit(Player(0), 1213484355, 100.0, 200.0, 0.0)

            // 添加技能（使用技能ID）
            set ability_id = 1097699445  // 'AHhb' - 圣光术
            call UnitAddAbility(u, ability_id)

            // 设置技能等级
            call SetUnitAbilityLevel(u, ability_id, 3)

            // 增加等级
            call IncUnitAbilityLevel(u, ability_id)

            // 降低等级
            call DecUnitAbilityLevel(u, ability_id)

            // 设为永久技能
            call UnitMakeAbilityPermanent(u, ability_id, true)

            // 移除技能
            call UnitRemoveAbility(u, ability_id)
        endfunction
        '''

        vm = JassVM()
        vm.load_script(code)
        vm.execute()

    def test_ability_with_nested_calls(self):
        """测试嵌套调用和技能操作。"""
        code = '''
        function main takes nothing returns nothing
            local unit u
            local integer ability_id

            // 创建单位并添加技能
            set u = CreateUnit(Player(0), 1213484355, 100.0, 200.0, 0.0)
            set ability_id = 1097699445

            // 添加技能
            call UnitAddAbility(u, ability_id)

            // 获取并验证等级
            // (实际JASS中会用条件判断，这里仅测试native函数调用)
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
# 检查基础函数数量（7个基础 + 19个触发器 + 15个数学 + 2个异步 + 14个单位操作 + 8个单位组 = 65）
all_funcs = registry.get_all()
assert len(all_funcs) == 65
```

修改为：
```python
# 检查基础函数数量（7个基础 + 19个触发器 + 15个数学 + 2个异步 + 14个单位操作 + 8个单位组 + 7个技能 = 72）
all_funcs = registry.get_all()
assert len(all_funcs) == 72
```

**Step 3: 运行所有相关测试**

```bash
pytest tests/natives/test_ability_natives.py tests/integration/test_ability_natives.py tests/natives/test_factory.py -v
```

Expected: PASS

**Step 4: 提交**

```bash
git add tests/integration/test_ability_natives.py tests/natives/test_factory.py
git commit -m "test: add ability natives integration tests and update factory test count"
```

---

## Task 7: 运行完整测试套件

**Files:**
- 所有测试文件

**Step 1: 运行完整测试套件**

```bash
pytest tests/ -v
```

Expected: 所有测试通过（538+ 测试）

**Step 2: 提交（如有必要）**

如果有任何修复，提交更改。

---

## Task 8: 更新项目文档

**Files:**
- Modify: `PROJECT_NOTES.md`
- Modify: `TODO.md`

**Step 1: 添加完成记录到PROJECT_NOTES.md**

在文件末尾添加：

```markdown
#### 46. 技能系统Native函数实现完成 (2026-03-02)
- **新增组件**:
  - Unit类技能支持 - 存储技能等级和永久状态
  - `ability_natives.py` - 7个技能系统Native函数
- **新增Native函数**:
  - 技能管理: UnitAddAbility, UnitRemoveAbility
  - 等级查询: GetUnitAbilityLevel, SetUnitAbilityLevel
  - 等级调整: IncUnitAbilityLevel, DecUnitAbilityLevel
  - 永久技能: UnitMakeAbilityPermanent
- **修改文件**:
  - `src/jass_runner/natives/handle.py` - 添加技能存储和管理方法
  - `src/jass_runner/natives/ability_natives.py` - 新建，实现7个函数
  - `src/jass_runner/natives/factory.py` - 注册新函数
- **测试覆盖**:
  - 单元测试: Unit技能方法、7个native函数
  - 集成测试: 完整技能系统工作流
- **测试统计**: 所有测试通过
```

**Step 2: 更新TODO.md**

找到第二批任务：
```markdown
  - [ ] 第二批：技能系统核心（UnitAddAbility, UnitRemoveAbility, GetUnitAbilityLevel, SetUnitAbilityLevel, IncUnitAbilityLevel, DecUnitAbilityLevel, UnitMakeAbilityPermanent）
```

改为：
```markdown
  - [x] 第二批：技能系统核心（UnitAddAbility, UnitRemoveAbility, GetUnitAbilityLevel, SetUnitAbilityLevel, IncUnitAbilityLevel, DecUnitAbilityLevel, UnitMakeAbilityPermanent）✅ 已完成
```

**Step 3: 提交**

```bash
git add PROJECT_NOTES.md TODO.md
git commit -m "docs: update project notes for ability natives implementation"
```

---

## 实施完成检查清单

- [ ] Task 1: 在Unit类中添加技能支持
- [ ] Task 2: 实现UnitAddAbility和UnitRemoveAbility
- [ ] Task 3: 实现GetUnitAbilityLevel和SetUnitAbilityLevel
- [ ] Task 4: 实现IncUnitAbilityLevel和DecUnitAbilityLevel
- [ ] Task 5: 实现UnitMakeAbilityPermanent
- [ ] Task 6: 添加集成测试和更新工厂测试计数
- [ ] Task 7: 运行完整测试套件
- [ ] Task 8: 更新项目文档

---

## 注意事项

1. **技能ID格式**: 使用fourcc整数格式（如1097699445代表'AHhb'）
2. **等级限制**: 技能等级必须大于0，降低等级时不能低于1
3. **永久技能**: 在当前模拟中只是记录状态，不影响实际游戏逻辑
4. **向后兼容**: 不影响现有功能，所有现有测试应继续通过
