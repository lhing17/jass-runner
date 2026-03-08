# GetLocalPlayer Native函数实现计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 实现JASS native函数GetLocalPlayer，在模拟环境中固定返回Player(0)

**Architecture:** 继承NativeFunction抽象基类，实现execute方法通过HandleManager获取玩家0，并在NativeFactory中注册

**Tech Stack:** Python 3.8+, pytest, 项目自定义native函数框架

---

## 前置阅读

- `src/jass_runner/natives/base.py` - NativeFunction基类定义
- `src/jass_runner/natives/basic.py:262-289` - PlayerNative参考实现
- `src/jass_runner/natives/factory.py` - NativeFactory注册机制
- `docs/plans/2026-03-08-getlocalplayer-design.md` - 设计文档

---

### Task 1: 编写GetLocalPlayer的测试

**Files:**
- Create: `tests/natives/test_get_local_player.py`

**Step 1: 编写失败测试**

```python
import pytest
from jass_runner.natives.state import StateContext
from jass_runner.natives.basic import GetLocalPlayer, PlayerNative


class TestGetLocalPlayer:
    """测试GetLocalPlayer native函数。"""

    def setup_method(self):
        """设置测试环境。"""
        self.state_context = StateContext()
        self.get_local_player = GetLocalPlayer()
        self.player_native = PlayerNative()

    def test_get_local_player_returns_valid_player(self):
        """测试GetLocalPlayer返回有效的Player对象。"""
        result = self.get_local_player.execute(self.state_context)
        assert result is not None
        assert result.handle_type == "player"

    def test_get_local_player_returns_player_zero(self):
        """测试GetLocalPlayer返回玩家ID为0。"""
        result = self.get_local_player.execute(self.state_context)
        assert result.player_id == 0

    def test_get_local_player_returns_same_as_player_zero(self):
        """测试GetLocalPlayer返回的对象与Player(0)相同。"""
        local_player = self.get_local_player.execute(self.state_context)
        player_zero = self.player_native.execute(self.state_context, 0)
        assert local_player is player_zero
```

**Step 2: 运行测试验证失败**

Run: `pytest tests/natives/test_get_local_player.py -v`

Expected: FAIL with "ImportError: cannot import name 'GetLocalPlayer' from 'jass_runner.natives.basic'"

**Step 3: Commit测试文件**

```bash
git add tests/natives/test_get_local_player.py
git commit -m "test: 添加GetLocalPlayer native函数测试"
```

---

### Task 2: 实现GetLocalPlayer类

**Files:**
- Modify: `src/jass_runner/natives/basic.py`（在PlayerNative类之后添加）

**Step 1: 添加GetLocalPlayer实现**

在 `src/jass_runner/natives/basic.py` 中，找到 `PlayerNative` 类（约第262-289行），在其后添加：

```python
class GetLocalPlayer(NativeFunction):
    """获取本地玩家。

    在当前模拟环境中，固定返回玩家0作为"本地玩家"。
    """

    @property
    def name(self) -> str:
        """获取native函数的名称。"""
        return "GetLocalPlayer"

    def execute(self, state_context: 'StateContext', *args) -> 'Player':
        """执行GetLocalPlayer native函数。

        Args:
            state_context: 状态上下文，包含handle_manager
            *args: 无参数

        Returns:
            Player: 玩家0的Player对象
        """
        handle_manager = state_context.handle_manager
        return handle_manager.get_player(0)
```

**Step 2: 运行测试验证通过**

Run: `pytest tests/natives/test_get_local_player.py -v`

Expected: 3 tests PASSED

**Step 3: Commit实现**

```bash
git add src/jass_runner/natives/basic.py
git commit -m "feat: 实现GetLocalPlayer native函数"
```

---

### Task 3: 在NativeFactory中注册

**Files:**
- Modify: `src/jass_runner/natives/factory.py`

**Step 1: 添加导入和注册**

在 `src/jass_runner/natives/factory.py` 中：

1. 确保导入包含GetLocalPlayer：
   ```python
   from .basic import (
       DisplayTextToPlayer,
       KillUnit,
       PlayerNative,
       GetLocalPlayer,  # 添加这行
   )
   ```

2. 在 `create_default_registry()` 方法中添加注册（在PlayerNative注册附近）：
   ```python
   registry.register(PlayerNative())
   registry.register(GetLocalPlayer())  # 添加这行
   ```

**Step 2: 验证注册成功**

Run: `python -c "from jass_runner.natives.factory import NativeFactory; f = NativeFactory(); r = f.create_default_registry(); p = r.get('GetLocalPlayer'); print('GetLocalPlayer registered:', p is not None)"`

Expected: `GetLocalPlayer registered: True`

**Step 3: Commit注册**

```bash
git add src/jass_runner/natives/factory.py
git commit -m "chore: 在NativeFactory中注册GetLocalPlayer"
```

---

### Task 4: 运行完整测试套件验证

**Step 1: 运行相关测试**

Run: `pytest tests/natives/test_get_local_player.py tests/natives/test_basic.py -v`

Expected: 所有测试 PASSED

**Step 2: 运行完整测试套件**

Run: `pytest`

Expected: 所有测试 PASSED

**Step 3: 最终提交（如有未提交的更改）**

```bash
git status  # 检查是否有未提交更改
```

---

## 实现完成检查清单

- [ ] GetLocalPlayer类实现在basic.py中
- [ ] 测试文件test_get_local_player.py包含3个测试用例
- [ ] NativeFactory中已注册GetLocalPlayer
- [ ] 所有测试通过
- [ ] 代码提交到git

---

## 参考代码

### PlayerNative参考实现

文件: `src/jass_runner/natives/basic.py:262-289`

```python
class PlayerNative(NativeFunction):
    """获取Player对象（通过player_id）。"""

    @property
    def name(self) -> str:
        return "Player"

    def execute(self, state_context, player_id: int) -> Player:
        """执行Player native函数。"""
        handle_manager = state_context.handle_manager
        player = handle_manager.get_player(player_id)
        return player
```

### Native函数基类

文件: `src/jass_runner/natives/base.py`

```python
class NativeFunction(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def execute(self, state_context, *args, **kwargs):
        pass
```
