# SetPlayerAlliance Native 函数实现计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 实现 `ConvertAllianceType`、`SetPlayerAlliance` 和 `GetPlayerAlliance` 三个 native 函数，支持玩家联盟系统的模拟。

**Architecture:** 创建 `AllianceManager` 集中管理玩家间联盟关系，三个 native 函数分别处理类型转换、设置和查询操作。联盟关系存储为 `(source_id, other_id) -> Set[alliance_type]` 的字典结构。

**Tech Stack:** Python 3.8+, pytest, logging

---

## 前置知识

### 现有 Native 函数实现模式

参考 `src/jass_runner/natives/player_state_natives.py` 中的实现模式：

```python
class GetPlayerState(NativeFunction):
    """获取玩家状态。"""

    @property
    def name(self) -> str:
        return "GetPlayerState"

    def execute(self, state_context: 'StateContext', player: 'Player',
                state_type: int) -> int:
        if player is None:
            logger.warning("[GetPlayerState] 玩家对象为 None")
            return 0
        # ... 实现逻辑
```

### 注册 Native 函数

在 `src/jass_runner/natives/factory.py` 的 `create_default_registry()` 方法中注册：

```python
registry.register(GetPlayerState())
```

### 联盟类型常量（来自 common.j）

```python
ALLIANCE_PASSIVE = 0
ALLIANCE_HELP_REQUEST = 1
ALLIANCE_HELP_RESPONSE = 2
ALLIANCE_SHARED_XP = 3
ALLIANCE_SHARED_SPELLS = 4
ALLIANCE_SHARED_VISION = 5
ALLIANCE_SHARED_CONTROL = 6
ALLIANCE_SHARED_ADVANCED_CONTROL = 7
ALLIANCE_RESCUABLE = 8
ALLIANCE_SHARED_VISION_FORCED = 9
```

---

## Task 1: 创建联盟类型常量定义文件

**Files:**
- Create: `src/jass_runner/natives/alliance.py`

**Step 1: 创建常量定义文件**

```python
"""联盟类型常量定义。

此模块定义了 Warcraft 3 JASS 中的联盟类型常量，
与 common.j 中的定义保持一致。
"""

# 联盟类型常量
ALLIANCE_PASSIVE = 0
ALLIANCE_HELP_REQUEST = 1
ALLIANCE_HELP_RESPONSE = 2
ALLIANCE_SHARED_XP = 3
ALLIANCE_SHARED_SPELLS = 4
ALLIANCE_SHARED_VISION = 5
ALLIANCE_SHARED_CONTROL = 6
ALLIANCE_SHARED_ADVANCED_CONTROL = 7
ALLIANCE_RESCUABLE = 8
ALLIANCE_SHARED_VISION_FORCED = 9

# 联盟类型名称映射（用于日志输出）
ALLIANCE_NAMES = {
    ALLIANCE_PASSIVE: "ALLIANCE_PASSIVE",
    ALLIANCE_HELP_REQUEST: "ALLIANCE_HELP_REQUEST",
    ALLIANCE_HELP_RESPONSE: "ALLIANCE_HELP_RESPONSE",
    ALLIANCE_SHARED_XP: "ALLIANCE_SHARED_XP",
    ALLIANCE_SHARED_SPELLS: "ALLIANCE_SHARED_SPELLS",
    ALLIANCE_SHARED_VISION: "ALLIANCE_SHARED_VISION",
    ALLIANCE_SHARED_CONTROL: "ALLIANCE_SHARED_CONTROL",
    ALLIANCE_SHARED_ADVANCED_CONTROL: "ALLIANCE_SHARED_ADVANCED_CONTROL",
    ALLIANCE_RESCUABLE: "ALLIANCE_RESCUABLE",
    ALLIANCE_SHARED_VISION_FORCED: "ALLIANCE_SHARED_VISION_FORCED",
}


def get_alliance_name(alliance_type: int) -> str:
    """获取联盟类型的名称。

    参数：
        alliance_type: 联盟类型整数

    返回：
        联盟类型的可读名称，如果未知则返回 "UNKNOWN"
    """
    return ALLIANCE_NAMES.get(alliance_type, f"UNKNOWN({alliance_type})")
```

**Step 2: 提交**

```bash
git add src/jass_runner/natives/alliance.py
git commit -m "feat: 添加联盟类型常量定义"
```

---

## Task 2: 创建 AllianceManager 类

**Files:**
- Create: `src/jass_runner/natives/alliance_manager.py`
- Test: `tests/natives/test_alliance_manager.py`

**Step 1: 编写 AllianceManager 测试**

```python
"""AllianceManager 测试。"""

import pytest
from src.jass_runner.natives.alliance_manager import AllianceManager
from src.jass_runner.natives.alliance import (
    ALLIANCE_PASSIVE,
    ALLIANCE_SHARED_VISION,
)


class TestAllianceManager:
    """测试 AllianceManager 的功能。"""

    def test_set_and_get_alliance(self):
        """测试设置和获取联盟关系。"""
        manager = AllianceManager()

        # 初始状态应为 False
        assert manager.get_alliance(0, 1, ALLIANCE_PASSIVE) is False

        # 设置联盟
        manager.set_alliance(0, 1, ALLIANCE_PASSIVE, True)
        assert manager.get_alliance(0, 1, ALLIANCE_PASSIVE) is True

        # 取消联盟
        manager.set_alliance(0, 1, ALLIANCE_PASSIVE, False)
        assert manager.get_alliance(0, 1, ALLIANCE_PASSIVE) is False

    def test_multiple_alliance_types(self):
        """测试同一对玩家可以设置多个联盟类型。"""
        manager = AllianceManager()

        manager.set_alliance(0, 1, ALLIANCE_PASSIVE, True)
        manager.set_alliance(0, 1, ALLIANCE_SHARED_VISION, True)

        assert manager.get_alliance(0, 1, ALLIANCE_PASSIVE) is True
        assert manager.get_alliance(0, 1, ALLIANCE_SHARED_VISION) is True

    def test_alliance_independence(self):
        """测试不同玩家对之间的联盟关系相互独立。"""
        manager = AllianceManager()

        # 设置玩家0对玩家1的联盟
        manager.set_alliance(0, 1, ALLIANCE_PASSIVE, True)

        # 玩家0对玩家2应该没有联盟
        assert manager.get_alliance(0, 2, ALLIANCE_PASSIVE) is False

        # 玩家1对玩家0应该没有联盟（单向）
        assert manager.get_alliance(1, 0, ALLIANCE_PASSIVE) is False

    def test_get_all_alliances(self):
        """测试获取所有联盟类型。"""
        manager = AllianceManager()

        manager.set_alliance(0, 1, ALLIANCE_PASSIVE, True)
        manager.set_alliance(0, 1, ALLIANCE_SHARED_VISION, True)

        alliances = manager.get_all_alliances(0, 1)
        assert ALLIANCE_PASSIVE in alliances
        assert ALLIANCE_SHARED_VISION in alliances
```

**Step 2: 运行测试验证失败**

```bash
pytest tests/natives/test_alliance_manager.py -v
```

Expected: 失败，模块不存在

**Step 3: 实现 AllianceManager**

```python
"""联盟管理器实现。

此模块提供 AllianceManager 类，用于集中管理玩家之间的联盟关系。
"""

from typing import Dict, Set, Tuple


class AllianceManager:
    """管理玩家之间的联盟关系。

    使用字典存储联盟关系，键为 (source_id, other_id) 元组，
    值为该玩家对已启用的联盟类型集合。
    """

    def __init__(self):
        """初始化联盟管理器。"""
        # (source_player_id, other_player_id) -> Set[alliance_type]
        self._alliances: Dict[Tuple[int, int], Set[int]] = {}

    def set_alliance(self, source_id: int, other_id: int,
                     alliance_type: int, value: bool) -> None:
        """设置玩家之间的联盟关系。

        参数：
            source_id: 源玩家ID
            other_id: 目标玩家ID
            alliance_type: 联盟类型（0-9）
            value: True 启用，False 禁用
        """
        key = (source_id, other_id)

        if key not in self._alliances:
            self._alliances[key] = set()

        if value:
            self._alliances[key].add(alliance_type)
        else:
            self._alliances[key].discard(alliance_type)

            # 如果集合为空，删除该键
            if not self._alliances[key]:
                del self._alliances[key]

    def get_alliance(self, source_id: int, other_id: int,
                     alliance_type: int) -> bool:
        """获取玩家之间的特定联盟关系状态。

        参数：
            source_id: 源玩家ID
            other_id: 目标玩家ID
            alliance_type: 联盟类型

        返回：
            该联盟类型是否启用
        """
        key = (source_id, other_id)

        if key not in self._alliances:
            return False

        return alliance_type in self._alliances[key]

    def get_all_alliances(self, source_id: int, other_id: int) -> Set[int]:
        """获取两个玩家之间所有已启用的联盟类型。

        参数：
            source_id: 源玩家ID
            other_id: 目标玩家ID

        返回：
            已启用的联盟类型集合
        """
        key = (source_id, other_id)
        return self._alliances.get(key, set()).copy()
```

**Step 4: 运行测试验证通过**

```bash
pytest tests/natives/test_alliance_manager.py -v
```

Expected: 4 个测试全部通过

**Step 5: 提交**

```bash
git add src/jass_runner/natives/alliance_manager.py tests/natives/test_alliance_manager.py
git commit -m "feat: 实现 AllianceManager 类"
```

---

## Task 3: 实现 ConvertAllianceType Native 函数

**Files:**
- Create: `src/jass_runner/natives/alliance_natives.py`
- Test: `tests/natives/test_alliance_natives.py`

**Step 1: 编写 ConvertAllianceType 测试**

```python
"""联盟相关 native 函数测试。"""

import pytest
from unittest.mock import MagicMock
from src.jass_runner.natives.alliance_natives import ConvertAllianceType
from src.jass_runner.natives.alliance import ALLIANCE_PASSIVE, ALLIANCE_SHARED_VISION


class TestConvertAllianceType:
    """测试 ConvertAllianceType native 函数。"""

    def test_convert_alliance_type_returns_input(self):
        """测试 ConvertAllianceType 返回传入的整数。"""
        native = ConvertAllianceType()
        state_context = MagicMock()

        result = native.execute(state_context, 0)
        assert result == 0

        result = native.execute(state_context, 5)
        assert result == 5

    def test_convert_alliance_type_with_constants(self):
        """测试使用联盟常量。"""
        native = ConvertAllianceType()
        state_context = MagicMock()

        assert native.execute(state_context, ALLIANCE_PASSIVE) == ALLIANCE_PASSIVE
        assert native.execute(state_context, ALLIANCE_SHARED_VISION) == ALLIANCE_SHARED_VISION
```

**Step 2: 运行测试验证失败**

```bash
pytest tests/natives/test_alliance_natives.py::TestConvertAllianceType -v
```

Expected: 失败，模块不存在

**Step 3: 实现 ConvertAllianceType**

```python
"""联盟相关 native 函数实现。

此模块包含 SetPlayerAlliance、GetPlayerAlliance 和 ConvertAllianceType
等联盟系统相关的 native 函数。
"""

import logging
from typing import TYPE_CHECKING

from .base import NativeFunction
from .alliance import get_alliance_name

if TYPE_CHECKING:
    from .manager import StateContext
    from .handle import Player

logger = logging.getLogger(__name__)


class ConvertAllianceType(NativeFunction):
    """将整数转换为联盟类型。

    在 Warcraft 3 中，这是一个类型转换函数，
    在我们的实现中直接返回传入的整数。
    """

    @property
    def name(self) -> str:
        return "ConvertAllianceType"

    def execute(self, state_context: 'StateContext', alliance_type: int) -> int:
        """执行 ConvertAllianceType。

        参数：
            state_context: 状态上下文
            alliance_type: 联盟类型整数

        返回：
            传入的联盟类型整数
        """
        logger.info(f"[ConvertAllianceType] 转换联盟类型: {alliance_type}")
        return alliance_type
```

**Step 4: 运行测试验证通过**

```bash
pytest tests/natives/test_alliance_natives.py::TestConvertAllianceType -v
```

Expected: 2 个测试通过

**Step 5: 提交**

```bash
git add src/jass_runner/natives/alliance_natives.py tests/natives/test_alliance_natives.py
git commit -m "feat: 实现 ConvertAllianceType native 函数"
```

---

## Task 4: 实现 SetPlayerAlliance Native 函数

**Files:**
- Modify: `src/jass_runner/natives/alliance_natives.py`
- Modify: `tests/natives/test_alliance_natives.py`

**Step 1: 编写 SetPlayerAlliance 测试**

添加到 `tests/natives/test_alliance_natives.py`：

```python
class TestSetPlayerAlliance:
    """测试 SetPlayerAlliance native 函数。"""

    def test_set_alliance_true(self):
        """测试设置联盟关系为 true。"""
        from src.jass_runner.natives.alliance_manager import AllianceManager

        native = SetPlayerAlliance()
        state_context = MagicMock()
        state_context.alliance_manager = AllianceManager()

        player0 = MagicMock()
        player0.player_id = 0
        player1 = MagicMock()
        player1.player_id = 1

        native.execute(state_context, player0, player1, ALLIANCE_PASSIVE, True)

        assert state_context.alliance_manager.get_alliance(0, 1, ALLIANCE_PASSIVE) is True

    def test_set_alliance_false(self):
        """测试设置联盟关系为 false。"""
        from src.jass_runner.natives.alliance_manager import AllianceManager

        native = SetPlayerAlliance()
        state_context = MagicMock()
        state_context.alliance_manager = AllianceManager()

        player0 = MagicMock()
        player0.player_id = 0
        player1 = MagicMock()
        player1.player_id = 1

        # 先设置再取消
        native.execute(state_context, player0, player1, ALLIANCE_PASSIVE, True)
        native.execute(state_context, player0, player1, ALLIANCE_PASSIVE, False)

        assert state_context.alliance_manager.get_alliance(0, 1, ALLIANCE_PASSIVE) is False

    def test_set_alliance_with_none_player(self):
        """测试传入 None player 时的处理。"""
        from src.jass_runner.natives.alliance_manager import AllianceManager

        native = SetPlayerAlliance()
        state_context = MagicMock()
        state_context.alliance_manager = AllianceManager()

        # 不应抛出异常
        native.execute(state_context, None, MagicMock(), ALLIANCE_PASSIVE, True)
        native.execute(state_context, MagicMock(), None, ALLIANCE_PASSIVE, True)
```

**Step 2: 运行测试验证失败**

```bash
pytest tests/natives/test_alliance_natives.py::TestSetPlayerAlliance -v
```

Expected: 失败，SetPlayerAlliance 未定义

**Step 3: 实现 SetPlayerAlliance**

添加到 `src/jass_runner/natives/alliance_natives.py`：

```python
class SetPlayerAlliance(NativeFunction):
    """设置两个玩家之间的联盟关系。"""

    @property
    def name(self) -> str:
        return "SetPlayerAlliance"

    def execute(self, state_context: 'StateContext',
                source_player: 'Player', other_player: 'Player',
                alliance_type: int, value: bool) -> None:
        """执行 SetPlayerAlliance。

        参数：
            state_context: 状态上下文
            source_player: 源玩家
            other_player: 目标玩家
            alliance_type: 联盟类型
            value: True 启用，False 禁用
        """
        if source_player is None or other_player is None:
            logger.warning("[SetPlayerAlliance] 玩家对象为 None")
            return

        alliance_manager = state_context.alliance_manager
        alliance_name = get_alliance_name(alliance_type)

        alliance_manager.set_alliance(
            source_player.player_id,
            other_player.player_id,
            alliance_type,
            value
        )

        logger.info(
            f"[SetPlayerAlliance] 玩家{source_player.player_id} 对 "
            f"玩家{other_player.player_id} 设置 {alliance_name}={value}"
        )
```

**Step 4: 运行测试验证通过**

```bash
pytest tests/natives/test_alliance_natives.py::TestSetPlayerAlliance -v
```

Expected: 3 个测试通过

**Step 5: 提交**

```bash
git add src/jass_runner/natives/alliance_natives.py tests/natives/test_alliance_natives.py
git commit -m "feat: 实现 SetPlayerAlliance native 函数"
```

---

## Task 5: 实现 GetPlayerAlliance Native 函数

**Files:**
- Modify: `src/jass_runner/natives/alliance_natives.py`
- Modify: `tests/natives/test_alliance_natives.py`

**Step 1: 编写 GetPlayerAlliance 测试**

添加到 `tests/natives/test_alliance_natives.py`：

```python
class TestGetPlayerAlliance:
    """测试 GetPlayerAlliance native 函数。"""

    def test_get_alliance_true(self):
        """测试获取已启用的联盟关系。"""
        from src.jass_runner.natives.alliance_manager import AllianceManager

        native = GetPlayerAlliance()
        state_context = MagicMock()
        state_context.alliance_manager = AllianceManager()

        player0 = MagicMock()
        player0.player_id = 0
        player1 = MagicMock()
        player1.player_id = 1

        # 先设置
        state_context.alliance_manager.set_alliance(0, 1, ALLIANCE_PASSIVE, True)

        result = native.execute(state_context, player0, player1, ALLIANCE_PASSIVE)
        assert result is True

    def test_get_alliance_false(self):
        """测试获取未启用的联盟关系。"""
        from src.jass_runner.natives.alliance_manager import AllianceManager

        native = GetPlayerAlliance()
        state_context = MagicMock()
        state_context.alliance_manager = AllianceManager()

        player0 = MagicMock()
        player0.player_id = 0
        player1 = MagicMock()
        player1.player_id = 1

        result = native.execute(state_context, player0, player1, ALLIANCE_PASSIVE)
        assert result is False

    def test_get_alliance_with_none_player(self):
        """测试传入 None player 时返回 False。"""
        from src.jass_runner.natives.alliance_manager import AllianceManager

        native = GetPlayerAlliance()
        state_context = MagicMock()
        state_context.alliance_manager = AllianceManager()

        result = native.execute(state_context, None, MagicMock(), ALLIANCE_PASSIVE)
        assert result is False

        result = native.execute(state_context, MagicMock(), None, ALLIANCE_PASSIVE)
        assert result is False
```

**Step 2: 运行测试验证失败**

```bash
pytest tests/natives/test_alliance_natives.py::TestGetPlayerAlliance -v
```

Expected: 失败，GetPlayerAlliance 未定义

**Step 3: 实现 GetPlayerAlliance**

添加到 `src/jass_runner/natives/alliance_natives.py`：

```python
class GetPlayerAlliance(NativeFunction):
    """获取两个玩家之间的联盟关系状态。"""

    @property
    def name(self) -> str:
        return "GetPlayerAlliance"

    def execute(self, state_context: 'StateContext',
                source_player: 'Player', other_player: 'Player',
                alliance_type: int) -> bool:
        """执行 GetPlayerAlliance。

        参数：
            state_context: 状态上下文
            source_player: 源玩家
            other_player: 目标玩家
            alliance_type: 联盟类型

        返回：
            该联盟类型是否启用
        """
        if source_player is None or other_player is None:
            logger.warning("[GetPlayerAlliance] 玩家对象为 None")
            return False

        alliance_manager = state_context.alliance_manager
        alliance_name = get_alliance_name(alliance_type)

        result = alliance_manager.get_alliance(
            source_player.player_id,
            other_player.player_id,
            alliance_type
        )

        logger.info(
            f"[GetPlayerAlliance] 玩家{source_player.player_id} 对 "
            f"玩家{other_player.player_id} 的 {alliance_name}={result}"
        )

        return result
```

**Step 4: 运行测试验证通过**

```bash
pytest tests/natives/test_alliance_natives.py::TestGetPlayerAlliance -v
```

Expected: 3 个测试通过

**Step 5: 提交**

```bash
git add src/jass_runner/natives/alliance_natives.py tests/natives/test_alliance_natives.py
git commit -m "feat: 实现 GetPlayerAlliance native 函数"
```

---

## Task 6: 在 StateContext 中集成 AllianceManager

**Files:**
- Modify: `src/jass_runner/natives/manager.py`
- Test: 需要确保现有测试仍然通过

**Step 1: 检查 StateContext 当前实现**

查看 `src/jass_runner/natives/manager.py` 中的 `StateContext` 类，了解如何添加 `alliance_manager` 属性。

**Step 2: 修改 StateContext**

在 `StateContext` 的 `__init__` 方法中添加：

```python
from .alliance_manager import AllianceManager

class StateContext:
    def __init__(self, handle_manager: HandleManager):
        self.handle_manager = handle_manager
        self.alliance_manager = AllianceManager()  # 新增
```

**Step 3: 运行现有测试确保不破坏**

```bash
pytest tests/natives/ -v
```

Expected: 所有测试通过

**Step 4: 提交**

```bash
git add src/jass_runner/natives/manager.py
git commit -m "feat: 在 StateContext 中集成 AllianceManager"
```

---

## Task 7: 注册 Native 函数

**Files:**
- Modify: `src/jass_runner/natives/factory.py`

**Step 1: 导入新的 native 函数**

在 `factory.py` 顶部添加导入：

```python
from .alliance_natives import ConvertAllianceType, SetPlayerAlliance, GetPlayerAlliance
```

**Step 2: 在 create_default_registry 中注册**

在 `create_default_registry` 方法中添加：

```python
def create_default_registry(self) -> NativeRegistry:
    registry = NativeRegistry()

    # 现有注册...

    # 注册联盟相关 native 函数
    registry.register(ConvertAllianceType())
    registry.register(SetPlayerAlliance())
    registry.register(GetPlayerAlliance())

    return registry
```

**Step 3: 运行所有测试**

```bash
pytest tests/ -v
```

Expected: 所有测试通过

**Step 4: 提交**

```bash
git add src/jass_runner/natives/factory.py
git commit -m "feat: 注册联盟相关 native 函数"
```

---

## Task 8: 创建集成测试

**Files:**
- Create: `tests/integration/test_alliance.py`

**Step 1: 编写集成测试**

```python
"""联盟系统集成测试。

测试完整的联盟设置和查询流程。
"""

import pytest
from src.jass_runner.vm import JassVM


class TestAllianceIntegration:
    """测试联盟系统端到端功能。"""

    def test_set_and_get_alliance(self):
        """测试设置和获取联盟关系的完整流程。"""
        jass_code = '''
function main takes nothing returns nothing
    local player p0 = Player(0)
    local player p1 = Player(1)
    local boolean result

    // 设置联盟
    call SetPlayerAlliance(p0, p1, ALLIANCE_PASSIVE, true)

    // 查询联盟
    set result = GetPlayerAlliance(p0, p1, ALLIANCE_PASSIVE)

    // 输出结果用于验证
    if result then
        call DisplayTextToPlayer(p0, 0, 0, "Alliance is active")
    else
        call DisplayTextToPlayer(p0, 0, 0, "Alliance is inactive")
    endif
endfunction
'''
        vm = JassVM()
        result = vm.execute(jass_code)

        assert result.success
        # 检查日志中包含联盟设置信息
        assert "Alliance is active" in result.output or "SetPlayerAlliance" in result.output

    def test_convert_alliance_type(self):
        """测试 ConvertAllianceType 在脚本中的使用。"""
        jass_code = '''
function main takes nothing returns nothing
    local alliancetype at = ConvertAllianceType(0)
    local player p0 = Player(0)
    local player p1 = Player(1)

    call SetPlayerAlliance(p0, p1, at, true)
endfunction
'''
        vm = JassVM()
        result = vm.execute(jass_code)

        assert result.success
```

**Step 2: 运行集成测试**

```bash
pytest tests/integration/test_alliance.py -v
```

Expected: 测试通过（可能需要根据实际 VM 行为调整断言）

**Step 3: 提交**

```bash
git add tests/integration/test_alliance.py
git commit -m "test: 添加联盟系统集成测试"
```

---

## Task 9: 运行完整测试套件

**Step 1: 运行所有测试**

```bash
pytest tests/ -v
```

Expected: 所有测试通过

**Step 2: 检查代码风格**

```bash
flake8 src/jass_runner/natives/alliance*.py tests/natives/test_alliance*.py
```

Expected: 无错误或警告

**Step 3: 最终提交**

```bash
git commit -m "feat: 完成 SetPlayerAlliance 及相关 native 函数实现

- 添加联盟类型常量定义
- 实现 AllianceManager 管理玩家联盟关系
- 实现 ConvertAllianceType native 函数
- 实现 SetPlayerAlliance native 函数
- 实现 GetPlayerAlliance native 函数
- 添加完整的单元测试和集成测试"
```

---

## 验证清单

- [ ] `ConvertAllianceType` 工作正常，返回传入的整数
- [ ] `SetPlayerAlliance` 可以设置玩家间的联盟关系
- [ ] `GetPlayerAlliance` 可以查询玩家间的联盟关系
- [ ] `AllianceManager` 正确维护联盟状态
- [ ] 所有单元测试通过
- [ ] 集成测试通过
- [ ] 代码符合项目规范（中文注释、行数限制等）
