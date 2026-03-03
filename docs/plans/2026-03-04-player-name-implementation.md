# 玩家名称 Native 函数实现计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 实现 GetPlayerName 和 SetPlayerName 两个 native 函数，支持玩家名称的获取和设置

**Architecture:** 在 Player 类已有 name 属性的基础上，添加两个 native 函数封装，记录日志

**Tech Stack:** Python 3.8+, pytest

---

## Task 1: 实现 GetPlayerName Native 函数

**Files:**
- Create: `src/jass_runner/natives/player_name_natives.py`
- Test: `tests/natives/test_player_name_natives.py`

**Step 1: 编写测试**

```python
def test_get_player_name():
    """测试 GetPlayerName native 函数。"""
    from src.jass_runner.natives.player_name_natives import GetPlayerName
    from src.jass_runner.natives.state import StateContext
    from src.jass_runner.natives.manager import HandleManager

    handle_manager = HandleManager()
    state_context = StateContext(handle_manager)
    native = GetPlayerName()

    player = handle_manager.create_player(0)
    result = native.execute(state_context, player)

    assert result == "玩家0"
```

**Step 2: 运行测试确认失败**

**Step 3: 实现 GetPlayerName 类**

创建 `src/jass_runner/natives/player_name_natives.py`：

```python
"""玩家名称相关 native 函数实现。"""

import logging
from typing import TYPE_CHECKING

from .base import NativeFunction

if TYPE_CHECKING:
    from .state import StateContext
    from .handle import Player

logger = logging.getLogger(__name__)


class GetPlayerName(NativeFunction):
    """获取玩家名称。"""

    @property
    def name(self) -> str:
        return "GetPlayerName"

    def execute(self, state_context: 'StateContext', player: 'Player') -> str:
        """执行 GetPlayerName native 函数。

        参数：
            state_context: 状态上下文
            player: 玩家对象

        返回：
            玩家名称
        """
        return player.name
```

**Step 4: 运行测试确认通过并提交**

```bash
git add tests/natives/test_player_name_natives.py src/jass_runner/natives/player_name_natives.py
git commit -m "feat(natives): 实现 GetPlayerName native 函数"
```

---

## Task 2: 实现 SetPlayerName Native 函数

**Files:**
- Modify: `src/jass_runner/natives/player_name_natives.py`
- Test: `tests/natives/test_player_name_natives.py`

**Step 1: 编写测试**

```python
def test_set_player_name():
    """测试 SetPlayerName native 函数。"""
    from src.jass_runner.natives.player_name_natives import SetPlayerName
    from src.jass_runner.natives.state import StateContext
    from src.jass_runner.natives.manager import HandleManager

    handle_manager = HandleManager()
    state_context = StateContext(handle_manager)
    native = SetPlayerName()

    player = handle_manager.create_player(0)
    native.execute(state_context, player, "张三")

    assert player.name == "张三"
```

**Step 2: 实现 SetPlayerName 类**

在 `player_name_natives.py` 中添加：

```python
class SetPlayerName(NativeFunction):
    """设置玩家名称。"""

    @property
    def name(self) -> str:
        return "SetPlayerName"

    def execute(self, state_context: 'StateContext', player: 'Player',
                name: str) -> None:
        """执行 SetPlayerName native 函数。

        参数：
            state_context: 状态上下文
            player: 玩家对象
            name: 新名称
        """
        old_name = player.name
        player.name = name
        logger.info(f"[玩家{player.player_id}] 设置名称为\"{name}\"（原名称\"{old_name}\"）")
```

**Step 3: 运行测试确认通过并提交**

```bash
git add tests/natives/test_player_name_natives.py src/jass_runner/natives/player_name_natives.py
git commit -m "feat(natives): 实现 SetPlayerName native 函数"
```

---

## Task 3: 在 NativeFactory 中注册

**Files:**
- Modify: `src/jass_runner/natives/factory.py`
- Test: `tests/natives/test_player_name_natives.py`

**Step 1: 编写测试**

```python
def test_all_player_name_natives_registered():
    """测试玩家名称 native 函数已注册。"""
    from src.jass_runner.natives.factory import NativeFactory

    factory = NativeFactory()
    registry = factory.create_default_registry()

    assert registry.get("GetPlayerName") is not None
    assert registry.get("SetPlayerName") is not None
```

**Step 2: 修改 factory.py**

在文件顶部添加导入：
```python
from .player_name_natives import (
    GetPlayerName,
    SetPlayerName,
)
```

在 `create_default_registry` 中注册：
```python
# 玩家名称 native 函数
registry.register(GetPlayerName())
registry.register(SetPlayerName())
```

**Step 3: 运行测试确认通过并提交**

```bash
git add tests/natives/test_player_name_natives.py src/jass_runner/natives/factory.py
git commit -m "feat(factory): 注册玩家名称 native 函数"
```

---

## Task 4: 编写集成测试

**Files:**
- Create: `tests/integration/test_player_name_system.py`

```python
"""玩家名称系统集成测试。"""

import pytest
from src.jass_runner.natives.factory import NativeFactory
from src.jass_runner.natives.state import StateContext
from src.jass_runner.natives.manager import HandleManager


class TestPlayerNameSystem:
    """测试玩家名称系统完整流程。"""

    def test_player_name_workflow(self):
        """测试玩家名称获取和设置的完整流程。"""
        factory = NativeFactory()
        registry = factory.create_default_registry()
        state_context = StateContext()

        # 创建玩家
        player = state_context.handle_manager.create_player(0)

        # 获取默认名称
        get_name = registry.get("GetPlayerName")
        assert get_name.execute(state_context, player) == "玩家0"

        # 设置新名称
        set_name = registry.get("SetPlayerName")
        set_name.execute(state_context, player, "张三")

        # 验证新名称
        assert get_name.execute(state_context, player) == "张三"
```

```bash
git add tests/integration/test_player_name_system.py
git commit -m "test(integration): 添加玩家名称系统集成测试"
```

---

## Task 5: 更新项目笔记

**Files:**
- Modify: `PROJECT_NOTES.md`
- Modify: `TODO.md`

在 PROJECT_NOTES.md 中添加：
```markdown
## 玩家名称系统

已实现玩家名称获取和设置：
- Native函数：GetPlayerName, SetPlayerName
- 默认名称格式："玩家{player_id}"
- 支持自定义玩家名称
```

在 TODO.md 中标记完成：
```markdown
- [x] Native函数：GetPlayerName, SetPlayerName
```

```bash
git add PROJECT_NOTES.md TODO.md
git commit -m "docs: 更新项目笔记，记录玩家名称系统实现"
```

---

## 验证清单

```bash
pytest tests/natives/test_player_name_natives.py -v
pytest tests/integration/test_player_name_system.py -v
pytest
```
