# 单位所有权与关系Native函数实施计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 实现7个单位所有权与关系Native函数：SetUnitOwner, IsUnitOwnedByPlayer, IsUnitAlly, IsUnitEnemy, IsUnitInRange, IsUnitInRangeXY, IsUnitInRangeLoc

**Architecture:** 扩展Player类添加盟友/敌对关系管理，创建两个新的native函数模块（unit_ownership_natives.py和unit_range_natives.py），通过HandleManager集成玩家查询功能

**Tech Stack:** Python 3.8+, pytest, 现有JASS Runner架构（Handle系统、Native函数框架）

---

## 前置知识

### 相关文件位置
- Player类: `src/jass_runner/handles/player.py`
- Unit类: `src/jass_runner/handles/unit.py`
- HandleManager: `src/jass_runner/natives/manager.py`
- Native基类: `src/jass_runner/natives/base.py`
- Native工厂: `src/jass_runner/natives/factory.py`
- 现有单位状态函数参考: `src/jass_runner/natives/unit_state_natives.py`

### common.j函数签名
```
native SetUnitOwner takes unit whichUnit, player whichPlayer, boolean changeColor returns nothing
constant native IsUnitOwnedByPlayer takes unit whichUnit, player whichPlayer returns boolean
constant native IsUnitAlly takes unit whichUnit, player whichPlayer returns boolean
constant native IsUnitEnemy takes unit whichUnit, player whichPlayer returns boolean
constant native IsUnitInRange takes unit whichUnit, unit otherUnit, real distance returns boolean
constant native IsUnitInRangeXY takes unit whichUnit, real x, real y, real distance returns boolean
constant native IsUnitInRangeLoc takes unit whichUnit, location whichLocation, real distance returns boolean
```

---

## Task 1: 扩展Player类添加关系管理

**Files:**
- Modify: `src/jass_runner/handles/player.py`
- Test: `tests/handles/test_player.py` (创建)

**Step 1: 编写Player关系管理测试**

创建 `tests/handles/test_player.py`:
```python
"""Player类测试。"""

import pytest
from src.jass_runner.handles.player import Player


class TestPlayerAlliance:
    """测试Player关系管理功能。"""

    def test_player_default_no_alliance(self):
        """测试Player默认无盟友关系。"""
        player1 = Player(0)
        player2 = Player(1)

        assert not player1.is_ally(1)
        assert not player1.is_enemy(1)

    def test_player_set_alliance_true(self):
        """测试设置盟友关系。"""
        player1 = Player(0)

        player1.set_alliance(1, True)

        assert player1.is_ally(1)
        assert not player1.is_enemy(1)

    def test_player_set_alliance_false(self):
        """测试设置敌对关系。"""
        player1 = Player(0)

        player1.set_alliance(1, False)

        assert player1.is_enemy(1)
        assert not player1.is_ally(1)

    def test_player_alliance_mutual_exclusive(self):
        """测试盟友和敌对关系互斥。"""
        player1 = Player(0)

        player1.set_alliance(1, True)
        assert player1.is_ally(1)

        player1.set_alliance(1, False)
        assert not player1.is_ally(1)
        assert player1.is_enemy(1)

        player1.set_alliance(1, True)
        assert player1.is_ally(1)
        assert not player1.is_enemy(1)
```

**Step 2: 运行测试确认失败**

```bash
pytest tests/handles/test_player.py -v
```

Expected: FAIL with "AttributeError: 'Player' object has no attribute 'set_alliance'"

**Step 3: 实现Player关系管理**

修改 `src/jass_runner/handles/player.py`，添加：
```python
from typing import Set


class Player(Handle):
    """玩家对象。"""

    def __init__(self, player_id: int):
        super().__init__()
        self.player_id = player_id
        self.name = f"玩家{player_id}"
        self.race = None
        self.color = player_id
        self.slot_state = "playing"
        self.controller = "user"
        self._allies: Set[int] = set()
        self._enemies: Set[int] = set()

    def set_alliance(self, other_player_id: int, is_ally: bool) -> None:
        """设置与其他玩家的关系。

        参数：
            other_player_id: 其他玩家ID
            is_ally: True为盟友，False为敌人
        """
        if is_ally:
            self._allies.add(other_player_id)
            self._enemies.discard(other_player_id)
        else:
            self._enemies.add(other_player_id)
            self._allies.discard(other_player_id)

    def is_ally(self, other_player_id: int) -> bool:
        """检查是否是指定玩家的盟友。"""
        return other_player_id in self._allies

    def is_enemy(self, other_player_id: int) -> bool:
        """检查是否是指定玩家的敌人。"""
        return other_player_id in self._enemies
```

**Step 4: 运行测试确认通过**

```bash
pytest tests/handles/test_player.py -v
```

Expected: 4 tests PASSED

**Step 5: 提交**

```bash
git add tests/handles/test_player.py src/jass_runner/handles/player.py
git commit -m "feat: add player alliance management"
```

---

## Task 2: 扩展HandleManager添加玩家查询

**Files:**
- Modify: `src/jass_runner/natives/manager.py`
- Test: `tests/natives/test_manager.py` (添加测试)

**Step 1: 编写HandleManager玩家查询测试**

在 `tests/natives/test_manager.py` 添加：
```python
    def test_get_player_by_id_returns_player(self):
        """测试通过ID获取玩家对象。"""
        from src.jass_runner.handles.player import Player
        manager = HandleManager()

        player = manager.get_player_by_id(0)

        assert isinstance(player, Player)
        assert player.player_id == 0

    def test_get_player_by_id_caches_player(self):
        """测试玩家对象被缓存。"""
        manager = HandleManager()

        player1 = manager.get_player_by_id(1)
        player2 = manager.get_player_by_id(1)

        assert player1 is player2

    def test_get_player_by_id_invalid_returns_none(self):
        """测试无效玩家ID返回None。"""
        manager = HandleManager()

        result = manager.get_player_by_id(16)

        assert result is None
```

**Step 2: 运行测试确认失败**

```bash
pytest tests/natives/test_manager.py::TestHandleManager::test_get_player_by_id_returns_player -v
```

Expected: FAIL with "AttributeError: 'HandleManager' object has no attribute 'get_player_by_id'"

**Step 3: 实现HandleManager玩家查询**

修改 `src/jass_runner/natives/manager.py`，添加：
```python
from typing import Optional
from src.jass_runner.handles.player import Player


class HandleManager:
    """句柄管理器。"""

    def __init__(self):
        self._handles: Dict[int, Handle] = {}
        self._next_id = 1
        self._players: Dict[int, Player] = {}  # 缓存玩家对象

    def get_player_by_id(self, player_id: int) -> Optional[Player]:
        """通过ID获取玩家对象。

        参数：
            player_id: 玩家ID (0-15)

        返回：
            Player对象，如果ID无效则返回None
        """
        if not 0 <= player_id <= 15:
            return None

        if player_id not in self._players:
            self._players[player_id] = Player(player_id)

        return self._players[player_id]
```

**Step 4: 运行测试确认通过**

```bash
pytest tests/natives/test_manager.py -v
```

Expected: 所有测试 PASSED

**Step 5: 提交**

```bash
git add tests/natives/test_manager.py src/jass_runner/natives/manager.py
git commit -m "feat: add get_player_by_id to HandleManager"
```

---

## Task 3: 实现IsUnitOwnedByPlayer

**Files:**
- Create: `src/jass_runner/natives/unit_ownership_natives.py`
- Create: `tests/natives/test_unit_ownership_natives.py`
- Modify: `src/jass_runner/natives/factory.py` (注册)

**Step 1: 编写IsUnitOwnedByPlayer测试**

创建 `tests/natives/test_unit_ownership_natives.py`:
```python
"""单位所有权Native函数测试。"""

import pytest
from src.jass_runner.natives.unit_ownership_natives import IsUnitOwnedByPlayer
from src.jass_runner.handles.unit import Unit
from src.jass_runner.handles.player import Player


class TestIsUnitOwnedByPlayer:
    """测试IsUnitOwnedByPlayer函数。"""

    def test_unit_owned_by_correct_player(self):
        """测试单位属于指定玩家时返回True。"""
        native = IsUnitOwnedByPlayer()
        unit = Unit("Hpal", 0, 0.0, 0.0)
        player = Player(0)

        result = native.execute(unit, player)

        assert result is True

    def test_unit_not_owned_by_different_player(self):
        """测试单位不属于指定玩家时返回False。"""
        native = IsUnitOwnedByPlayer()
        unit = Unit("Hpal", 0, 0.0, 0.0)
        player = Player(1)

        result = native.execute(unit, player)

        assert result is False

    def test_null_unit_returns_false(self):
        """测试null单位返回False。"""
        native = IsUnitOwnedByPlayer()
        player = Player(0)

        result = native.execute(None, player)

        assert result is False

    def test_null_player_returns_false(self):
        """测试null玩家返回False。"""
        native = IsUnitOwnedByPlayer()
        unit = Unit("Hpal", 0, 0.0, 0.0)

        result = native.execute(unit, None)

        assert result is False
```

**Step 2: 运行测试确认失败**

```bash
pytest tests/natives/test_unit_ownership_natives.py::TestIsUnitOwnedByPlayer -v
```

Expected: FAIL with "ModuleNotFoundError: No module named 'src.jass_runner.natives.unit_ownership_natives'"

**Step 3: 实现IsUnitOwnedByPlayer**

创建 `src/jass_runner/natives/unit_ownership_natives.py`:
```python
"""单位所有权Native函数实现。

包含单位所有权查询和玩家关系检测函数。
"""

import logging
from typing import Any, Optional

from src.jass_runner.natives.base import NativeFunction
from src.jass_runner.handles.unit import Unit
from src.jass_runner.handles.player import Player


logger = logging.getLogger(__name__)


class IsUnitOwnedByPlayer(NativeFunction):
    """检查单位是否属于指定玩家。"""

    @property
    def name(self) -> str:
        return "IsUnitOwnedByPlayer"

    def execute(self, which_unit: Optional[Unit], which_player: Optional[Player]) -> bool:
        """执行单位所有权检查。

        参数：
            which_unit: 要检查的单位
            which_player: 要检查的玩家

        返回：
            如果单位属于该玩家返回True，否则返回False
        """
        if which_unit is None or which_player is None:
            return False

        return which_unit.player_id == which_player.player_id
```

**Step 4: 运行测试确认通过**

```bash
pytest tests/natives/test_unit_ownership_natives.py::TestIsUnitOwnedByPlayer -v
```

Expected: 4 tests PASSED

**Step 5: 注册到工厂并提交**

修改 `src/jass_runner/natives/factory.py`，添加导入和注册：
```python
from src.jass_runner.natives.unit_ownership_natives import (
    IsUnitOwnedByPlayer,
)

# 在create_default_registry中添加:
registry.register(IsUnitOwnedByPlayer())
```

```bash
git add tests/natives/test_unit_ownership_natives.py src/jass_runner/natives/unit_ownership_natives.py src/jass_runner/natives/factory.py
git commit -m "feat: implement IsUnitOwnedByPlayer native function"
```

---

## Task 4: 实现IsUnitInRangeXY

**Files:**
- Create: `src/jass_runner/natives/unit_range_natives.py`
- Create: `tests/natives/test_unit_range_natives.py`
- Modify: `src/jass_runner/natives/factory.py` (注册)

**Step 1: 编写IsUnitInRangeXY测试**

创建 `tests/natives/test_unit_range_natives.py`:
```python
"""单位范围检测Native函数测试。"""

import pytest
import math
from src.jass_runner.natives.unit_range_natives import IsUnitInRangeXY
from src.jass_runner.handles.unit import Unit


class TestIsUnitInRangeXY:
    """测试IsUnitInRangeXY函数。"""

    def test_unit_in_range_returns_true(self):
        """测试单位在范围内返回True。"""
        native = IsUnitInRangeXY()
        unit = Unit("Hpal", 0, 0.0, 0.0)

        result = native.execute(unit, 100.0, 0.0, 150.0)

        assert result is True

    def test_unit_out_of_range_returns_false(self):
        """测试单位在范围外返回False。"""
        native = IsUnitInRangeXY()
        unit = Unit("Hpal", 0, 0.0, 0.0)

        result = native.execute(unit, 200.0, 0.0, 150.0)

        assert result is False

    def test_unit_at_exact_distance_returns_true(self):
        """测试单位恰好在边界距离返回True。"""
        native = IsUnitInRangeXY()
        unit = Unit("Hpal", 0, 100.0, 0.0)

        result = native.execute(unit, 0.0, 0.0, 100.0)

        assert result is True

    def test_diagonal_distance(self):
        """测试对角线距离计算。"""
        native = IsUnitInRangeXY()
        unit = Unit("Hpal", 0, 30.0, 40.0)  # 距离50

        result = native.execute(unit, 0.0, 0.0, 50.0)

        assert result is True

        result = native.execute(unit, 0.0, 0.0, 49.9)

        assert result is False

    def test_null_unit_returns_false(self):
        """测试null单位返回False。"""
        native = IsUnitInRangeXY()

        result = native.execute(None, 0.0, 0.0, 100.0)

        assert result is False

    def test_negative_distance_treated_as_zero(self):
        """测试负距离视为0。"""
        native = IsUnitInRangeXY()
        unit = Unit("Hpal", 0, 0.0, 0.0)

        result = native.execute(unit, 0.0, 0.0, -10.0)

        # 距离为0，只有恰好在同一点才返回True
        assert result is True
```

**Step 2: 运行测试确认失败**

```bash
pytest tests/natives/test_unit_range_natives.py::TestIsUnitInRangeXY -v
```

Expected: FAIL

**Step 3: 实现IsUnitInRangeXY**

创建 `src/jass_runner/natives/unit_range_natives.py`:
```python
"""单位范围检测Native函数实现。

包含单位距离检测相关函数。
"""

import logging
import math
from typing import Any, Optional

from src.jass_runner.natives.base import NativeFunction
from src.jass_runner.handles.unit import Unit
from src.jass_runner.handles.location import Location


logger = logging.getLogger(__name__)


class IsUnitInRangeXY(NativeFunction):
    """检查单位是否在指定坐标指定距离内。"""

    @property
    def name(self) -> str:
        return "IsUnitInRangeXY"

    def execute(self, which_unit: Optional[Unit], x: float, y: float, distance: float) -> bool:
        """执行范围检测。

        参数：
            which_unit: 要检查的单位
            x: 目标X坐标
            y: 目标Y坐标
            distance: 检测距离

        返回：
            如果单位在范围内返回True，否则返回False
        """
        if which_unit is None:
            return False

        # 负距离视为0
        if distance < 0:
            distance = 0

        dx = which_unit.x - x
        dy = which_unit.y - y
        actual_distance = math.sqrt(dx * dx + dy * dy)

        return actual_distance <= distance
```

**Step 4: 运行测试确认通过**

```bash
pytest tests/natives/test_unit_range_natives.py::TestIsUnitInRangeXY -v
```

Expected: 6 tests PASSED

**Step 5: 注册到工厂并提交**

修改 `src/jass_runner/natives/factory.py`，添加：
```python
from src.jass_runner.natives.unit_range_natives import (
    IsUnitInRangeXY,
)

# 在create_default_registry中添加:
registry.register(IsUnitInRangeXY())
```

```bash
git add tests/natives/test_unit_range_natives.py src/jass_runner/natives/unit_range_natives.py src/jass_runner/natives/factory.py
git commit -m "feat: implement IsUnitInRangeXY native function"
```

---

## Task 5: 实现IsUnitInRangeLoc

**Files:**
- Modify: `src/jass_runner/natives/unit_range_natives.py`
- Modify: `tests/natives/test_unit_range_natives.py`
- Modify: `src/jass_runner/natives/factory.py` (注册)

**Step 1: 编写IsUnitInRangeLoc测试**

在 `tests/natives/test_unit_range_natives.py` 添加：
```python
from src.jass_runner.handles.location import Location


class TestIsUnitInRangeLoc:
    """测试IsUnitInRangeLoc函数。"""

    def test_unit_in_range_of_location(self):
        """测试单位在位置范围内。"""
        from src.jass_runner.natives.unit_range_natives import IsUnitInRangeLoc
        native = IsUnitInRangeLoc()
        unit = Unit("Hpal", 0, 50.0, 50.0)
        loc = Location(0.0, 0.0)

        result = native.execute(unit, loc, 100.0)

        assert result is True

    def test_unit_out_of_range_of_location(self):
        """测试单位在位置范围外。"""
        from src.jass_runner.natives.unit_range_natives import IsUnitInRangeLoc
        native = IsUnitInRangeLoc()
        unit = Unit("Hpal", 0, 200.0, 200.0)
        loc = Location(0.0, 0.0)

        result = native.execute(unit, loc, 100.0)

        assert result is False

    def test_null_location_returns_false(self):
        """测试null位置返回False。"""
        from src.jass_runner.natives.unit_range_natives import IsUnitInRangeLoc
        native = IsUnitInRangeLoc()
        unit = Unit("Hpal", 0, 0.0, 0.0)

        result = native.execute(unit, None, 100.0)

        assert result is False
```

**Step 2: 运行测试确认失败**

```bash
pytest tests/natives/test_unit_range_natives.py::TestIsUnitInRangeLoc -v
```

Expected: FAIL

**Step 3: 实现IsUnitInRangeLoc**

在 `src/jass_runner/natives/unit_range_natives.py` 添加：
```python
class IsUnitInRangeLoc(NativeFunction):
    """检查单位是否在指定位置指定距离内。"""

    @property
    def name(self) -> str:
        return "IsUnitInRangeLoc"

    def execute(self, which_unit: Optional[Unit], which_location: Optional[Location], distance: float) -> bool:
        """执行范围检测。

        参数：
            which_unit: 要检查的单位
            which_location: 目标位置
            distance: 检测距离

        返回：
            如果单位在范围内返回True，否则返回False
        """
        if which_unit is None or which_location is None:
            return False

        # 复用IsUnitInRangeXY的逻辑
        xy_checker = IsUnitInRangeXY()
        return xy_checker.execute(which_unit, which_location.x, which_location.y, distance)
```

**Step 4: 运行测试确认通过**

```bash
pytest tests/natives/test_unit_range_natives.py::TestIsUnitInRangeLoc -v
```

Expected: 3 tests PASSED

**Step 5: 注册到工厂并提交**

修改 `src/jass_runner/natives/factory.py`，添加：
```python
from src.jass_runner.natives.unit_range_natives import (
    IsUnitInRangeXY,
    IsUnitInRangeLoc,
)

# 在create_default_registry中添加:
registry.register(IsUnitInRangeLoc())
```

```bash
git add tests/natives/test_unit_range_natives.py src/jass_runner/natives/unit_range_natives.py src/jass_runner/natives/factory.py
git commit -m "feat: implement IsUnitInRangeLoc native function"
```

---

## Task 6: 实现IsUnitInRange

**Files:**
- Modify: `src/jass_runner/natives/unit_range_natives.py`
- Modify: `tests/natives/test_unit_range_natives.py`
- Modify: `src/jass_runner/natives/factory.py` (注册)

**Step 1: 编写IsUnitInRange测试**

在 `tests/natives/test_unit_range_natives.py` 添加：
```python
class TestIsUnitInRange:
    """测试IsUnitInRange函数。"""

    def test_unit_in_range_of_other_unit(self):
        """测试单位在另一单位范围内。"""
        from src.jass_runner.natives.unit_range_natives import IsUnitInRange
        native = IsUnitInRange()
        unit1 = Unit("Hpal", 0, 0.0, 0.0)
        unit2 = Unit("Hpal", 1, 50.0, 0.0)

        result = native.execute(unit1, unit2, 100.0)

        assert result is True

    def test_unit_out_of_range_of_other_unit(self):
        """测试单位在另一单位范围外。"""
        from src.jass_runner.natives.unit_range_natives import IsUnitInRange
        native = IsUnitInRange()
        unit1 = Unit("Hpal", 0, 0.0, 0.0)
        unit2 = Unit("Hpal", 1, 200.0, 0.0)

        result = native.execute(unit1, unit2, 100.0)

        assert result is False

    def test_null_other_unit_returns_false(self):
        """测试null其他单位返回False。"""
        from src.jass_runner.natives.unit_range_natives import IsUnitInRange
        native = IsUnitInRange()
        unit = Unit("Hpal", 0, 0.0, 0.0)

        result = native.execute(unit, None, 100.0)

        assert result is False
```

**Step 2: 运行测试确认失败**

```bash
pytest tests/natives/test_unit_range_natives.py::TestIsUnitInRange -v
```

Expected: FAIL

**Step 3: 实现IsUnitInRange**

在 `src/jass_runner/natives/unit_range_natives.py` 添加：
```python
class IsUnitInRange(NativeFunction):
    """检查单位是否在另一单位指定距离内。"""

    @property
    def name(self) -> str:
        return "IsUnitInRange"

    def execute(self, which_unit: Optional[Unit], other_unit: Optional[Unit], distance: float) -> bool:
        """执行范围检测。

        参数：
            which_unit: 要检查的单位
            other_unit: 目标单位
            distance: 检测距离

        返回：
            如果单位在范围内返回True，否则返回False
        """
        if which_unit is None or other_unit is None:
            return False

        # 复用IsUnitInRangeXY的逻辑
        xy_checker = IsUnitInRangeXY()
        return xy_checker.execute(which_unit, other_unit.x, other_unit.y, distance)
```

**Step 4: 运行测试确认通过**

```bash
pytest tests/natives/test_unit_range_natives.py::TestIsUnitInRange -v
```

Expected: 3 tests PASSED

**Step 5: 注册到工厂并提交**

修改 `src/jass_runner/natives/factory.py`，添加：
```python
from src.jass_runner.natives.unit_range_natives import (
    IsUnitInRangeXY,
    IsUnitInRangeLoc,
    IsUnitInRange,
)

# 在create_default_registry中添加:
registry.register(IsUnitInRange())
```

```bash
git add tests/natives/test_unit_range_natives.py src/jass_runner/natives/unit_range_natives.py src/jass_runner/natives/factory.py
git commit -m "feat: implement IsUnitInRange native function"
```

---

## Task 7: 实现SetUnitOwner

**Files:**
- Modify: `src/jass_runner/natives/unit_ownership_natives.py`
- Modify: `tests/natives/test_unit_ownership_natives.py`
- Modify: `src/jass_runner/natives/factory.py` (注册)

**Step 1: 编写SetUnitOwner测试**

在 `tests/natives/test_unit_ownership_natives.py` 添加：
```python
class TestSetUnitOwner:
    """测试SetUnitOwner函数。"""

    def test_set_unit_owner_changes_owner(self):
        """测试变更单位所有者。"""
        from src.jass_runner.natives.unit_ownership_natives import SetUnitOwner
        native = SetUnitOwner()
        unit = Unit("Hpal", 0, 0.0, 0.0)
        new_owner = Player(1)

        native.execute(unit, new_owner, False)

        assert unit.player_id == 1

    def test_set_unit_owner_with_change_color(self):
        """测试变更单位所有者并改变颜色。"""
        from src.jass_runner.natives.unit_ownership_natives import SetUnitOwner
        native = SetUnitOwner()
        unit = Unit("Hpal", 0, 0.0, 0.0)
        new_owner = Player(2)

        native.execute(unit, new_owner, True)

        assert unit.player_id == 2
        # changeColor为True时，单位颜色应改变（通过日志验证）

    def test_null_unit_does_nothing(self):
        """测试null单位不执行操作。"""
        from src.jass_runner.natives.unit_ownership_natives import SetUnitOwner
        native = SetUnitOwner()
        new_owner = Player(1)

        result = native.execute(None, new_owner, False)

        assert result is None

    def test_null_player_does_nothing(self):
        """测试null玩家不执行操作。"""
        from src.jass_runner.natives.unit_ownership_natives import SetUnitOwner
        native = SetUnitOwner()
        unit = Unit("Hpal", 0, 0.0, 0.0)

        result = native.execute(unit, None, False)

        assert result is None
        assert unit.player_id == 0  # 未改变
```

**Step 2: 运行测试确认失败**

```bash
pytest tests/natives/test_unit_ownership_natives.py::TestSetUnitOwner -v
```

Expected: FAIL

**Step 3: 实现SetUnitOwner**

在 `src/jass_runner/natives/unit_ownership_natives.py` 添加：
```python
class SetUnitOwner(NativeFunction):
    """设置单位所属玩家。"""

    @property
    def name(self) -> str:
        return "SetUnitOwner"

    def execute(self, which_unit: Optional[Unit], which_player: Optional[Player], change_color: bool) -> None:
        """执行单位所有权变更。

        参数：
            which_unit: 要变更所有者的单位
            which_player: 新所有者玩家
            change_color: 是否改变单位颜色
        """
        if which_unit is None or which_player is None:
            return

        old_owner = which_unit.player_id
        which_unit.player_id = which_player.player_id

        if change_color:
            # 改变单位颜色（通过颜色ID）
            which_unit.color = which_player.color
            logger.info(f"单位 {which_unit.name} (ID:{which_unit.id}) 所有权从玩家 {old_owner} 变更为玩家 {which_player.player_id} (颜色已改变)")
        else:
            logger.info(f"单位 {which_unit.name} (ID:{which_unit.id}) 所有权从玩家 {old_owner} 变更为玩家 {which_player.player_id}")
```

**Step 4: 运行测试确认通过**

```bash
pytest tests/natives/test_unit_ownership_natives.py::TestSetUnitOwner -v
```

Expected: 4 tests PASSED

**Step 5: 注册到工厂并提交**

修改 `src/jass_runner/natives/factory.py`，添加：
```python
from src.jass_runner.natives.unit_ownership_natives import (
    IsUnitOwnedByPlayer,
    SetUnitOwner,
)

# 在create_default_registry中添加:
registry.register(SetUnitOwner())
```

```bash
git add tests/natives/test_unit_ownership_natives.py src/jass_runner/natives/unit_ownership_natives.py src/jass_runner/natives/factory.py
git commit -m "feat: implement SetUnitOwner native function"
```

---

## Task 8: 实现IsUnitAlly和IsUnitEnemy

**Files:**
- Modify: `src/jass_runner/natives/unit_ownership_natives.py`
- Modify: `tests/natives/test_unit_ownership_natives.py`
- Modify: `src/jass_runner/natives/factory.py` (注册)

**Step 1: 编写IsUnitAlly和IsUnitEnemy测试**

在 `tests/natives/test_unit_ownership_natives.py` 添加：
```python
from src.jass_runner.natives.manager import HandleManager


class TestIsUnitAlly:
    """测试IsUnitAlly函数。"""

    def test_unit_is_ally_returns_true(self):
        """测试单位所属玩家与指定玩家是盟友。"""
        from src.jass_runner.natives.unit_ownership_natives import IsUnitAlly
        native = IsUnitAlly()
        manager = HandleManager()

        unit = Unit("Hpal", 0, 0.0, 0.0)
        unit_owner = manager.get_player_by_id(0)
        other_player = manager.get_player_by_id(1)

        # 设置盟友关系
        unit_owner.set_alliance(1, True)

        result = native.execute(unit, other_player, state_context=manager)

        assert result is True

    def test_unit_is_not_ally_returns_false(self):
        """测试单位所属玩家与指定玩家不是盟友。"""
        from src.jass_runner.natives.unit_ownership_natives import IsUnitAlly
        native = IsUnitAlly()
        manager = HandleManager()

        unit = Unit("Hpal", 0, 0.0, 0.0)
        other_player = manager.get_player_by_id(1)

        result = native.execute(unit, other_player, state_context=manager)

        assert result is False

    def test_null_unit_returns_false(self):
        """测试null单位返回False。"""
        from src.jass_runner.natives.unit_ownership_natives import IsUnitAlly
        native = IsUnitAlly()
        manager = HandleManager()
        other_player = manager.get_player_by_id(1)

        result = native.execute(None, other_player, state_context=manager)

        assert result is False


class TestIsUnitEnemy:
    """测试IsUnitEnemy函数。"""

    def test_unit_is_enemy_returns_true(self):
        """测试单位所属玩家与指定玩家是敌人。"""
        from src.jass_runner.natives.unit_ownership_natives import IsUnitEnemy
        native = IsUnitEnemy()
        manager = HandleManager()

        unit = Unit("Hpal", 0, 0.0, 0.0)
        unit_owner = manager.get_player_by_id(0)
        other_player = manager.get_player_by_id(1)

        # 设置敌对关系
        unit_owner.set_alliance(1, False)

        result = native.execute(unit, other_player, state_context=manager)

        assert result is True

    def test_unit_is_not_enemy_returns_false(self):
        """测试单位所属玩家与指定玩家不是敌人。"""
        from src.jass_runner.natives.unit_ownership_natives import IsUnitEnemy
        native = IsUnitEnemy()
        manager = HandleManager()

        unit = Unit("Hpal", 0, 0.0, 0.0)
        other_player = manager.get_player_by_id(1)

        result = native.execute(unit, other_player, state_context=manager)

        assert result is False
```

**Step 2: 运行测试确认失败**

```bash
pytest tests/natives/test_unit_ownership_natives.py::TestIsUnitAlly -v
```

Expected: FAIL

**Step 3: 实现IsUnitAlly和IsUnitEnemy**

在 `src/jass_runner/natives/unit_ownership_natives.py` 添加：
```python
from src.jass_runner.natives.manager import HandleManager


class IsUnitAlly(NativeFunction):
    """检查单位所属玩家与指定玩家是否盟友。"""

    @property
    def name(self) -> str:
        return "IsUnitAlly"

    def execute(self, which_unit: Optional[Unit], which_player: Optional[Player], state_context: Optional[HandleManager] = None) -> bool:
        """执行盟友关系检查。

        参数：
            which_unit: 要检查的单位
            which_player: 要检查的玩家
            state_context: 状态上下文（HandleManager）

        返回：
            如果单位所属玩家与指定玩家是盟友返回True
        """
        if which_unit is None or which_player is None:
            return False

        if state_context is None:
            return False

        # 获取单位所属玩家对象
        unit_owner = state_context.get_player_by_id(which_unit.player_id)
        if unit_owner is None:
            return False

        return unit_owner.is_ally(which_player.player_id)


class IsUnitEnemy(NativeFunction):
    """检查单位所属玩家与指定玩家是否敌对。"""

    @property
    def name(self) -> str:
        return "IsUnitEnemy"

    def execute(self, which_unit: Optional[Unit], which_player: Optional[Player], state_context: Optional[HandleManager] = None) -> bool:
        """执行敌对关系检查。

        参数：
            which_unit: 要检查的单位
            which_player: 要检查的玩家
            state_context: 状态上下文（HandleManager）

        返回：
            如果单位所属玩家与指定玩家是敌人返回True
        """
        if which_unit is None or which_player is None:
            return False

        if state_context is None:
            return False

        # 获取单位所属玩家对象
        unit_owner = state_context.get_player_by_id(which_unit.player_id)
        if unit_owner is None:
            return False

        return unit_owner.is_enemy(which_player.player_id)
```

**Step 4: 运行测试确认通过**

```bash
pytest tests/natives/test_unit_ownership_natives.py::TestIsUnitAlly tests/natives/test_unit_ownership_natives.py::TestIsUnitEnemy -v
```

Expected: 5 tests PASSED

**Step 5: 注册到工厂并提交**

修改 `src/jass_runner/natives/factory.py`，添加：
```python
from src.jass_runner.natives.unit_ownership_natives import (
    IsUnitOwnedByPlayer,
    SetUnitOwner,
    IsUnitAlly,
    IsUnitEnemy,
)

# 在create_default_registry中添加:
registry.register(IsUnitAlly())
registry.register(IsUnitEnemy())
```

```bash
git add tests/natives/test_unit_ownership_natives.py src/jass_runner/natives/unit_ownership_natives.py src/jass_runner/natives/factory.py
git commit -m "feat: implement IsUnitAlly and IsUnitEnemy native functions"
```

---

## Task 9: 创建集成测试

**Files:**
- Create: `tests/integration/test_unit_ownership_integration.py`

**Step 1: 编写集成测试**

创建 `tests/integration/test_unit_ownership_integration.py`:
```python
"""单位所有权Native函数集成测试。"""

import pytest
from src.jass_runner.handles.unit import Unit
from src.jass_runner.handles.player import Player
from src.jass_runner.handles.location import Location
from src.jass_runner.natives.manager import HandleManager
from src.jass_runner.natives.unit_ownership_natives import (
    IsUnitOwnedByPlayer,
    SetUnitOwner,
    IsUnitAlly,
    IsUnitEnemy,
)
from src.jass_runner.natives.unit_range_natives import (
    IsUnitInRange,
    IsUnitInRangeXY,
    IsUnitInRangeLoc,
)


class TestUnitOwnershipWorkflow:
    """测试单位所有权完整工作流程。"""

    def test_complete_ownership_transfer(self):
        """测试完整的单位所有权转移流程。"""
        manager = HandleManager()
        set_owner = SetUnitOwner()
        is_owned = IsUnitOwnedByPlayer()

        # 创建单位和玩家
        unit = Unit("Hpal", 0, 0.0, 0.0)
        player0 = Player(0)
        player1 = Player(1)

        # 初始属于玩家0
        assert is_owned.execute(unit, player0) is True
        assert is_owned.execute(unit, player1) is False

        # 转移所有权
        set_owner.execute(unit, player1, False)

        # 现在属于玩家1
        assert is_owned.execute(unit, player0) is False
        assert is_owned.execute(unit, player1) is True

    def test_ally_and_enemy_detection(self):
        """测试盟友和敌人检测。"""
        manager = HandleManager()
        is_ally = IsUnitAlly()
        is_enemy = IsUnitEnemy()

        unit = Unit("Hpal", 0, 0.0, 0.0)
        player1 = manager.get_player_by_id(1)

        # 初始无关系
        assert is_ally.execute(unit, player1, state_context=manager) is False
        assert is_enemy.execute(unit, player1, state_context=manager) is False

        # 设置为盟友
        unit_owner = manager.get_player_by_id(0)
        unit_owner.set_alliance(1, True)

        assert is_ally.execute(unit, player1, state_context=manager) is True
        assert is_enemy.execute(unit, player1, state_context=manager) is False

        # 改为敌人
        unit_owner.set_alliance(1, False)

        assert is_ally.execute(unit, player1, state_context=manager) is False
        assert is_enemy.execute(unit, player1, state_context=manager) is True


class TestUnitRangeDetectionWorkflow:
    """测试单位范围检测完整工作流程。"""

    def test_range_detection_between_units(self):
        """测试单位间范围检测。"""
        is_in_range = IsUnitInRange()

        unit1 = Unit("Hpal", 0, 0.0, 0.0)
        unit2 = Unit("Hpal", 1, 50.0, 0.0)

        assert is_in_range.execute(unit1, unit2, 100.0) is True
        assert is_in_range.execute(unit1, unit2, 40.0) is False

    def test_range_detection_with_coordinates(self):
        """测试坐标范围检测。"""
        is_in_range_xy = IsUnitInRangeXY()

        unit = Unit("Hpal", 0, 30.0, 40.0)  # 距离(0,0)为50

        assert is_in_range_xy.execute(unit, 0.0, 0.0, 50.0) is True
        assert is_in_range_xy.execute(unit, 0.0, 0.0, 49.9) is False

    def test_range_detection_with_location(self):
        """测试位置范围检测。"""
        is_in_range_loc = IsUnitInRangeLoc()

        unit = Unit("Hpal", 0, 30.0, 40.0)
        loc = Location(0.0, 0.0)

        assert is_in_range_loc.execute(unit, loc, 50.0) is True
        assert is_in_range_loc.execute(unit, loc, 49.9) is False
```

**Step 2: 运行集成测试**

```bash
pytest tests/integration/test_unit_ownership_integration.py -v
```

Expected: 6 tests PASSED

**Step 3: 提交**

```bash
git add tests/integration/test_unit_ownership_integration.py
git commit -m "test: add unit ownership and range detection integration tests"
```

---

## Task 10: 更新Native函数计数和文档

**Files:**
- Modify: `tests/natives/test_factory.py` (更新计数)
- Modify: `TODO.md` (标记完成)

**Step 1: 更新工厂测试计数**

修改 `tests/natives/test_factory.py` 中的计数：
```python
# 从85改为92（新增7个函数）
assert len(natives) == 92
```

**Step 2: 运行工厂测试**

```bash
pytest tests/natives/test_factory.py -v
```

Expected: PASS

**Step 3: 更新TODO.md**

在 `TODO.md` 中标记第五批完成：
```markdown
- [x] 第五批：单位所有权和关系（SetUnitOwner, IsUnitOwnedByPlayer, IsUnitAlly, IsUnitEnemy, IsUnitInRange系列）✅ 已完成
```

**Step 4: 提交**

```bash
git add tests/natives/test_factory.py TODO.md
git commit -m "docs: update native function count and mark fifth batch as completed"
```

---

## Task 11: 运行完整测试套件

**Step 1: 运行所有测试**

```bash
pytest tests/ -v --tb=short
```

Expected: 所有测试通过（新增约30个测试）

**Step 2: 最终提交**

```bash
# 如有未提交的更改
git add -A
git commit -m "feat: complete fifth batch of unit ownership and range natives"
```

---

## 总结

本计划实现7个Native函数：

1. **Player类扩展**: 添加盟友/敌对关系管理
2. **HandleManager扩展**: 添加玩家查询方法
3. **IsUnitOwnedByPlayer**: 检查单位所有权
4. **IsUnitInRangeXY**: 坐标范围检测
5. **IsUnitInRangeLoc**: 位置范围检测
6. **IsUnitInRange**: 单位间范围检测
7. **SetUnitOwner**: 变更单位所有权
8. **IsUnitAlly/IsUnitEnemy**: 盟友/敌人检测
9. **集成测试**: 完整工作流程验证

**新增文件**:
- `src/jass_runner/natives/unit_ownership_natives.py`
- `src/jass_runner/natives/unit_range_natives.py`
- `tests/handles/test_player.py`
- `tests/natives/test_unit_ownership_natives.py`
- `tests/natives/test_unit_range_natives.py`
- `tests/integration/test_unit_ownership_integration.py`

**修改文件**:
- `src/jass_runner/handles/player.py`
- `src/jass_runner/natives/manager.py`
- `src/jass_runner/natives/factory.py`
- `tests/natives/test_factory.py`
- `TODO.md`
