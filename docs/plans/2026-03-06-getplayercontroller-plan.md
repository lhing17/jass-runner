# GetPlayerController Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 实现 GetPlayerController native 函数和 ConvertMapControl 类型转换函数

**Architecture:** 修改 Player 类将 controller 改为整数存储，新建 player_controller_natives.py 模块实现两个 native 函数，在工厂中注册

**Tech Stack:** Python 3.8+, pytest, 现有 JASS Runner 框架

---

## Task 1: 修改 Player 类的 controller 属性为整数

**Files:**
- Modify: `src/jass_runner/natives/player.py:40`

**Step 1: 修改 controller 初始化逻辑**

将第40行从：
```python
self.controller = "user" if player_id < 8 else "computer" if player_id < 12 else "neutral"
```

改为：
```python
# MAP_CONTROL_USER=0, MAP_CONTROL_COMPUTER=1, MAP_CONTROL_NEUTRAL=3
if player_id < 8:
    self.controller = 0  # MAP_CONTROL_USER
elif player_id < 12:
    self.controller = 1  # MAP_CONTROL_COMPUTER
else:
    self.controller = 3  # MAP_CONTROL_NEUTRAL
```

**Step 2: 验证修改**

Run: `python -c "from src.jass_runner.natives.player import Player; p = Player('p1', 0); print(p.controller)"`
Expected: `0`

Run: `python -c "from src.jass_runner.natives.player import Player; p = Player('p9', 9); print(p.controller)"`
Expected: `1`

Run: `python -c "from src.jass_runner.natives.player import Player; p = Player('p13', 13); print(p.controller)"`
Expected: `3`

**Step 3: Commit**

```bash
git add src/jass_runner/natives/player.py
git commit -m "refactor(player): 将 controller 属性从字符串改为整数类型"
```

---

## Task 2: 创建 player_controller_natives.py 模块

**Files:**
- Create: `src/jass_runner/natives/player_controller_natives.py`

**Step 1: 编写模块代码**

```python
"""玩家控制器相关 native 函数实现。

此模块包含与玩家控制器类型相关的 JASS native 函数。
"""

import logging
from typing import TYPE_CHECKING

from .base import NativeFunction

if TYPE_CHECKING:
    from .state import StateContext
    from .handle import Player

logger = logging.getLogger(__name__)


class GetPlayerController(NativeFunction):
    """获取玩家控制器类型。"""

    @property
    def name(self) -> str:
        """获取 native 函数名称。

        返回：
            函数名称 "GetPlayerController"
        """
        return "GetPlayerController"

    def execute(self, state_context: 'StateContext', player: 'Player') -> int:
        """执行 GetPlayerController native 函数。

        参数：
            state_context: 状态上下文
            player: 玩家对象

        返回：
            控制器类型整数（0=USER, 1=COMPUTER, 2=RESCUABLE, 3=NEUTRAL, 4=CREEP, 5=NONE）
        """
        if player is None:
            logger.warning("[GetPlayerController] 玩家对象为 None")
            return 0  # MAP_CONTROL_USER

        result = player.controller
        logger.info(f"[GetPlayerController] 玩家{player.player_id} 控制器类型: {result}")
        return result


class ConvertMapControl(NativeFunction):
    """将整数转换为控制器类型。

    在 Warcraft 3 中，这是一个类型转换函数，
    在我们的实现中直接返回传入的整数。
    """

    @property
    def name(self) -> str:
        return "ConvertMapControl"

    def execute(self, state_context: 'StateContext', control_type: int) -> int:
        """执行 ConvertMapControl。

        参数：
            state_context: 状态上下文
            control_type: 控制器类型整数

        返回：
            传入的控制器类型整数
        """
        logger.info(f"[ConvertMapControl] 转换控制器类型: {control_type}")
        return control_type
```

**Step 2: 验证模块可导入**

Run: `python -c "from src.jass_runner.natives.player_controller_natives import GetPlayerController, ConvertMapControl; print('OK')"`
Expected: `OK`

**Step 3: Commit**

```bash
git add src/jass_runner/natives/player_controller_natives.py
git commit -m "feat(natives): 实现 GetPlayerController 和 ConvertMapControl native 函数"
```

---

## Task 3: 在工厂中注册新的 native 函数

**Files:**
- Modify: `src/jass_runner/natives/factory.py`

**Step 1: 添加导入语句**

在第132行后（player_tech_natives 导入后）添加：
```python
from .player_controller_natives import (
    GetPlayerController,
    ConvertMapControl,
)
```

**Step 2: 注册 native 函数**

在第399行后（player_tech_natives 注册后）添加：
```python
        # 注册玩家控制器相关 native 函数
        registry.register(GetPlayerController())
        registry.register(ConvertMapControl())
```

**Step 3: 验证工厂可正常工作**

Run: `python -c "from src.jass_runner.natives.factory import NativeFactory; f = NativeFactory(); r = f.create_default_registry(); print('GetPlayerController' in r._functions); print('ConvertMapControl' in r._functions)"`
Expected:
```
True
True
```

**Step 4: Commit**

```bash
git add src/jass_runner/natives/factory.py
git commit -m "feat(natives): 在工厂中注册 GetPlayerController 和 ConvertMapControl"
```

---

## Task 4: 编写单元测试

**Files:**
- Create: `tests/test_player_controller_natives.py`

**Step 1: 编写测试代码**

```python
"""玩家控制器 native 函数单元测试。"""

import pytest
from unittest.mock import MagicMock

from jass_runner.natives.player_controller_natives import GetPlayerController, ConvertMapControl


class TestGetPlayerController:
    """测试 GetPlayerController native 函数。"""

    def test_returns_user_for_player_id_0(self):
        """测试玩家0返回 USER 控制器类型。"""
        native = GetPlayerController()
        mock_context = MagicMock()
        mock_player = MagicMock()
        mock_player.player_id = 0
        mock_player.controller = 0  # MAP_CONTROL_USER

        result = native.execute(mock_context, mock_player)

        assert result == 0

    def test_returns_computer_for_player_id_9(self):
        """测试玩家9返回 COMPUTER 控制器类型。"""
        native = GetPlayerController()
        mock_context = MagicMock()
        mock_player = MagicMock()
        mock_player.player_id = 9
        mock_player.controller = 1  # MAP_CONTROL_COMPUTER

        result = native.execute(mock_context, mock_player)

        assert result == 1

    def test_returns_neutral_for_player_id_13(self):
        """测试玩家13返回 NEUTRAL 控制器类型。"""
        native = GetPlayerController()
        mock_context = MagicMock()
        mock_player = MagicMock()
        mock_player.player_id = 13
        mock_player.controller = 3  # MAP_CONTROL_NEUTRAL

        result = native.execute(mock_context, mock_player)

        assert result == 3

    def test_returns_user_when_player_is_none(self):
        """测试玩家为None时返回 USER (0)。"""
        native = GetPlayerController()
        mock_context = MagicMock()

        result = native.execute(mock_context, None)

        assert result == 0


class TestConvertMapControl:
    """测试 ConvertMapControl native 函数。"""

    def test_returns_same_value_for_user(self):
        """测试 USER (0) 转换返回相同值。"""
        native = ConvertMapControl()
        mock_context = MagicMock()

        result = native.execute(mock_context, 0)

        assert result == 0

    def test_returns_same_value_for_computer(self):
        """测试 COMPUTER (1) 转换返回相同值。"""
        native = ConvertMapControl()
        mock_context = MagicMock()

        result = native.execute(mock_context, 1)

        assert result == 1

    def test_returns_same_value_for_neutral(self):
        """测试 NEUTRAL (3) 转换返回相同值。"""
        native = ConvertMapControl()
        mock_context = MagicMock()

        result = native.execute(mock_context, 3)

        assert result == 3

    def test_returns_same_value_for_any_integer(self):
        """测试任意整数转换返回相同值。"""
        native = ConvertMapControl()
        mock_context = MagicMock()

        for i in range(6):
            result = native.execute(mock_context, i)
            assert result == i
```

**Step 2: 运行测试**

Run: `pytest tests/test_player_controller_natives.py -v`
Expected: 所有测试通过

**Step 3: Commit**

```bash
git add tests/test_player_controller_natives.py
git commit -m "test(natives): 添加 GetPlayerController 和 ConvertMapControl 单元测试"
```

---

## Task 5: 编写集成测试

**Files:**
- Create: `tests/integration/test_player_controller_integration.py`

**Step 1: 编写集成测试**

```python
"""玩家控制器 native 函数集成测试。"""

import pytest
from jass_runner.vm import JassVM


class TestPlayerControllerIntegration:
    """测试玩家控制器相关 native 函数在 VM 中的集成。"""

    @pytest.fixture
    def vm(self):
        """创建 JassVM 实例。"""
        return JassVM()

    def test_get_player_controller_for_player_0(self, vm):
        """测试获取玩家0的控制器类型。"""
        script = '''
        function main takes nothing returns nothing
            local player p = Player(0)
            local mapcontrol c = GetPlayerController(p)
            // 玩家0应该是 USER (0)
            if c == MAP_CONTROL_USER then
                call DisplayTextToPlayer(p, 0, 0, "Player 0 is USER")
            endif
        endfunction
        '''
        vm.load_script(script)
        vm.execute()

    def test_get_player_controller_for_player_9(self, vm):
        """测试获取玩家9的控制器类型。"""
        script = '''
        function main takes nothing returns nothing
            local player p = Player(9)
            local mapcontrol c = GetPlayerController(p)
            // 玩家9应该是 COMPUTER (1)
            if c == MAP_CONTROL_COMPUTER then
                call DisplayTextToPlayer(p, 0, 0, "Player 9 is COMPUTER")
            endif
        endfunction
        '''
        vm.load_script(script)
        vm.execute()

    def test_convert_map_control(self, vm):
        """测试 ConvertMapControl 函数。"""
        script = '''
        function main takes nothing returns nothing
            local mapcontrol c
            set c = ConvertMapControl(0)
            if c == MAP_CONTROL_USER then
                call DisplayTextToPlayer(Player(0), 0, 0, "Convert 0 = USER")
            endif
        endfunction
        '''
        vm.load_script(script)
        vm.execute()
```

**Step 2: 运行集成测试**

Run: `pytest tests/integration/test_player_controller_integration.py -v`
Expected: 所有测试通过

**Step 3: Commit**

```bash
git add tests/integration/test_player_controller_integration.py
git commit -m "test(integration): 添加玩家控制器 native 函数集成测试"
```

---

## Task 6: 运行完整测试套件

**Step 1: 运行所有测试**

Run: `pytest tests/ -v --tb=short`
Expected: 所有测试通过

**Step 2: 最终提交**

```bash
git log --oneline -5
```

Expected 提交历史：
```
xxxxxxx test(integration): 添加玩家控制器 native 函数集成测试
xxxxxxx test(natives): 添加 GetPlayerController 和 ConvertMapControl 单元测试
xxxxxxx feat(natives): 在工厂中注册 GetPlayerController 和 ConvertMapControl
xxxxxxx feat(natives): 实现 GetPlayerController 和 ConvertMapControl native 函数
xxxxxxx refactor(player): 将 controller 属性从字符串改为整数类型
```
