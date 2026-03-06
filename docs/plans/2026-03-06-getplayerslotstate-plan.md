# GetPlayerSlotState Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 实现 GetPlayerSlotState native 函数和 ConvertPlayerSlotState 类型转换函数

**Architecture:** 修改 Player 类将 slot_state 改为整数存储，新建 player_slot_state_natives.py 模块实现两个 native 函数，更新类型检查器支持隐式转换，在工厂中注册

**Tech Stack:** Python 3.8+, pytest, 现有 JASS Runner 框架

---

## Task 1: 修改 Player 类的 slot_state 属性为整数

**Files:**
- Modify: `src/jass_runner/natives/player.py:39`

**Step 1: 修改 slot_state 初始化逻辑**

将第39行从：
```python
self.slot_state = "player" if player_id < 12 else "empty"  # 0-11为玩家，12-15为空
```

改为：
```python
# PLAYER_SLOT_STATE_EMPTY=0, PLAYER_SLOT_STATE_PLAYING=1, PLAYER_SLOT_STATE_LEFT=2
if player_id < 12:
    self.slot_state = 1  # PLAYER_SLOT_STATE_PLAYING
else:
    self.slot_state = 0  # PLAYER_SLOT_STATE_EMPTY
```

**Step 2: 更新类文档字符串**

将第19行的文档字符串从：
```python
slot_state: 插槽状态（'empty', 'closed', 'player'）
```

改为：
```python
slot_state: 插槽状态（0=EMPTY, 1=PLAYING, 2=LEFT）
```

**Step 3: 验证修改**

Run: `python -c "from src.jass_runner.natives.player import Player; p = Player('p1', 0); print(p.slot_state)"`
Expected: `1`

Run: `python -c "from src.jass_runner.natives.player import Player; p = Player('p11', 11); print(p.slot_state)"`
Expected: `1`

Run: `python -c "from src.jass_runner.natives.player import Player; p = Player('p13', 13); print(p.slot_state)"`
Expected: `0`

**Step 4: Commit**

```bash
git add src/jass_runner/natives/player.py
git commit -m "refactor(player): 将 slot_state 属性从字符串改为整数类型"
```

---

## Task 2: 创建 player_slot_state_natives.py 模块

**Files:**
- Create: `src/jass_runner/natives/player_slot_state_natives.py`

**Step 1: 编写模块代码**

```python
"""玩家插槽状态相关 native 函数实现。

此模块包含与玩家插槽状态相关的 JASS native 函数。
"""

import logging
from typing import TYPE_CHECKING

from .base import NativeFunction

if TYPE_CHECKING:
    from .state import StateContext
    from .handle import Player

logger = logging.getLogger(__name__)


class GetPlayerSlotState(NativeFunction):
    """获取玩家插槽状态。"""

    @property
    def name(self) -> str:
        """获取 native 函数名称。

        返回：
            函数名称 "GetPlayerSlotState"
        """
        return "GetPlayerSlotState"

    def execute(self, state_context: 'StateContext', player: 'Player') -> int:
        """执行 GetPlayerSlotState native 函数。

        参数：
            state_context: 状态上下文
            player: 玩家对象

        返回：
            插槽状态整数（0=EMPTY, 1=PLAYING, 2=LEFT）
        """
        if player is None:
            logger.warning("[GetPlayerSlotState] 玩家对象为 None")
            return 0  # PLAYER_SLOT_STATE_EMPTY

        result = player.slot_state
        logger.info(f"[GetPlayerSlotState] 玩家{player.player_id} 插槽状态: {result}")
        return result


class ConvertPlayerSlotState(NativeFunction):
    """将整数转换为插槽状态类型。

    在 Warcraft 3 中，这是一个类型转换函数，
    在我们的实现中直接返回传入的整数。
    """

    @property
    def name(self) -> str:
        return "ConvertPlayerSlotState"

    def execute(self, state_context: 'StateContext', slot_state: int) -> int:
        """执行 ConvertPlayerSlotState。

        参数：
            state_context: 状态上下文
            slot_state: 插槽状态整数

        返回：
            传入的插槽状态整数
        """
        logger.info(f"[ConvertPlayerSlotState] 转换插槽状态: {slot_state}")
        return slot_state
```

**Step 2: 验证模块可导入**

Run: `python -c "from src.jass_runner.natives.player_slot_state_natives import GetPlayerSlotState, ConvertPlayerSlotState; print('OK')"`
Expected: `OK`

**Step 3: Commit**

```bash
git add src/jass_runner/natives/player_slot_state_natives.py
git commit -m "feat(natives): 实现 GetPlayerSlotState 和 ConvertPlayerSlotState native 函数"
```

---

## Task 3: 更新类型检查器支持 integer→playerslotstate 转换

**Files:**
- Modify: `src/jass_runner/types/checker.py`

**Step 1: 找到类型转换表**

查找 `IMPLICIT_CONVERSIONS` 字典或类似的类型转换定义。

**Step 2: 添加 playerslotstate 类型转换**

参考 mapcontrol 的转换规则，添加：
```python
"playerslotstate": {"integer"},  # 允许 integer 隐式转换为 playerslotstate
```

或者如果是使用 `can_implicitly_convert` 方法，添加相应的类型检查逻辑。

**Step 3: 验证类型检查器**

Run: `python -c "from src.jass_runner.types.checker import TypeChecker; tc = TypeChecker(); print('playerslotstate' in tc._type_hierarchy._hierarchy)"`
Expected: `True`

**Step 4: Commit**

```bash
git add src/jass_runner/types/checker.py
git commit -m "feat(types): 添加 integer 到 playerslotstate 的隐式类型转换支持"
```

---

## Task 4: 在工厂中注册新的 native 函数

**Files:**
- Modify: `src/jass_runner/natives/factory.py`

**Step 1: 添加导入语句**

在 player_controller_natives 导入后添加：
```python
from .player_slot_state_natives import (
    GetPlayerSlotState,
    ConvertPlayerSlotState,
)
```

**Step 2: 注册 native 函数**

在 player_controller_natives 注册后添加：
```python
        # 注册玩家插槽状态相关 native 函数
        registry.register(GetPlayerSlotState())
        registry.register(ConvertPlayerSlotState())
```

**Step 3: 验证工厂可正常工作**

Run: `python -c "from src.jass_runner.natives.factory import NativeFactory; f = NativeFactory(); r = f.create_default_registry(); print('GetPlayerSlotState' in r._functions); print('ConvertPlayerSlotState' in r._functions)"`
Expected:
```
True
True
```

**Step 4: Commit**

```bash
git add src/jass_runner/natives/factory.py
git commit -m "feat(natives): 在工厂中注册 GetPlayerSlotState 和 ConvertPlayerSlotState"
```

---

## Task 5: 编写单元测试

**Files:**
- Create: `tests/test_player_slot_state_natives.py`

**Step 1: 编写测试代码**

```python
"""玩家插槽状态 native 函数单元测试。"""

import pytest
from unittest.mock import MagicMock

from jass_runner.natives.player_slot_state_natives import GetPlayerSlotState, ConvertPlayerSlotState


class TestGetPlayerSlotState:
    """测试 GetPlayerSlotState native 函数。"""

    def test_returns_playing_for_player_id_0(self):
        """测试玩家0返回 PLAYING 插槽状态。"""
        native = GetPlayerSlotState()
        mock_context = MagicMock()
        mock_player = MagicMock()
        mock_player.player_id = 0
        mock_player.slot_state = 1  # PLAYER_SLOT_STATE_PLAYING

        result = native.execute(mock_context, mock_player)

        assert result == mock_player.slot_state

    def test_returns_playing_for_player_id_11(self):
        """测试玩家11返回 PLAYING 插槽状态。"""
        native = GetPlayerSlotState()
        mock_context = MagicMock()
        mock_player = MagicMock()
        mock_player.player_id = 11
        mock_player.slot_state = 1  # PLAYER_SLOT_STATE_PLAYING

        result = native.execute(mock_context, mock_player)

        assert result == mock_player.slot_state

    def test_returns_empty_for_player_id_12(self):
        """测试玩家12返回 EMPTY 插槽状态。"""
        native = GetPlayerSlotState()
        mock_context = MagicMock()
        mock_player = MagicMock()
        mock_player.player_id = 12
        mock_player.slot_state = 0  # PLAYER_SLOT_STATE_EMPTY

        result = native.execute(mock_context, mock_player)

        assert result == mock_player.slot_state

    def test_returns_empty_for_player_id_15(self):
        """测试玩家15返回 EMPTY 插槽状态。"""
        native = GetPlayerSlotState()
        mock_context = MagicMock()
        mock_player = MagicMock()
        mock_player.player_id = 15
        mock_player.slot_state = 0  # PLAYER_SLOT_STATE_EMPTY

        result = native.execute(mock_context, mock_player)

        assert result == mock_player.slot_state

    def test_returns_empty_when_player_is_none(self):
        """测试玩家为None时返回 EMPTY (0)。"""
        native = GetPlayerSlotState()
        mock_context = MagicMock()

        result = native.execute(mock_context, None)

        assert result == 0


class TestConvertPlayerSlotState:
    """测试 ConvertPlayerSlotState native 函数。"""

    def test_returns_same_value_for_empty(self):
        """测试 EMPTY (0) 转换返回相同值。"""
        native = ConvertPlayerSlotState()
        mock_context = MagicMock()

        result = native.execute(mock_context, 0)

        assert result == 0

    def test_returns_same_value_for_playing(self):
        """测试 PLAYING (1) 转换返回相同值。"""
        native = ConvertPlayerSlotState()
        mock_context = MagicMock()

        result = native.execute(mock_context, 1)

        assert result == 1

    def test_returns_same_value_for_left(self):
        """测试 LEFT (2) 转换返回相同值。"""
        native = ConvertPlayerSlotState()
        mock_context = MagicMock()

        result = native.execute(mock_context, 2)

        assert result == 2

    def test_returns_same_value_for_any_integer(self):
        """测试任意整数转换返回相同值。"""
        native = ConvertPlayerSlotState()
        mock_context = MagicMock()

        for i in range(3):
            result = native.execute(mock_context, i)
            assert result == i
```

**Step 2: 运行测试**

Run: `pytest tests/test_player_slot_state_natives.py -v`
Expected: 所有测试通过

**Step 3: Commit**

```bash
git add tests/test_player_slot_state_natives.py
git commit -m "test(natives): 添加 GetPlayerSlotState 和 ConvertPlayerSlotState 单元测试"
```

---

## Task 6: 编写集成测试

**Files:**
- Create: `tests/integration/test_player_slot_state_integration.py`

**Step 1: 编写集成测试**

```python
"""玩家插槽状态 native 函数集成测试。"""

import pytest
from src.jass_runner.natives.player import Player
from src.jass_runner.natives.player_slot_state_natives import (
    GetPlayerSlotState,
    ConvertPlayerSlotState,
)


class TestPlayerSlotStateIntegration:
    """测试玩家插槽状态相关 native 函数在 VM 中的集成。"""

    def test_get_player_slot_state_for_player_0(self):
        """测试获取玩家0的插槽状态为 PLAYING。"""
        state_context = None
        player = Player("handle0", 0)

        result = GetPlayerSlotState().execute(state_context, player)

        # 玩家0应该是 PLAYING (1)
        assert result == 1

    def test_get_player_slot_state_for_player_11(self):
        """测试获取玩家11的插槽状态为 PLAYING。"""
        state_context = None
        player = Player("handle11", 11)

        result = GetPlayerSlotState().execute(state_context, player)

        # 玩家11应该是 PLAYING (1)
        assert result == 1

    def test_get_player_slot_state_for_player_12(self):
        """测试获取玩家12的插槽状态为 EMPTY。"""
        state_context = None
        player = Player("handle12", 12)

        result = GetPlayerSlotState().execute(state_context, player)

        # 玩家12应该是 EMPTY (0)
        assert result == 0

    def test_get_player_slot_state_for_player_15(self):
        """测试获取玩家15的插槽状态为 EMPTY。"""
        state_context = None
        player = Player("handle15", 15)

        result = GetPlayerSlotState().execute(state_context, player)

        # 玩家15应该是 EMPTY (0)
        assert result == 0

    def test_get_player_slot_state_returns_empty_for_none(self):
        """测试获取 None 玩家时返回 EMPTY。"""
        state_context = None

        result = GetPlayerSlotState().execute(state_context, None)

        # None 玩家应该返回 EMPTY (0)
        assert result == 0

    def test_convert_player_slot_state_returns_same_value(self):
        """测试 ConvertPlayerSlotState 返回相同的整数值。"""
        state_context = None

        # 测试所有插槽状态
        for i in range(3):
            result = ConvertPlayerSlotState().execute(state_context, i)
            assert result == i

    def test_player_slot_state_matches_player_attribute(self):
        """测试 GetPlayerSlotState 返回的值与 player.slot_state 属性一致。"""
        state_context = None

        # 测试不同玩家ID
        for player_id in [0, 5, 11, 12, 13, 15]:
            player = Player(f"handle{player_id}", player_id)
            result = GetPlayerSlotState().execute(state_context, player)
            assert result == player.slot_state
```

**Step 2: 运行集成测试**

Run: `pytest tests/integration/test_player_slot_state_integration.py -v`
Expected: 所有测试通过

**Step 3: Commit**

```bash
git add tests/integration/test_player_slot_state_integration.py
git commit -m "test(integration): 添加玩家插槽状态 native 函数集成测试"
```

---

## Task 7: 运行完整测试套件

**Step 1: 运行所有测试**

Run: `pytest tests/ -v --tb=short`
Expected: 所有测试通过

**Step 2: 最终提交**

```bash
git log --oneline -8
```

Expected 提交历史：
```
xxxxxxx test(integration): 添加玩家插槽状态 native 函数集成测试
xxxxxxx test(natives): 添加 GetPlayerSlotState 和 ConvertPlayerSlotState 单元测试
xxxxxxx feat(natives): 在工厂中注册 GetPlayerSlotState 和 ConvertPlayerSlotState
xxxxxxx feat(types): 添加 integer 到 playerslotstate 的隐式类型转换支持
xxxxxxx feat(natives): 实现 GetPlayerSlotState 和 ConvertPlayerSlotState native 函数
xxxxxxx refactor(player): 将 slot_state 属性从字符串改为整数类型
xxxxxxx docs(plans): 添加 GetPlayerSlotState 和 ConvertPlayerSlotState 实现的设计文档
```
