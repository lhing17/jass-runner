# 第四批单位状态扩展Native函数实施计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 实现7个单位状态相关Native函数：GetWidgetLife, SetWidgetLife, UnitDamageTarget, GetUnitLevel, IsUnitType, IsUnitAlive, IsUnitDead

**Architecture:** 扩展Unit类添加level属性，创建新的unit_state_natives.py模块实现状态查询和修改函数，遵循现有native函数实现模式。

**Tech Stack:** Python, pytest, 现有JASS Runner架构

---

## Task 1: 为Unit类添加level属性

**Files:**
- Modify: `src/jass_runner/natives/handle.py`
- Test: `tests/natives/test_handle.py`

**Step 1: 编写失败测试**

在 `tests/natives/test_handle.py` 中添加：

```python
class TestUnitLevel:
    """测试单位等级属性。"""

    def test_unit_default_level(self):
        """测试单位默认等级为1。"""
        from jass_runner.natives.handle import Unit
        unit = Unit("unit_1", "hfoo", 0, 100.0, 200.0, 0.0)
        assert unit.level == 1

    def test_unit_custom_level(self):
        """测试自定义单位等级。"""
        from jass_runner.natives.handle import Unit
        unit = Unit("unit_1", "hfoo", 0, 100.0, 200.0, 0.0)
        unit.level = 3
        assert unit.level == 3
```

**Step 2: 运行测试验证失败**

```bash
pytest tests/natives/test_handle.py::TestUnitLevel -v
```

Expected: FAIL（Unit对象没有level属性）

**Step 3: 为Unit类添加level属性**

在 `src/jass_runner/natives/handle.py` 中修改Unit类的`__init__`方法：

```python
def __init__(self, handle_id: str, unit_type: str, player_id: int,
             x: float, y: float, facing: float, name: str = None):
    super().__init__(handle_id, "unit")
    self.unit_type = unit_type
    self.player_id = player_id
    self.x = x
    self.y = y
    self.z = 0.0  # Z轴高度，默认为0
    self.facing = facing
    self.life = 100.0
    self.max_life = 100.0
    self.mana = 50.0
    self.max_mana = 50.0
    self.name = name or unit_type  # 如果没有提供名称，使用单位类型
    self.level = 1  # 单位等级，默认为1
    self._abilities: Dict[int, int] = {}  # 技能ID -> 等级
    self._permanent_abilities: Set[int] = set()  # 永久技能集合
```

**Step 4: 运行测试验证通过**

```bash
pytest tests/natives/test_handle.py::TestUnitLevel -v
```

Expected: PASS

**Step 5: 提交**

```bash
git add src/jass_runner/natives/handle.py tests/natives/test_handle.py
git commit -m "feat(handle): add level attribute to Unit class"
```

---

## Task 2: 实现GetWidgetLife和SetWidgetLife

**Files:**
- Create: `src/jass_runner/natives/unit_state_natives.py`
- Modify: `src/jass_runner/natives/factory.py`
- Test: `tests/natives/test_unit_state_natives.py`

**Step 1: 编写失败测试**

创建 `tests/natives/test_unit_state_natives.py`：

```python
"""单位状态Native函数测试。

此模块包含单位状态相关native函数的测试用例。
"""

import pytest
from jass_runner.natives.state import StateContext
from jass_runner.natives.unit_state_natives import GetWidgetLife, SetWidgetLife


class TestGetWidgetLife:
    """测试GetWidgetLife native函数。"""

    def test_get_widget_life_of_unit(self):
        """测试获取单位生命值。"""
        state = StateContext()
        get_life = GetWidgetLife()

        unit = state.handle_manager.create_unit("hfoo", 0, 100.0, 200.0, 0.0)
        # 默认生命值为100
        result = get_life.execute(state, unit)

        assert result == 100.0

    def test_get_widget_life_of_none(self):
        """测试获取None生命值返回0。"""
        state = StateContext()
        get_life = GetWidgetLife()

        result = get_life.execute(state, None)

        assert result == 0.0


class TestSetWidgetLife:
    """测试SetWidgetLife native函数。"""

    def test_set_widget_life(self):
        """测试设置单位生命值。"""
        state = StateContext()
        get_life = GetWidgetLife()
        set_life = SetWidgetLife()

        unit = state.handle_manager.create_unit("hfoo", 0, 100.0, 200.0, 0.0)
        # 设置生命值为50
        set_life.execute(state, unit, 50.0)

        result = get_life.execute(state, unit)
        assert result == 50.0

    def test_set_widget_life_to_zero_kills_unit(self):
        """测试设置生命值为0会杀死单位。"""
        state = StateContext()
        set_life = SetWidgetLife()

        unit = state.handle_manager.create_unit("hfoo", 0, 100.0, 200.0, 0.0)
        # 设置生命值为0
        set_life.execute(state, unit, 0.0)

        assert not unit.is_alive()

    def test_set_widget_life_of_none(self):
        """测试设置None生命值不报错。"""
        state = StateContext()
        set_life = SetWidgetLife()

        # 应该不报错
        set_life.execute(state, None, 50.0)
```

**Step 2: 运行测试验证失败**

```bash
pytest tests/natives/test_unit_state_natives.py -v
```

Expected: FAIL（GetWidgetLife和SetWidgetLife不存在）

**Step 3: 实现两个Native函数**

创建 `src/jass_runner/natives/unit_state_natives.py`：

```python
"""单位状态Native函数实现。

此模块包含JASS单位状态相关native函数的实现。
"""

import logging
from typing import Optional
from .base import NativeFunction
from .handle import Unit

logger = logging.getLogger(__name__)


class GetWidgetLife(NativeFunction):
    """获取widget（单位/建筑）的生命值。

    对应JASS native函数: real GetWidgetLife(widget whichWidget)

    注意: 在JASS中widget是unit和destructable的基类。
    这里我们主要处理unit类型。
    """

    @property
    def name(self) -> str:
        """获取函数名称。"""
        return "GetWidgetLife"

    def execute(self, state_context, widget) -> float:
        """执行GetWidgetLife native函数。

        参数：
            state_context: 状态上下文
            widget: widget对象（通常是unit）

        返回：
            当前生命值，如果widget为None返回0
        """
        if widget is None:
            return 0.0

        # 检查是否有life属性
        if hasattr(widget, 'life'):
            return float(widget.life)

        return 0.0


class SetWidgetLife(NativeFunction):
    """设置widget（单位/建筑）的生命值。

    对应JASS native函数: void SetWidgetLife(widget whichWidget, real newLife)

    注意: 如果设置为0或以下，单位会被杀死。
    """

    @property
    def name(self) -> str:
        """获取函数名称。"""
        return "SetWidgetLife"

    def execute(self, state_context, widget, new_life: float):
        """执行SetWidgetLife native函数。

        参数：
            state_context: 状态上下文
            widget: widget对象（通常是unit）
            new_life: 新的生命值
        """
        if widget is None:
            logger.warning("[SetWidgetLife] widget为None")
            return

        if not hasattr(widget, 'life'):
            logger.warning("[SetWidgetLife] widget没有life属性")
            return

        widget.life = new_life

        # 如果生命值<=0，杀死单位
        if new_life <= 0:
            widget.destroy()
            logger.debug(f"[SetWidgetLife] widget {widget.id} 已被杀死")

        logger.debug(f"[SetWidgetLife] widget {widget.id} 生命值设置为 {new_life}")
```

**Step 4: 注册到NativeFactory**

在 `src/jass_runner/natives/factory.py` 中：

1. 添加导入：
```python
from .unit_state_natives import GetWidgetLife, SetWidgetLife
```

2. 在create_default_registry方法中添加注册：
```python
# 注册单位状态native函数
registry.register(GetWidgetLife())
registry.register(SetWidgetLife())
```

**Step 5: 运行测试验证通过**

```bash
pytest tests/natives/test_unit_state_natives.py -v
```

Expected: PASS

**Step 6: 提交**

```bash
git add src/jass_runner/natives/unit_state_natives.py src/jass_runner/natives/factory.py tests/natives/test_unit_state_natives.py
git commit -m "feat(natives): add GetWidgetLife and SetWidgetLife native functions"
```

---

## Task 3: 实现UnitDamageTarget

**Files:**
- Modify: `src/jass_runner/natives/unit_state_natives.py`
- Modify: `src/jass_runner/natives/factory.py`
- Test: `tests/natives/test_unit_state_natives.py`

**Step 1: 编写失败测试**

在 `tests/natives/test_unit_state_natives.py` 中添加：

```python
from jass_runner.natives.unit_state_natives import UnitDamageTarget


class TestUnitDamageTarget:
    """测试UnitDamageTarget native函数。"""

    def test_damage_target_reduces_life(self):
        """测试对目标造成伤害减少生命值。"""
        state = StateContext()
        damage_target = UnitDamageTarget()
        get_life = GetWidgetLife()

        attacker = state.handle_manager.create_unit("hfoo", 0, 100.0, 200.0, 0.0)
        target = state.handle_manager.create_unit("hfoo", 1, 150.0, 200.0, 0.0)

        # 造成25点伤害
        damage_target.execute(state, attacker, target, 25.0, True, False, 0, 0, 0)

        result = get_life.execute(state, target)
        assert result == 75.0  # 100 - 25 = 75

    def test_damage_target_can_kill(self):
        """测试伤害可以杀死目标。"""
        state = StateContext()
        damage_target = UnitDamageTarget()

        attacker = state.handle_manager.create_unit("hfoo", 0, 100.0, 200.0, 0.0)
        target = state.handle_manager.create_unit("hfoo", 1, 150.0, 200.0, 0.0)

        # 造成100点伤害（致命）
        damage_target.execute(state, attacker, target, 100.0, True, False, 0, 0, 0)

        assert not target.is_alive()

    def test_damage_target_with_none_params(self):
        """测试None参数不报错。"""
        state = StateContext()
        damage_target = UnitDamageTarget()

        # 应该不报错
        damage_target.execute(state, None, None, 25.0, True, False, 0, 0, 0)
```

**Step 2: 运行测试验证失败**

```bash
pytest tests/natives/test_unit_state_natives.py::TestUnitDamageTarget -v
```

Expected: FAIL（UnitDamageTarget不存在）

**Step 3: 实现UnitDamageTarget**

在 `src/jass_runner/natives/unit_state_natives.py` 中添加：

```python
class UnitDamageTarget(NativeFunction):
    """让单位对目标造成伤害。

    对应JASS native函数: boolean UnitDamageTarget(unit whichUnit, widget target, real amount, boolean attack, boolean ranged, attacktype attackType, damagetype damageType, weapontype weaponType)

    注意: 这是一个简化实现，忽略攻击类型参数。
    """

    @property
    def name(self) -> str:
        """获取函数名称。"""
        return "UnitDamageTarget"

    def execute(self, state_context, attacker, target, amount: float,
                attack: bool = True, ranged: bool = False,
                attack_type: int = 0, damage_type: int = 0,
                weapon_type: int = 0) -> bool:
        """执行UnitDamageTarget native函数。

        参数：
            state_context: 状态上下文
            attacker: 攻击单位
            target: 目标widget
            amount: 伤害数值
            attack: 是否为攻击伤害
            ranged: 是否为远程伤害
            attack_type: 攻击类型（简化实现中忽略）
            damage_type: 伤害类型（简化实现中忽略）
            weapon_type: 武器类型（简化实现中忽略）

        返回：
            伤害成功返回True
        """
        if attacker is None or target is None:
            logger.warning("[UnitDamageTarget] 攻击者或目标为None")
            return False

        if not hasattr(target, 'life'):
            logger.warning("[UnitDamageTarget] 目标没有life属性")
            return False

        # 应用伤害
        target.life -= amount

        # 如果生命值<=0，杀死目标
        if target.life <= 0:
            target.destroy()
            logger.info(f"[UnitDamageTarget] 目标 {target.id} 被 {attacker.id} 杀死")
        else:
            logger.debug(f"[UnitDamageTarget] {attacker.id} 对 {target.id} 造成 {amount} 点伤害")

        return True
```

**Step 4: 注册到NativeFactory**

在 `src/jass_runner/natives/factory.py` 中：

1. 更新导入，添加UnitDamageTarget
2. 添加注册：
```python
registry.register(UnitDamageTarget())
```

**Step 5: 运行测试验证通过**

```bash
pytest tests/natives/test_unit_state_natives.py::TestUnitDamageTarget -v
```

Expected: PASS

**Step 6: 提交**

```bash
git add src/jass_runner/natives/unit_state_natives.py src/jass_runner/natives/factory.py tests/natives/test_unit_state_natives.py
git commit -m "feat(natives): add UnitDamageTarget native function"
```

---

## Task 4: 实现GetUnitLevel

**Files:**
- Modify: `src/jass_runner/natives/unit_state_natives.py`
- Modify: `src/jass_runner/natives/factory.py`
- Test: `tests/natives/test_unit_state_natives.py`

**Step 1: 编写失败测试**

在 `tests/natives/test_unit_state_natives.py` 中添加：

```python
from jass_runner.natives.unit_state_natives import GetUnitLevel


class TestGetUnitLevel:
    """测试GetUnitLevel native函数。"""

    def test_get_unit_level_default(self):
        """测试获取单位默认等级。"""
        state = StateContext()
        get_level = GetUnitLevel()

        unit = state.handle_manager.create_unit("hfoo", 0, 100.0, 200.0, 0.0)
        # 默认等级为1
        result = get_level.execute(state, unit)

        assert result == 1

    def test_get_unit_level_custom(self):
        """测试获取自定义等级。"""
        state = StateContext()
        get_level = GetUnitLevel()

        unit = state.handle_manager.create_unit("hfoo", 0, 100.0, 200.0, 0.0)
        unit.level = 5

        result = get_level.execute(state, unit)
        assert result == 5

    def test_get_unit_level_of_none(self):
        """测试获取None等级返回0。"""
        state = StateContext()
        get_level = GetUnitLevel()

        result = get_level.execute(state, None)

        assert result == 0
```

**Step 2: 运行测试验证失败**

```bash
pytest tests/natives/test_unit_state_natives.py::TestGetUnitLevel -v
```

Expected: FAIL（GetUnitLevel不存在）

**Step 3: 实现GetUnitLevel**

在 `src/jass_runner/natives/unit_state_natives.py` 中添加：

```python
class GetUnitLevel(NativeFunction):
    """获取单位等级。

    对应JASS native函数: integer GetUnitLevel(unit whichUnit)
    """

    @property
    def name(self) -> str:
        """获取函数名称。"""
        return "GetUnitLevel"

    def execute(self, state_context, unit) -> int:
        """执行GetUnitLevel native函数。

        参数：
            state_context: 状态上下文
            unit: 单位对象

        返回：
            单位等级，如果单位为None返回0
        """
        if unit is None:
            return 0

        if hasattr(unit, 'level'):
            return int(unit.level)

        return 0
```

**Step 4: 注册到NativeFactory**

在 `src/jass_runner/natives/factory.py` 中：

1. 更新导入，添加GetUnitLevel
2. 添加注册：
```python
registry.register(GetUnitLevel())
```

**Step 5: 运行测试验证通过**

```bash
pytest tests/natives/test_unit_state_natives.py::TestGetUnitLevel -v
```

Expected: PASS

**Step 6: 提交**

```bash
git add src/jass_runner/natives/unit_state_natives.py src/jass_runner/natives/factory.py tests/natives/test_unit_state_natives.py
git commit -m "feat(natives): add GetUnitLevel native function"
```

---

## Task 5: 实现IsUnitType

**Files:**
- Modify: `src/jass_runner/natives/unit_state_natives.py`
- Modify: `src/jass_runner/natives/factory.py`
- Test: `tests/natives/test_unit_state_natives.py`

**Step 1: 编写失败测试**

在 `tests/natives/test_unit_state_natives.py` 中添加：

```python
from jass_runner.natives.unit_state_natives import IsUnitType


class TestIsUnitType:
    """测试IsUnitType native函数。"""

    def test_is_unit_type_match(self):
        """测试单位类型匹配。"""
        state = StateContext()
        is_unit_type = IsUnitType()

        unit = state.handle_manager.create_unit("hfoo", 0, 100.0, 200.0, 0.0)

        # 检查是否为步兵类型（'hfoo'的FourCC是1213484355）
        result = is_unit_type.execute(state, unit, 1213484355)

        assert result is True

    def test_is_unit_type_no_match(self):
        """测试单位类型不匹配。"""
        state = StateContext()
        is_unit_type = IsUnitType()

        unit = state.handle_manager.create_unit("hkni", 0, 100.0, 200.0, 0.0)

        # 检查是否为步兵类型
        result = is_unit_type.execute(state, unit, 1213484355)  # hfoo

        assert result is False

    def test_is_unit_type_with_none(self):
        """测试None单位返回False。"""
        state = StateContext()
        is_unit_type = IsUnitType()

        result = is_unit_type.execute(state, None, 1213484355)

        assert result is False
```

**Step 2: 运行测试验证失败**

```bash
pytest tests/natives/test_unit_state_natives.py::TestIsUnitType -v
```

Expected: FAIL（IsUnitType不存在）

**Step 3: 实现IsUnitType**

在 `src/jass_runner/natives/unit_state_natives.py` 中添加：

```python
class IsUnitType(NativeFunction):
    """检查单位是否为指定类型。

    对应JASS native函数: boolean IsUnitType(unit whichUnit, unittype whichUnitType)

    注意: 在JASS中unittype是整数（FourCC）。
    """

    @property
    def name(self) -> str:
        """获取函数名称。"""
        return "IsUnitType"

    def execute(self, state_context, unit, unit_type: int) -> bool:
        """执行IsUnitType native函数。

        参数：
            state_context: 状态上下文
            unit: 单位对象
            unit_type: 单位类型（FourCC整数）

        返回：
            单位类型匹配返回True，否则返回False
        """
        if unit is None:
            return False

        if not hasattr(unit, 'unit_type'):
            return False

        # 将单位类型字符串转换为FourCC进行比较
        unit_type_str = unit.unit_type
        unit_type_fourcc = self._string_to_fourcc(unit_type_str)

        return unit_type_fourcc == unit_type

    def _string_to_fourcc(self, s: str) -> int:
        """将4字符字符串转换为FourCC整数。

        参数：
            s: 4字符字符串（如'hfoo'）

        返回：
            FourCC整数
        """
        if len(s) != 4:
            return 0

        result = 0
        for i, char in enumerate(s):
            result |= ord(char) << (i * 8)
        return result
```

**Step 4: 注册到NativeFactory**

在 `src/jass_runner/natives/factory.py` 中：

1. 更新导入，添加IsUnitType
2. 添加注册：
```python
registry.register(IsUnitType())
```

**Step 5: 运行测试验证通过**

```bash
pytest tests/natives/test_unit_state_natives.py::TestIsUnitType -v
```

Expected: PASS

**Step 6: 提交**

```bash
git add src/jass_runner/natives/unit_state_natives.py src/jass_runner/natives/factory.py tests/natives/test_unit_state_natives.py
git commit -m "feat(natives): add IsUnitType native function"
```

---

## Task 6: 实现IsUnitAlive和IsUnitDead

**Files:**
- Modify: `src/jass_runner/natives/unit_state_natives.py`
- Modify: `src/jass_runner/natives/factory.py`
- Test: `tests/natives/test_unit_state_natives.py`

**Step 1: 编写失败测试**

在 `tests/natives/test_unit_state_natives.py` 中添加：

```python
from jass_runner.natives.unit_state_natives import IsUnitAlive, IsUnitDead


class TestIsUnitAlive:
    """测试IsUnitAlive native函数。"""

    def test_is_unit_alive_true(self):
        """测试存活单位返回True。"""
        state = StateContext()
        is_alive = IsUnitAlive()

        unit = state.handle_manager.create_unit("hfoo", 0, 100.0, 200.0, 0.0)

        result = is_alive.execute(state, unit)

        assert result is True

    def test_is_unit_alive_false(self):
        """测试死亡单位返回False。"""
        state = StateContext()
        is_alive = IsUnitAlive()
        set_life = SetWidgetLife()

        unit = state.handle_manager.create_unit("hfoo", 0, 100.0, 200.0, 0.0)
        # 杀死单位
        set_life.execute(state, unit, 0.0)

        result = is_alive.execute(state, unit)

        assert result is False

    def test_is_unit_alive_with_none(self):
        """测试None返回False。"""
        state = StateContext()
        is_alive = IsUnitAlive()

        result = is_alive.execute(state, None)

        assert result is False


class TestIsUnitDead:
    """测试IsUnitDead native函数。"""

    def test_is_unit_dead_false(self):
        """测试存活单位返回False。"""
        state = StateContext()
        is_dead = IsUnitDead()

        unit = state.handle_manager.create_unit("hfoo", 0, 100.0, 200.0, 0.0)

        result = is_dead.execute(state, unit)

        assert result is False

    def test_is_unit_dead_true(self):
        """测试死亡单位返回True。"""
        state = StateContext()
        is_dead = IsUnitDead()
        set_life = SetWidgetLife()

        unit = state.handle_manager.create_unit("hfoo", 0, 100.0, 200.0, 0.0)
        # 杀死单位
        set_life.execute(state, unit, 0.0)

        result = is_dead.execute(state, unit)

        assert result is True

    def test_is_unit_dead_with_none(self):
        """测试None返回True（None被认为是死亡的）。"""
        state = StateContext()
        is_dead = IsUnitDead()

        result = is_dead.execute(state, None)

        assert result is True
```

**Step 2: 运行测试验证失败**

```bash
pytest tests/natives/test_unit_state_natives.py::TestIsUnitAlive tests/natives/test_unit_state_natives.py::TestIsUnitDead -v
```

Expected: FAIL（IsUnitAlive和IsUnitDead不存在）

**Step 3: 实现两个Native函数**

在 `src/jass_runner/natives/unit_state_natives.py` 中添加：

```python
class IsUnitAlive(NativeFunction):
    """检查单位是否存活。

    对应JASS native函数: boolean IsUnitAlive(unit whichUnit)
    """

    @property
    def name(self) -> str:
        """获取函数名称。"""
        return "IsUnitAlive"

    def execute(self, state_context, unit) -> bool:
        """执行IsUnitAlive native函数。

        参数：
            state_context: 状态上下文
            unit: 单位对象

        返回：
            单位存活返回True，否则返回False
        """
        if unit is None:
            return False

        return unit.is_alive()


class IsUnitDead(NativeFunction):
    """检查单位是否死亡。

    对应JASS native函数: boolean IsUnitDead(unit whichUnit)
    """

    @property
    def name(self) -> str:
        """获取函数名称。"""
        return "IsUnitDead"

    def execute(self, state_context, unit) -> bool:
        """执行IsUnitDead native函数。

        参数：
            state_context: 状态上下文
            unit: 单位对象

        返回：
            单位死亡返回True，否则返回False
        """
        if unit is None:
            return True  # None被认为是死亡的

        return not unit.is_alive()
```

**Step 4: 注册到NativeFactory**

在 `src/jass_runner/natives/factory.py` 中：

1. 更新导入，添加IsUnitAlive和IsUnitDead
2. 添加注册：
```python
registry.register(IsUnitAlive())
registry.register(IsUnitDead())
```

**Step 5: 运行测试验证通过**

```bash
pytest tests/natives/test_unit_state_natives.py::TestIsUnitAlive tests/natives/test_unit_state_natives.py::TestIsUnitDead -v
```

Expected: PASS

**Step 6: 提交**

```bash
git add src/jass_runner/natives/unit_state_natives.py src/jass_runner/natives/factory.py tests/natives/test_unit_state_natives.py
git commit -m "feat(natives): add IsUnitAlive and IsUnitDead native functions"
```

---

## Task 7: 添加集成测试

**Files:**
- Create: `tests/integration/test_unit_state_integration.py`

**Step 1: 编写集成测试**

创建 `tests/integration/test_unit_state_integration.py`：

```python
"""单位状态Native函数集成测试。

此模块包含单位状态相关native函数的集成测试。
"""

from jass_runner.vm.jass_vm import JassVM


class TestUnitStateIntegration:
    """测试单位状态native函数完整工作流。"""

    def test_widget_life_workflow(self):
        """测试widget生命值操作工作流。"""
        code = '''
        function main takes nothing returns nothing
            local unit u
            local real life

            // 创建单位
            set u = CreateUnit(Player(0), 1213484355, 100.0, 200.0, 0.0)

            // 获取生命值
            set life = GetWidgetLife(u)
            // life 应该为 100.0

            // 设置生命值
            call SetWidgetLife(u, 50.0)

            // 再次获取
            set life = GetWidgetLife(u)
            // life 应该为 50.0
        endfunction
        '''

        vm = JassVM()
        vm.load_script(code)
        vm.execute()

    def test_unit_damage_workflow(self):
        """测试单位伤害工作流。"""
        code = '''
        function main takes nothing returns nothing
            local unit attacker
            local unit target

            // 创建单位
            set attacker = CreateUnit(Player(0), 1213484355, 100.0, 200.0, 0.0)
            set target = CreateUnit(Player(1), 1213484355, 150.0, 200.0, 0.0)

            // 造成伤害
            call UnitDamageTarget(attacker, target, 25.0, true, false, 0, 0, 0)

            // 目标生命值应该为 75.0
        endfunction
        '''

        vm = JassVM()
        vm.load_script(code)
        vm.execute()
```

**Step 2: 运行测试验证通过**

```bash
pytest tests/integration/test_unit_state_integration.py -v
```

Expected: PASS

**Step 3: 提交**

```bash
git add tests/integration/test_unit_state_integration.py
git commit -m "test(natives): add unit state integration tests"
```

---

## Task 8: 更新工厂测试计数和文档

**Files:**
- Modify: `tests/natives/test_factory.py`
- Modify: `TODO.md`

**Step 1: 更新工厂测试计数**

修改 `tests/natives/test_factory.py`：

```python
# 检查基础函数数量（7个基础 + 19个触发器 + 15个数学 + 2个异步 + 14个单位操作 + 14个单位组 + 7个技能 + 7个单位状态 = 85）
all_funcs = registry.get_all()
assert len(all_funcs) == 85
```

**Step 2: 更新TODO.md**

修改 `TODO.md`：

```markdown
- [x] 第四批：单位状态扩展（GetWidgetLife, SetWidgetLife, UnitDamageTarget, GetUnitLevel, IsUnitType, IsUnitAlive, IsUnitDead）✅ 已完成
```

**Step 3: 运行测试验证通过**

```bash
pytest tests/natives/test_factory.py -v
```

Expected: PASS

**Step 4: 提交**

```bash
git add tests/natives/test_factory.py TODO.md
git commit -m "test(natives): update factory count and mark fourth batch as completed"
```

---

## Task 9: 运行完整测试套件

**Step 1: 运行完整测试**

```bash
pytest tests/ -q
```

Expected: 所有测试通过

**Step 2: 最终提交（如果有未提交的更改）**

```bash
git status
# 如果有更改，提交
```

---

## 总结

第四批单位状态扩展Native函数实施完成，包括：

1. **GetWidgetLife** - 获取widget生命值
2. **SetWidgetLife** - 设置widget生命值（<=0会杀死单位）
3. **UnitDamageTarget** - 单位对目标造成伤害
4. **GetUnitLevel** - 获取单位等级
5. **IsUnitType** - 检查单位类型（FourCC比较）
6. **IsUnitAlive** - 检查单位是否存活
7. **IsUnitDead** - 检查单位是否死亡

**新增文件：**
- `src/jass_runner/natives/unit_state_natives.py` - 单位状态native函数实现
- `tests/natives/test_unit_state_natives.py` - 单元测试
- `tests/integration/test_unit_state_integration.py` - 集成测试

**修改文件：**
- `src/jass_runner/natives/handle.py` - 添加level属性
- `src/jass_runner/natives/factory.py` - 注册新native函数
- `tests/natives/test_factory.py` - 更新计数
- `TODO.md` - 标记完成
