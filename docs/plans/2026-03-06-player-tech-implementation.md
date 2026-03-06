# 玩家科技Native函数实施计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 实现6个玩家科技相关的native函数（SetPlayerTechMaxAllowed, GetPlayerTechMaxAllowed, AddPlayerTechResearched, SetPlayerTechResearched, GetPlayerTechResearched, GetPlayerTechCount）

**Architecture:** 在Player类中添加两个字典存储科技状态（_tech_max_allowed和_tech_researched），新建player_tech_natives.py实现6个native函数类，遵循TDD方法逐步开发

**Tech Stack:** Python 3.8+, pytest, 项目现有的NativeFunction框架

---

## 前置检查

**检查1: 确认Player类位置**
- 文件: `src/jass_runner/natives/player.py`
- 确认存在Player类，有`_gold`, `_lumber`等属性

**检查2: 确认NativeFunction基类**
- 文件: `src/jass_runner/natives/base.py`
- 确认存在NativeFunction抽象基类

**检查3: 确认Factory注册方式**
- 文件: `src/jass_runner/natives/factory.py`
- 查看现有函数如何注册

---

## Task 1: 修改Player类添加科技状态存储

**Files:**
- Modify: `src/jass_runner/natives/player.py:49`（在__init__方法末尾添加）

**Step 1: 编写Player类测试**

创建测试文件 `tests/natives/test_player_tech.py`：

```python
"""玩家科技功能测试。"""

import pytest
from src.jass_runner.natives.player import Player


class TestPlayerTech:
    """测试Player类的科技功能。"""

    def test_set_and_get_tech_max_allowed(self):
        """测试设置和获取科技最大允许等级。"""
        player = Player("test_handle", 0)
        tech_id = 1214542384  # 'Hpal'的FourCC值

        player.set_tech_max_allowed(tech_id, 5)
        assert player.get_tech_max_allowed(tech_id) == 5

    def test_get_tech_max_allowed_default(self):
        """测试获取未设置的科技最大允许等级返回0。"""
        player = Player("test_handle", 0)
        tech_id = 1214542384

        assert player.get_tech_max_allowed(tech_id) == 0

    def test_set_and_get_tech_researched(self):
        """测试设置和获取科技研究等级。"""
        player = Player("test_handle", 0)
        tech_id = 1214542384

        player.set_tech_researched(tech_id, 3)
        assert player.get_tech_researched(tech_id, False) is True
        assert player.get_tech_count(tech_id, False) == 3

    def test_add_tech_researched(self):
        """测试增加科技研究等级。"""
        player = Player("test_handle", 0)
        tech_id = 1214542384

        player.set_tech_researched(tech_id, 1)
        player.add_tech_researched(tech_id, 2)
        assert player.get_tech_count(tech_id, False) == 3

    def test_get_tech_researched_false(self):
        """测试未研究的科技返回False。"""
        player = Player("test_handle", 0)
        tech_id = 1214542384

        assert player.get_tech_researched(tech_id, False) is False

    def test_get_tech_count_default(self):
        """测试获取未设置的科技等级返回0。"""
        player = Player("test_handle", 0)
        tech_id = 1214542384

        assert player.get_tech_count(tech_id, False) == 0
```

**Step 2: 运行测试验证失败**

```bash
pytest tests/natives/test_player_tech.py -v
```

Expected: FAIL with "AttributeError: 'Player' object has no attribute 'set_tech_max_allowed'"

**Step 3: 修改Player类添加科技状态**

在 `src/jass_runner/natives/player.py` 的 `__init__` 方法末尾（第49行后）添加：

```python
        # 科技系统
        self._tech_max_allowed: Dict[int, int] = {}  # techid -> 最大允许等级
        self._tech_researched: Dict[int, int] = {}   # techid -> 当前研究等级
```

在类末尾添加方法：

```python
    def set_tech_max_allowed(self, techid: int, maximum: int) -> None:
        """设置科技最大允许等级。

        参数：
            techid: 科技ID（FourCC格式）
            maximum: 最大允许等级
        """
        self._tech_max_allowed[techid] = maximum

    def get_tech_max_allowed(self, techid: int) -> int:
        """获取科技最大允许等级。

        参数：
            techid: 科技ID（FourCC格式）

        返回：
            最大允许等级，未设置返回0
        """
        return self._tech_max_allowed.get(techid, 0)

    def add_tech_researched(self, techid: int, levels: int) -> None:
        """增加科技研究等级。

        参数：
            techid: 科技ID（FourCC格式）
            levels: 要增加的等级数
        """
        current = self._tech_researched.get(techid, 0)
        self._tech_researched[techid] = current + levels

    def set_tech_researched(self, techid: int, level: int) -> None:
        """设置科技研究等级。

        参数：
            techid: 科技ID（FourCC格式）
            level: 要设置的等级
        """
        self._tech_researched[techid] = level

    def get_tech_researched(self, techid: int, specificonly: bool) -> bool:
        """获取科技是否已研究。

        参数：
            techid: 科技ID（FourCC格式）
            specificonly: 是否只检查特定科技（当前忽略）

        返回：
            等级大于0返回True，否则返回False
        """
        return self._tech_researched.get(techid, 0) > 0

    def get_tech_count(self, techid: int, specificonly: bool) -> int:
        """获取科技当前研究等级。

        参数：
            techid: 科技ID（FourCC格式）
            specificonly: 是否只检查特定科技（当前忽略）

        返回：
            当前研究等级，未设置返回0
        """
        return self._tech_researched.get(techid, 0)
```

**Step 4: 运行测试验证通过**

```bash
pytest tests/natives/test_player_tech.py -v
```

Expected: 6个测试全部PASS

**Step 5: 提交**

```bash
git add src/jass_runner/natives/player.py tests/natives/test_player_tech.py
git commit -m "feat(player): 添加玩家科技状态存储和管理方法"
```

---

## Task 2: 实现SetPlayerTechMaxAllowed Native函数

**Files:**
- Create: `src/jass_runner/natives/player_tech_natives.py`
- Test: `tests/natives/test_player_tech_natives.py`

**Step 1: 编写测试**

创建 `tests/natives/test_player_tech_natives.py`：

```python
"""玩家科技Native函数测试。"""

import pytest
from unittest.mock import MagicMock
from src.jass_runner.natives.player_tech_natives import SetPlayerTechMaxAllowed
from src.jass_runner.natives.player import Player


class TestSetPlayerTechMaxAllowed:
    """测试SetPlayerTechMaxAllowed native函数。"""

    def test_set_player_tech_max_allowed(self):
        """测试设置玩家科技最大允许等级。"""
        native = SetPlayerTechMaxAllowed()
        state_context = MagicMock()
        player = Player("test_handle", 0)
        tech_id = 1214542384  # 'Hpal'

        result = native.execute(state_context, player, tech_id, 5)
        assert result is None
        assert player.get_tech_max_allowed(tech_id) == 5

    def test_set_player_tech_max_allowed_none_player(self):
        """测试player为None时的处理。"""
        native = SetPlayerTechMaxAllowed()
        state_context = MagicMock()

        result = native.execute(state_context, None, 1214542384, 5)
        assert result is None
```

**Step 2: 运行测试验证失败**

```bash
pytest tests/natives/test_player_tech_natives.py::TestSetPlayerTechMaxAllowed -v
```

Expected: FAIL with "ModuleNotFoundError: No module named 'src.jass_runner.natives.player_tech_natives'"

**Step 3: 实现SetPlayerTechMaxAllowed**

创建 `src/jass_runner/natives/player_tech_natives.py`：

```python
"""玩家科技相关native函数实现。

此模块包含与玩家科技系统相关的JASS native函数。
"""

import logging
from typing import TYPE_CHECKING

from .base import NativeFunction

if TYPE_CHECKING:
    from .state import StateContext
    from .handle import Player

logger = logging.getLogger(__name__)


class SetPlayerTechMaxAllowed(NativeFunction):
    """设置玩家科技最大允许等级。"""

    @property
    def name(self) -> str:
        """获取native函数名称。

        返回：
            函数名称 "SetPlayerTechMaxAllowed"
        """
        return "SetPlayerTechMaxAllowed"

    def execute(self, state_context: 'StateContext', whichPlayer: 'Player',
                techid: int, maximum: int) -> None:
        """执行SetPlayerTechMaxAllowed native函数。

        参数：
            state_context: 状态上下文
            whichPlayer: 玩家对象
            techid: 科技ID（FourCC格式）
            maximum: 最大允许等级
        """
        if whichPlayer is None:
            logger.warning("[SetPlayerTechMaxAllowed] 玩家对象为None")
            return None

        whichPlayer.set_tech_max_allowed(techid, maximum)
        logger.info(f"[SetPlayerTechMaxAllowed] 玩家{whichPlayer.player_id} 科技{techid} 最大等级设为{maximum}")
        return None
```

**Step 4: 运行测试验证通过**

```bash
pytest tests/natives/test_player_tech_natives.py::TestSetPlayerTechMaxAllowed -v
```

Expected: 2个测试全部PASS

**Step 5: 提交**

```bash
git add src/jass_runner/natives/player_tech_natives.py tests/natives/test_player_tech_natives.py
git commit -m "feat(natives): 实现SetPlayerTechMaxAllowed native函数"
```

---

## Task 3: 实现GetPlayerTechMaxAllowed Native函数

**Files:**
- Modify: `src/jass_runner/natives/player_tech_natives.py`（在SetPlayerTechMaxAllowed后添加）
- Test: `tests/natives/test_player_tech_natives.py`

**Step 1: 编写测试**

在 `tests/natives/test_player_tech_natives.py` 中添加：

```python

class TestGetPlayerTechMaxAllowed:
    """测试GetPlayerTechMaxAllowed native函数。"""

    def test_get_player_tech_max_allowed(self):
        """测试获取玩家科技最大允许等级。"""
        native = GetPlayerTechMaxAllowed()
        state_context = MagicMock()
        player = Player("test_handle", 0)
        tech_id = 1214542384

        player.set_tech_max_allowed(tech_id, 5)
        result = native.execute(state_context, player, tech_id)
        assert result == 5

    def test_get_player_tech_max_allowed_default(self):
        """测试获取未设置的科技最大允许等级返回0。"""
        native = GetPlayerTechMaxAllowed()
        state_context = MagicMock()
        player = Player("test_handle", 0)
        tech_id = 1214542384

        result = native.execute(state_context, player, tech_id)
        assert result == 0

    def test_get_player_tech_max_allowed_none_player(self):
        """测试player为None时返回0。"""
        native = GetPlayerTechMaxAllowed()
        state_context = MagicMock()

        result = native.execute(state_context, None, 1214542384)
        assert result == 0
```

**Step 2: 运行测试验证失败**

```bash
pytest tests/natives/test_player_tech_natives.py::TestGetPlayerTechMaxAllowed -v
```

Expected: FAIL with "NameError: name 'GetPlayerTechMaxAllowed' is not defined"

**Step 3: 实现GetPlayerTechMaxAllowed**

在 `src/jass_runner/natives/player_tech_natives.py` 中添加：

```python

class GetPlayerTechMaxAllowed(NativeFunction):
    """获取玩家科技最大允许等级。"""

    @property
    def name(self) -> str:
        """获取native函数名称。

        返回：
            函数名称 "GetPlayerTechMaxAllowed"
        """
        return "GetPlayerTechMaxAllowed"

    def execute(self, state_context: 'StateContext', whichPlayer: 'Player',
                techid: int) -> int:
        """执行GetPlayerTechMaxAllowed native函数。

        参数：
            state_context: 状态上下文
            whichPlayer: 玩家对象
            techid: 科技ID（FourCC格式）

        返回：
            最大允许等级，未设置或玩家为None返回0
        """
        if whichPlayer is None:
            logger.warning("[GetPlayerTechMaxAllowed] 玩家对象为None")
            return 0

        result = whichPlayer.get_tech_max_allowed(techid)
        logger.info(f"[GetPlayerTechMaxAllowed] 玩家{whichPlayer.player_id} 科技{techid} 最大等级为{result}")
        return result
```

**Step 4: 运行测试验证通过**

```bash
pytest tests/natives/test_player_tech_natives.py::TestGetPlayerTechMaxAllowed -v
```

Expected: 3个测试全部PASS

**Step 5: 提交**

```bash
git add src/jass_runner/natives/player_tech_natives.py tests/natives/test_player_tech_natives.py
git commit -m "feat(natives): 实现GetPlayerTechMaxAllowed native函数"
```

---

## Task 4: 实现AddPlayerTechResearched Native函数

**Files:**
- Modify: `src/jass_runner/natives/player_tech_natives.py`
- Test: `tests/natives/test_player_tech_natives.py`

**Step 1: 编写测试**

在 `tests/natives/test_player_tech_natives.py` 中添加：

```python

class TestAddPlayerTechResearched:
    """测试AddPlayerTechResearched native函数。"""

    def test_add_player_tech_researched(self):
        """测试增加玩家科技研究等级。"""
        native = AddPlayerTechResearched()
        state_context = MagicMock()
        player = Player("test_handle", 0)
        tech_id = 1214542384

        player.set_tech_researched(tech_id, 1)
        result = native.execute(state_context, player, tech_id, 2)
        assert result is None
        assert player.get_tech_count(tech_id, False) == 3

    def test_add_player_tech_researched_none_player(self):
        """测试player为None时的处理。"""
        native = AddPlayerTechResearched()
        state_context = MagicMock()

        result = native.execute(state_context, None, 1214542384, 2)
        assert result is None
```

**Step 2: 运行测试验证失败**

```bash
pytest tests/natives/test_player_tech_natives.py::TestAddPlayerTechResearched -v
```

Expected: FAIL with "NameError: name 'AddPlayerTechResearched' is not defined"

**Step 3: 实现AddPlayerTechResearched**

在 `src/jass_runner/natives/player_tech_natives.py` 中添加：

```python

class AddPlayerTechResearched(NativeFunction):
    """增加玩家科技研究等级。"""

    @property
    def name(self) -> str:
        """获取native函数名称。

        返回：
            函数名称 "AddPlayerTechResearched"
        """
        return "AddPlayerTechResearched"

    def execute(self, state_context: 'StateContext', whichPlayer: 'Player',
                techid: int, levels: int) -> None:
        """执行AddPlayerTechResearched native函数。

        参数：
            state_context: 状态上下文
            whichPlayer: 玩家对象
            techid: 科技ID（FourCC格式）
            levels: 要增加的等级数
        """
        if whichPlayer is None:
            logger.warning("[AddPlayerTechResearched] 玩家对象为None")
            return None

        whichPlayer.add_tech_researched(techid, levels)
        new_level = whichPlayer.get_tech_count(techid, False)
        logger.info(f"[AddPlayerTechResearched] 玩家{whichPlayer.player_id} 科技{techid} 增加{levels}级，当前等级{new_level}")
        return None
```

**Step 4: 运行测试验证通过**

```bash
pytest tests/natives/test_player_tech_natives.py::TestAddPlayerTechResearched -v
```

Expected: 2个测试全部PASS

**Step 5: 提交**

```bash
git add src/jass_runner/natives/player_tech_natives.py tests/natives/test_player_tech_natives.py
git commit -m "feat(natives): 实现AddPlayerTechResearched native函数"
```

---

## Task 5: 实现SetPlayerTechResearched Native函数

**Files:**
- Modify: `src/jass_runner/natives/player_tech_natives.py`
- Test: `tests/natives/test_player_tech_natives.py`

**Step 1: 编写测试**

在 `tests/natives/test_player_tech_natives.py` 中添加：

```python

class TestSetPlayerTechResearched:
    """测试SetPlayerTechResearched native函数。"""

    def test_set_player_tech_researched(self):
        """测试设置玩家科技研究等级。"""
        native = SetPlayerTechResearched()
        state_context = MagicMock()
        player = Player("test_handle", 0)
        tech_id = 1214542384

        result = native.execute(state_context, player, tech_id, 5)
        assert result is None
        assert player.get_tech_count(tech_id, False) == 5

    def test_set_player_tech_researched_none_player(self):
        """测试player为None时的处理。"""
        native = SetPlayerTechResearched()
        state_context = MagicMock()

        result = native.execute(state_context, None, 1214542384, 5)
        assert result is None
```

**Step 2: 运行测试验证失败**

```bash
pytest tests/natives/test_player_tech_natives.py::TestSetPlayerTechResearched -v
```

Expected: FAIL with "NameError: name 'SetPlayerTechResearched' is not defined"

**Step 3: 实现SetPlayerTechResearched**

在 `src/jass_runner/natives/player_tech_natives.py` 中添加：

```python

class SetPlayerTechResearched(NativeFunction):
    """设置玩家科技研究等级。"""

    @property
    def name(self) -> str:
        """获取native函数名称。

        返回：
            函数名称 "SetPlayerTechResearched"
        """
        return "SetPlayerTechResearched"

    def execute(self, state_context: 'StateContext', whichPlayer: 'Player',
                techid: int, setToLevel: int) -> None:
        """执行SetPlayerTechResearched native函数。

        参数：
            state_context: 状态上下文
            whichPlayer: 玩家对象
            techid: 科技ID（FourCC格式）
            setToLevel: 要设置的等级
        """
        if whichPlayer is None:
            logger.warning("[SetPlayerTechResearched] 玩家对象为None")
            return None

        whichPlayer.set_tech_researched(techid, setToLevel)
        logger.info(f"[SetPlayerTechResearched] 玩家{whichPlayer.player_id} 科技{techid} 等级设为{setToLevel}")
        return None
```

**Step 4: 运行测试验证通过**

```bash
pytest tests/natives/test_player_tech_natives.py::TestSetPlayerTechResearched -v
```

Expected: 2个测试全部PASS

**Step 5: 提交**

```bash
git add src/jass_runner/natives/player_tech_natives.py tests/natives/test_player_tech_natives.py
git commit -m "feat(natives): 实现SetPlayerTechResearched native函数"
```

---

## Task 6: 实现GetPlayerTechResearched Native函数

**Files:**
- Modify: `src/jass_runner/natives/player_tech_natives.py`
- Test: `tests/natives/test_player_tech_natives.py`

**Step 1: 编写测试**

在 `tests/natives/test_player_tech_natives.py` 中添加：

```python

class TestGetPlayerTechResearched:
    """测试GetPlayerTechResearched native函数。"""

    def test_get_player_tech_researched_true(self):
        """测试获取已研究的科技返回True。"""
        native = GetPlayerTechResearched()
        state_context = MagicMock()
        player = Player("test_handle", 0)
        tech_id = 1214542384

        player.set_tech_researched(tech_id, 3)
        result = native.execute(state_context, player, tech_id, False)
        assert result is True

    def test_get_player_tech_researched_false(self):
        """测试获取未研究的科技返回False。"""
        native = GetPlayerTechResearched()
        state_context = MagicMock()
        player = Player("test_handle", 0)
        tech_id = 1214542384

        result = native.execute(state_context, player, tech_id, False)
        assert result is False

    def test_get_player_tech_researched_zero_level(self):
        """测试等级为0时返回False。"""
        native = GetPlayerTechResearched()
        state_context = MagicMock()
        player = Player("test_handle", 0)
        tech_id = 1214542384

        player.set_tech_researched(tech_id, 0)
        result = native.execute(state_context, player, tech_id, False)
        assert result is False

    def test_get_player_tech_researched_none_player(self):
        """测试player为None时返回False。"""
        native = GetPlayerTechResearched()
        state_context = MagicMock()

        result = native.execute(state_context, None, 1214542384, False)
        assert result is False
```

**Step 2: 运行测试验证失败**

```bash
pytest tests/natives/test_player_tech_natives.py::TestGetPlayerTechResearched -v
```

Expected: FAIL with "NameError: name 'GetPlayerTechResearched' is not defined"

**Step 3: 实现GetPlayerTechResearched**

在 `src/jass_runner/natives/player_tech_natives.py` 中添加：

```python

class GetPlayerTechResearched(NativeFunction):
    """获取玩家科技是否已研究。"""

    @property
    def name(self) -> str:
        """获取native函数名称。

        返回：
            函数名称 "GetPlayerTechResearched"
        """
        return "GetPlayerTechResearched"

    def execute(self, state_context: 'StateContext', whichPlayer: 'Player',
                techid: int, specificonly: bool) -> bool:
        """执行GetPlayerTechResearched native函数。

        参数：
            state_context: 状态上下文
            whichPlayer: 玩家对象
            techid: 科技ID（FourCC格式）
            specificonly: 是否只检查特定科技（当前忽略）

        返回：
            等级大于0返回True，否则返回False
        """
        if whichPlayer is None:
            logger.warning("[GetPlayerTechResearched] 玩家对象为None")
            return False

        result = whichPlayer.get_tech_researched(techid, specificonly)
        logger.info(f"[GetPlayerTechResearched] 玩家{whichPlayer.player_id} 科技{techid} 已研究: {result}")
        return result
```

**Step 4: 运行测试验证通过**

```bash
pytest tests/natives/test_player_tech_natives.py::TestGetPlayerTechResearched -v
```

Expected: 4个测试全部PASS

**Step 5: 提交**

```bash
git add src/jass_runner/natives/player_tech_natives.py tests/natives/test_player_tech_natives.py
git commit -m "feat(natives): 实现GetPlayerTechResearched native函数"
```

---

## Task 7: 实现GetPlayerTechCount Native函数

**Files:**
- Modify: `src/jass_runner/natives/player_tech_natives.py`
- Test: `tests/natives/test_player_tech_natives.py`

**Step 1: 编写测试**

在 `tests/natives/test_player_tech_natives.py` 中添加：

```python

class TestGetPlayerTechCount:
    """测试GetPlayerTechCount native函数。"""

    def test_get_player_tech_count(self):
        """测试获取玩家科技研究等级。"""
        native = GetPlayerTechCount()
        state_context = MagicMock()
        player = Player("test_handle", 0)
        tech_id = 1214542384

        player.set_tech_researched(tech_id, 5)
        result = native.execute(state_context, player, tech_id, False)
        assert result == 5

    def test_get_player_tech_count_default(self):
        """测试获取未设置的科技等级返回0。"""
        native = GetPlayerTechCount()
        state_context = MagicMock()
        player = Player("test_handle", 0)
        tech_id = 1214542384

        result = native.execute(state_context, player, tech_id, False)
        assert result == 0

    def test_get_player_tech_count_none_player(self):
        """测试player为None时返回0。"""
        native = GetPlayerTechCount()
        state_context = MagicMock()

        result = native.execute(state_context, None, 1214542384, False)
        assert result == 0
```

**Step 2: 运行测试验证失败**

```bash
pytest tests/natives/test_player_tech_natives.py::TestGetPlayerTechCount -v
```

Expected: FAIL with "NameError: name 'GetPlayerTechCount' is not defined"

**Step 3: 实现GetPlayerTechCount**

在 `src/jass_runner/natives/player_tech_natives.py` 中添加：

```python

class GetPlayerTechCount(NativeFunction):
    """获取玩家科技研究等级。"""

    @property
    def name(self) -> str:
        """获取native函数名称。

        返回：
            函数名称 "GetPlayerTechCount"
        """
        return "GetPlayerTechCount"

    def execute(self, state_context: 'StateContext', whichPlayer: 'Player',
                techid: int, specificonly: bool) -> int:
        """执行GetPlayerTechCount native函数。

        参数：
            state_context: 状态上下文
            whichPlayer: 玩家对象
            techid: 科技ID（FourCC格式）
            specificonly: 是否只检查特定科技（当前忽略）

        返回：
            当前研究等级，未设置或玩家为None返回0
        """
        if whichPlayer is None:
            logger.warning("[GetPlayerTechCount] 玩家对象为None")
            return 0

        result = whichPlayer.get_tech_count(techid, specificonly)
        logger.info(f"[GetPlayerTechCount] 玩家{whichPlayer.player_id} 科技{techid} 等级为{result}")
        return result
```

**Step 4: 运行测试验证通过**

```bash
pytest tests/natives/test_player_tech_natives.py::TestGetPlayerTechCount -v
```

Expected: 3个测试全部PASS

**Step 5: 提交**

```bash
git add src/jass_runner/natives/player_tech_natives.py tests/natives/test_player_tech_natives.py
git commit -m "feat(natives): 实现GetPlayerTechCount native函数"
```

---

## Task 8: 在NativeFactory中注册所有函数

**Files:**
- Modify: `src/jass_runner/natives/factory.py`
- Modify: `src/jass_runner/natives/__init__.py`
- Test: `tests/natives/test_factory.py`

**Step 1: 更新__init__.py导出**

在 `src/jass_runner/natives/__init__.py` 中添加导出：

```python
from .player_tech_natives import (
    SetPlayerTechMaxAllowed,
    GetPlayerTechMaxAllowed,
    AddPlayerTechResearched,
    SetPlayerTechResearched,
    GetPlayerTechResearched,
    GetPlayerTechCount,
)
```

**Step 2: 在Factory中注册**

在 `src/jass_runner/natives/factory.py` 的 `create_default_registry` 方法中添加：

```python
from .player_tech_natives import (
    SetPlayerTechMaxAllowed,
    GetPlayerTechMaxAllowed,
    AddPlayerTechResearched,
    SetPlayerTechResearched,
    GetPlayerTechResearched,
    GetPlayerTechCount,
)

# 在registry注册部分添加：
registry.register(SetPlayerTechMaxAllowed())
registry.register(GetPlayerTechMaxAllowed())
registry.register(AddPlayerTechResearched())
registry.register(SetPlayerTechResearched())
registry.register(GetPlayerTechResearched())
registry.register(GetPlayerTechCount())
```

**Step 3: 更新Factory测试**

在 `tests/natives/test_factory.py` 中更新函数数量统计：

```python
# 更新期望的函数数量（原有数量 + 6）
assert len(natives) == 原有数量 + 6
```

**Step 4: 运行Factory测试**

```bash
pytest tests/natives/test_factory.py -v
```

Expected: PASS

**Step 5: 提交**

```bash
git add src/jass_runner/natives/factory.py src/jass_runner/natives/__init__.py tests/natives/test_factory.py
git commit -m "feat(natives): 在工厂中注册6个玩家科技native函数"
```

---

## Task 9: 创建集成测试

**Files:**
- Create: `tests/integration/test_player_tech_integration.py`

**Step 1: 编写集成测试**

创建 `tests/integration/test_player_tech_integration.py`：

```python
"""玩家科技系统集成测试。"""

import pytest
from src.jass_runner.natives.player import Player
from src.jass_runner.natives.player_tech_natives import (
    SetPlayerTechMaxAllowed,
    GetPlayerTechMaxAllowed,
    AddPlayerTechResearched,
    SetPlayerTechResearched,
    GetPlayerTechResearched,
    GetPlayerTechCount,
)


class TestPlayerTechIntegration:
    """测试玩家科技系统完整工作流程。"""

    def test_complete_tech_research_flow(self):
        """测试完整的科技研究流程。"""
        state_context = None
        player = Player("test_handle", 0)
        tech_id = 1214542384  # 'Hpal'

        # 设置最大允许等级
        SetPlayerTechMaxAllowed().execute(state_context, player, tech_id, 5)
        assert GetPlayerTechMaxAllowed().execute(state_context, player, tech_id) == 5

        # 初始未研究
        assert GetPlayerTechResearched().execute(state_context, player, tech_id, False) is False
        assert GetPlayerTechCount().execute(state_context, player, tech_id, False) == 0

        # 研究科技
        SetPlayerTechResearched().execute(state_context, player, tech_id, 2)
        assert GetPlayerTechResearched().execute(state_context, player, tech_id, False) is True
        assert GetPlayerTechCount().execute(state_context, player, tech_id, False) == 2

        # 增加研究等级
        AddPlayerTechResearched().execute(state_context, player, tech_id, 2)
        assert GetPlayerTechCount().execute(state_context, player, tech_id, False) == 4

    def test_multi_player_tech_isolation(self):
        """测试多玩家科技独立。"""
        state_context = None
        player0 = Player("handle0", 0)
        player1 = Player("handle1", 1)
        tech_id = 1214542384

        # 玩家0研究科技
        SetPlayerTechResearched().execute(state_context, player0, tech_id, 3)

        # 玩家1未研究
        assert GetPlayerTechCount().execute(state_context, player1, tech_id, False) == 0
        assert GetPlayerTechResearched().execute(state_context, player1, tech_id, False) is False

        # 玩家0有研究
        assert GetPlayerTechCount().execute(state_context, player0, tech_id, False) == 3
        assert GetPlayerTechResearched().execute(state_context, player0, tech_id, False) is True

    def test_multiple_techs(self):
        """测试多个科技独立管理。"""
        state_context = None
        player = Player("test_handle", 0)
        tech1 = 1214542384  # 'Hpal'
        tech2 = 1214542385  # 'Hmkg'

        SetPlayerTechResearched().execute(state_context, player, tech1, 2)
        SetPlayerTechResearched().execute(state_context, player, tech2, 5)

        assert GetPlayerTechCount().execute(state_context, player, tech1, False) == 2
        assert GetPlayerTechCount().execute(state_context, player, tech2, False) == 5
```

**Step 2: 运行集成测试**

```bash
pytest tests/integration/test_player_tech_integration.py -v
```

Expected: 3个测试全部PASS

**Step 3: 提交**

```bash
git add tests/integration/test_player_tech_integration.py
git commit -m "test(integration): 添加玩家科技系统集成测试"
```

---

## Task 10: 运行完整测试套件

**Step 1: 运行所有相关测试**

```bash
pytest tests/natives/test_player_tech.py tests/natives/test_player_tech_natives.py tests/natives/test_factory.py tests/integration/test_player_tech_integration.py -v
```

Expected: 所有测试PASS

**Step 2: 运行完整测试套件确保无回归**

```bash
pytest
```

Expected: 所有原有测试 + 新增测试全部PASS

**Step 3: 提交设计文档**

```bash
git add docs/plans/2026-03-06-player-tech-design.md docs/plans/2026-03-06-player-tech-implementation.md
git commit -m "docs: 添加玩家科技系统设计文档和实施计划"
```

---

## 完成检查清单

- [ ] Player类添加了科技状态存储（_tech_max_allowed, _tech_researched）
- [ ] Player类添加了6个科技管理方法
- [ ] 实现了SetPlayerTechMaxAllowed native函数
- [ ] 实现了GetPlayerTechMaxAllowed native函数
- [ ] 实现了AddPlayerTechResearched native函数
- [ ] 实现了SetPlayerTechResearched native函数
- [ ] 实现了GetPlayerTechResearched native函数
- [ ] 实现了GetPlayerTechCount native函数
- [ ] 6个函数都在NativeFactory中注册
- [ ] 所有函数都导出到__init__.py
- [ ] Player类测试通过
- [ ] 6个native函数单元测试通过
- [ ] 集成测试通过
- [ ] 完整测试套件无回归
- [ ] 设计文档已提交

---

## 参考文档

- 设计文档: `docs/plans/2026-03-06-player-tech-design.md`
- common.j参考: `resources/common.j` 第1702-1707行
- 类似实现参考: `src/jass_runner/natives/player_state_natives.py`
