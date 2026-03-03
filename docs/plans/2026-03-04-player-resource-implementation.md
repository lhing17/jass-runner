# 玩家资源系统实现计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 实现玩家资源管理系统，支持黄金、木材、人口四种状态，提供 GetPlayerState 和 SetPlayerState native 函数

**Architecture:** 在 Player 类中添加资源属性，通过 get_state/set_state 方法管理资源，PlayerStateNatives 封装为 native 函数，超过范围时自动截断

**Tech Stack:** Python 3.8+, pytest, 项目既有 Native 函数框架

---

## 前置准备

确保已阅读：
- `docs/plans/2026-03-04-player-resource-system-design.md` - 设计文档
- `src/jass_runner/natives/handle.py` - 现有 Player 类实现（约280-341行）
- `src/jass_runner/natives/item_inventory_natives.py` - 参考实现示例

---

## Task 1: 添加 Player 资源属性

**Files:**
- Modify: `src/jass_runner/natives/handle.py`
- Test: `tests/natives/test_player_state.py`

**Step 1: 编写 Player 资源属性测试**

```python
def test_player_initial_resources():
    """测试 Player 初始资源值。"""
    from src.jass_runner.natives.handle import Player

    player = Player(0)

    assert player.get_state(1) == 500   # GOLD 初始值
    assert player.get_state(2) == 0     # LUMBER 初始值
    assert player.get_state(4) == 100   # FOOD_CAP 初始值
    assert player.get_state(5) == 0     # FOOD_USED 初始值
```

**Step 2: 运行测试确认失败**

```bash
pytest tests/natives/test_player_state.py::test_player_initial_resources -v
```

Expected: FAIL - "get_state not defined"

**Step 3: 在 Player 类中添加资源属性和方法**

在 `src/jass_runner/natives/handle.py` 中，在 Player 类的 `__init__` 方法中添加：

```python
# 资源属性（最小集）
self._gold: int = 500         # 黄金 0-1000000，初始500
self._lumber: int = 0         # 木材 0-1000000，初始0
self._food_cap: int = 100     # 人口上限 0-300，初始100
self._food_used: int = 0      # 已用人口 0-food_cap，初始0
```

在 Player 类中添加常量定义：

```python
# 玩家状态类型常量
PLAYER_STATE_RESOURCE_GOLD = 1
PLAYER_STATE_RESOURCE_LUMBER = 2
PLAYER_STATE_RESOURCE_FOOD_CAP = 4
PLAYER_STATE_RESOURCE_FOOD_USED = 5
```

添加资源管理方法：

```python
def _clamp_resource(self, value: int, min_val: int, max_val: int) -> int:
    """将值截断到有效范围。

    参数：
        value: 要截断的值
        min_val: 最小值
        max_val: 最大值

    返回：
        截断后的值
    """
    return max(min_val, min(value, max_val))

def get_state(self, state_type: int) -> int:
    """获取玩家状态值。

    参数：
        state_type: 状态类型（PLAYER_STATE_RESOURCE_*）

    返回：
        状态值

    异常：
        ValueError: 无效的状态类型
    """
    if state_type == Player.PLAYER_STATE_RESOURCE_GOLD:
        return self._gold
    elif state_type == Player.PLAYER_STATE_RESOURCE_LUMBER:
        return self._lumber
    elif state_type == Player.PLAYER_STATE_RESOURCE_FOOD_CAP:
        return self._food_cap
    elif state_type == Player.PLAYER_STATE_RESOURCE_FOOD_USED:
        return self._food_used
    else:
        raise ValueError(f"无效的玩家状态类型: {state_type}")

def set_state(self, state_type: int, value: int) -> int:
    """设置玩家状态值。

    参数：
        state_type: 状态类型（PLAYER_STATE_RESOURCE_*）
        value: 要设置的值

    返回：
        实际设置的值（超出范围时自动截断到边界）

    异常：
        ValueError: 无效的状态类型
    """
    if state_type == Player.PLAYER_STATE_RESOURCE_GOLD:
        self._gold = self._clamp_resource(value, 0, 1000000)
        return self._gold
    elif state_type == Player.PLAYER_STATE_RESOURCE_LUMBER:
        self._lumber = self._clamp_resource(value, 0, 1000000)
        return self._lumber
    elif state_type == Player.PLAYER_STATE_RESOURCE_FOOD_CAP:
        self._food_cap = self._clamp_resource(value, 0, 300)
        return self._food_cap
    elif state_type == Player.PLAYER_STATE_RESOURCE_FOOD_USED:
        # 已用人口不能超过人口上限
        max_food = self._food_cap
        self._food_used = self._clamp_resource(value, 0, max_food)
        return self._food_used
    else:
        raise ValueError(f"无效的玩家状态类型: {state_type}")
```

**Step 4: 运行测试确认通过**

```bash
pytest tests/natives/test_player_state.py::test_player_initial_resources -v
```

Expected: PASS

**Step 5: 添加更多测试并提交**

```python
def test_player_set_resources():
    """测试设置玩家资源。"""
    from src.jass_runner.natives.handle import Player

    player = Player(0)

    # 设置黄金
    result = player.set_state(1, 1000)
    assert result == 1000
    assert player.get_state(1) == 1000

    # 设置木材
    result = player.set_state(2, 500)
    assert result == 500
    assert player.get_state(2) == 500

def test_player_resource_clamping():
    """测试资源值截断。"""
    from src.jass_runner.natives.handle import Player

    player = Player(0)

    # 测试上限截断
    result = player.set_state(1, 2000000)  # 超过100万
    assert result == 1000000
    assert player.get_state(1) == 1000000

    # 测试下限截断（负数）
    result = player.set_state(1, -100)
    assert result == 0
    assert player.get_state(1) == 0
```

```bash
git add tests/natives/test_player_state.py src/jass_runner/natives/handle.py
git commit -m "feat(handle): 添加 Player 资源属性管理"
```

---

## Task 2: 实现 GetPlayerState Native 函数

**Files:**
- Create: `src/jass_runner/natives/player_state_natives.py`
- Test: `tests/natives/test_player_natives.py`

**Step 1: 编写测试**

```python
def test_get_player_state():
    """测试 GetPlayerState native 函数。"""
    from src.jass_runner.natives.player_state_natives import GetPlayerState
    from src.jass_runner.natives.state import StateContext
    from src.jass_runner.natives.manager import HandleManager

    handle_manager = HandleManager()
    state_context = StateContext(handle_manager)
    native = GetPlayerState()

    player = handle_manager.create_player(0)
    result = native.execute(state_context, player, 1)  # GOLD

    assert result == 500  # 初始黄金
```

**Step 2: 运行测试确认失败**

```bash
pytest tests/natives/test_player_natives.py::test_get_player_state -v
```

Expected: FAIL - "player_state_natives not found"

**Step 3: 实现 GetPlayerState 类**

创建 `src/jass_runner/natives/player_state_natives.py`：

```python
"""玩家资源相关 native 函数实现。"""

import logging
from typing import TYPE_CHECKING

from .base import NativeFunction

if TYPE_CHECKING:
    from .state import StateContext
    from .handle import Player

logger = logging.getLogger(__name__)


class GetPlayerState(NativeFunction):
    """获取玩家状态。"""

    @property
    def name(self) -> str:
        return "GetPlayerState"

    def execute(self, state_context: 'StateContext', player: 'Player',
                state_type: int) -> int:
        """执行 GetPlayerState native 函数。

        参数：
            state_context: 状态上下文
            player: 玩家对象
            state_type: 状态类型（PLAYER_STATE_RESOURCE_*）

        返回：
            玩家状态值
        """
        return player.get_state(state_type)
```

**Step 4: 运行测试确认通过**

```bash
pytest tests/natives/test_player_natives.py::test_get_player_state -v
```

Expected: PASS

**Step 5: 提交**

```bash
git add tests/natives/test_player_natives.py src/jass_runner/natives/player_state_natives.py
git commit -m "feat(natives): 实现 GetPlayerState native 函数"
```

---

## Task 3: 实现 SetPlayerState Native 函数

**Files:**
- Modify: `src/jass_runner/natives/player_state_natives.py`
- Test: `tests/natives/test_player_natives.py`

**Step 1: 编写测试**

```python
def test_set_player_state():
    """测试 SetPlayerState native 函数。"""
    from src.jass_runner.natives.player_state_natives import SetPlayerState
    from src.jass_runner.natives.state import StateContext
    from src.jass_runner.natives.manager import HandleManager

    handle_manager = HandleManager()
    state_context = StateContext(handle_manager)
    native = SetPlayerState()

    player = handle_manager.create_player(0)
    result = native.execute(state_context, player, 1, 2000)  # 设置 GOLD 为 2000

    assert result == 2000
    assert player.get_state(1) == 2000

def test_set_player_state_clamping():
    """测试 SetPlayerState 截断功能。"""
    from src.jass_runner.natives.player_state_natives import SetPlayerState
    from src.jass_runner.natives.state import StateContext
    from src.jass_runner.natives.manager import HandleManager

    handle_manager = HandleManager()
    state_context = StateContext(handle_manager)
    native = SetPlayerState()

    player = handle_manager.create_player(0)
    result = native.execute(state_context, player, 1, 2000000)  # 超出上限

    assert result == 1000000  # 被截断到上限
```

**Step 2: 实现 SetPlayerState 类**

在 `player_state_natives.py` 中添加：

```python
class SetPlayerState(NativeFunction):
    """设置玩家状态。"""

    @property
    def name(self) -> str:
        return "SetPlayerState"

    def execute(self, state_context: 'StateContext', player: 'Player',
                state_type: int, value: int) -> int:
        """执行 SetPlayerState native 函数。

        参数：
            state_context: 状态上下文
            player: 玩家对象
            state_type: 状态类型（PLAYER_STATE_RESOURCE_*）
            value: 要设置的值

        返回：
            实际设置的值（超出范围时自动截断到边界）
        """
        actual_value = player.set_state(state_type, value)
        logger.info(f"[玩家{player.player_id}] 设置状态{state_type}为{actual_value}（输入{value}）")
        return actual_value
```

**Step 3: 运行测试确认通过并提交**

```bash
git add tests/natives/test_player_natives.py src/jass_runner/natives/player_state_natives.py
git commit -m "feat(natives): 实现 SetPlayerState native 函数"
```

---

## Task 4: 在 NativeFactory 中注册玩家资源函数

**Files:**
- Modify: `src/jass_runner/natives/factory.py`
- Test: `tests/natives/test_player_natives.py`

**Step 1: 编写集成测试**

```python
def test_all_player_natives_registered():
    """测试所有玩家资源 native 函数已注册。"""
    from src.jass_runner.natives.factory import NativeFactory

    registry = NativeFactory.create_default_registry()

    assert registry.get("GetPlayerState") is not None
    assert registry.get("SetPlayerState") is not None
```

**Step 2: 运行测试确认失败**

```bash
pytest tests/natives/test_player_natives.py::test_all_player_natives_registered -v
```

Expected: FAIL

**Step 3: 修改 factory.py 注册玩家资源函数**

在 `src/jass_runner/natives/factory.py` 中：

1. 在文件顶部导入：

```python
from .player_state_natives import (
    GetPlayerState,
    SetPlayerState,
)
```

2. 在 `create_default_registry` 方法中注册：

```python
# 玩家资源 native 函数
registry.register(GetPlayerState())
registry.register(SetPlayerState())
```

**Step 4: 运行测试确认通过并提交**

```bash
pytest tests/natives/test_player_natives.py::test_all_player_natives_registered -v
```

Expected: PASS

```bash
git add tests/natives/test_player_natives.py src/jass_runner/natives/factory.py
git commit -m "feat(factory): 注册玩家资源 native 函数"
```

---

## Task 5: 编写集成测试

**Files:**
- Create: `tests/integration/test_player_system.py`

**Step 1: 编写完整场景测试**

```python
"""玩家资源系统集成测试。"""

import pytest
from src.jass_runner.natives.factory import NativeFactory
from src.jass_runner.natives.state import StateContext
from src.jass_runner.natives.manager import HandleManager


class TestPlayerSystem:
    """测试玩家资源系统完整流程。"""

    def test_player_resource_workflow(self):
        """测试玩家资源操作的完整流程。"""
        registry = NativeFactory.create_default_registry()
        handle_manager = HandleManager()
        state_context = StateContext(handle_manager)

        # 创建玩家
        player = handle_manager.create_player(0)

        # 获取初始资源
        get_state = registry.get("GetPlayerState")
        assert get_state.execute(state_context, player, 1) == 500  # GOLD
        assert get_state.execute(state_context, player, 2) == 0    # LUMBER
        assert get_state.execute(state_context, player, 4) == 100 # FOOD_CAP
        assert get_state.execute(state_context, player, 5) == 0    # FOOD_USED

        # 设置资源
        set_state = registry.get("SetPlayerState")
        set_state.execute(state_context, player, 1, 1000)  # GOLD
        set_state.execute(state_context, player, 2, 500)   # LUMBER
        set_state.execute(state_context, player, 4, 200)   # FOOD_CAP
        set_state.execute(state_context, player, 5, 50)    # FOOD_USED

        # 验证设置后的值
        assert get_state.execute(state_context, player, 1) == 1000
        assert get_state.execute(state_context, player, 2) == 500
        assert get_state.execute(state_context, player, 4) == 200
        assert get_state.execute(state_context, player, 5) == 50

    def test_player_resource_clamping(self):
        """测试资源值截断。"""
        registry = NativeFactory.create_default_registry()
        handle_manager = HandleManager()
        state_context = StateContext(handle_manager)

        player = handle_manager.create_player(1)
        set_state = registry.get("SetPlayerState")

        # 测试黄金上限截断
        result = set_state.execute(state_context, player, 1, 2000000)
        assert result == 1000000

        # 测试黄金下限截断（负值）
        result = set_state.execute(state_context, player, 1, -500)
        assert result == 0

        # 测试人口上限截断
        result = set_state.execute(state_context, player, 4, 500)
        assert result == 300  # 最大300

        # 测试已用人口不能超过上限
        set_state.execute(state_context, player, 4, 100)  # 设置上限为100
        result = set_state.execute(state_context, player, 5, 150)  # 尝试设置150
        assert result == 100  # 被截断到100
```

**Step 2: 运行所有集成测试**

```bash
pytest tests/integration/test_player_system.py -v
```

Expected: ALL PASS

**Step 3: 提交**

```bash
git add tests/integration/test_player_system.py
git commit -m "test(integration): 添加玩家资源系统集成测试"
```

---

## Task 6: 更新项目笔记

**Files:**
- Modify: `PROJECT_NOTES.md`
- Modify: `TODO.md`

**Step 1: 更新 PROJECT_NOTES.md**

在合适的位置添加：

```markdown
## 玩家资源系统

已实现玩家资源管理：
- 支持四种核心资源状态：
  - GOLD（黄金）：0-1000000，初始500
  - LUMBER（木材）：0-1000000，初始0
  - FOOD_CAP（人口上限）：0-300，初始100
  - FOOD_USED（已用人口）：0-FOOD_CAP，初始0
- Native函数：GetPlayerState, SetPlayerState
- 资源值超出范围时自动截断到边界
```

**Step 2: 更新 TODO.md**

将 v0.7.0 中的 "玩家资源系统" 标记为完成，或添加新的待办项。

**Step 3: 提交**

```bash
git add PROJECT_NOTES.md TODO.md
git commit -m "docs: 更新项目笔记，记录玩家资源系统实现"
```

---

## 验证清单

完成所有任务后，运行以下命令验证：

```bash
# 运行所有玩家资源相关测试
pytest tests/natives/test_player_state.py -v
pytest tests/natives/test_player_natives.py -v
pytest tests/integration/test_player_system.py -v

# 运行全部测试确保无回归
pytest

# 代码检查
flake8 src/jass_runner/natives/player_state_natives.py
```

## 完成标准

- [ ] Player 类资源属性和方法实现并通过测试
- [ ] GetPlayerState 和 SetPlayerState native 函数实现并通过测试
- [ ] 两个函数在 NativeFactory 中注册
- [ ] 集成测试覆盖完整场景
- [ ] 项目笔记已更新
- [ ] 所有测试通过
- [ ] 代码符合项目规范（中文注释、行数限制）
