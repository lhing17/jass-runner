# ConvertPlayerState Native 函数实现计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 实现 `ConvertPlayerState` native 函数，扩展 `Player` 类支持所有 playerstate 常量。

**Architecture:** 在 `Player` 类中添加 `_state_data` 字典存储非资源类状态，保持现有资源状态逻辑不变。实现 `ConvertPlayerState` native 函数返回传入的整数。

**Tech Stack:** Python 3.8+, pytest, logging

---

## 前置知识

### 现有 Player 类状态实现

参考 `src/jass_runner/natives/handle.py` 中的 `Player` 类：

```python
class Player:
    PLAYER_STATE_RESOURCE_GOLD = 1
    PLAYER_STATE_RESOURCE_LUMBER = 2
    PLAYER_STATE_RESOURCE_FOOD_CAP = 4
    PLAYER_STATE_RESOURCE_FOOD_USED = 5

    def __init__(self, handle_id: str, player_id: int):
        self._gold: int = 500
        self._lumber: int = 0
        self._food_cap: int = 100
        self._food_used: int = 0

    def get_state(self, state_type: int) -> int:
        if state_type == Player.PLAYER_STATE_RESOURCE_GOLD:
            return self._gold
        # ... 其他资源状态

    def set_state(self, state_type: int, value: int) -> int:
        if state_type == Player.PLAYER_STATE_RESOURCE_GOLD:
            self._gold = self._clamp_resource(value, 0, 1000000)
            return self._gold
        # ... 其他资源状态
```

### ConvertAllianceType 实现参考

参考 `src/jass_runner/natives/alliance_natives.py`：

```python
class ConvertAllianceType(NativeFunction):
    @property
    def name(self) -> str:
        return "ConvertAllianceType"

    def execute(self, state_context: 'StateContext', alliance_type: int) -> int:
        logger.info(f"[ConvertAllianceType] 转换联盟类型: {alliance_type}")
        return alliance_type
```

### 常量解析参考

参考 `src/jass_runner/vm/jass_vm.py` 中的 `_convert_constant_value`：

```python
elif const_type == 'alliancetype':
    try:
        import re
        match = re.search(r'ConvertAllianceType\((\d+)\)', const_value)
        if match:
            return int(match.group(1))
        else:
            return int(const_value)
    except (ValueError, AttributeError):
        return 0
```

---

## Task 1: 扩展 Player 类支持通用状态存储

**Files:**
- Modify: `src/jass_runner/natives/handle.py`
- Test: `tests/handles/test_player.py`

**Step 1: 编写测试**

在 `tests/handles/test_player.py` 中添加：

```python
class TestPlayerExtendedStates:
    """测试 Player 类扩展状态支持。"""

    def test_get_state_non_resource_default_zero(self):
        """测试获取未设置的非资源状态返回 0。"""
        from src.jass_runner.natives.handle import Player

        player = Player("player_0", 0)

        # 获取未设置的状态（如 PLAYER_STATE_NO_CREEP_SLEEP = 25）
        result = player.get_state(25)
        assert result == 0

    def test_set_and_get_state_non_resource(self):
        """测试设置和获取非资源状态。"""
        from src.jass_runner.natives.handle import Player

        player = Player("player_0", 0)

        # 设置非资源状态
        player.set_state(25, 1)

        # 获取状态
        result = player.get_state(25)
        assert result == 1

    def test_resource_states_still_work(self):
        """测试资源状态仍然正常工作。"""
        from src.jass_runner.natives.handle import Player

        player = Player("player_0", 0)

        # 设置金币
        player.set_state(Player.PLAYER_STATE_RESOURCE_GOLD, 1000)

        # 获取金币
        result = player.get_state(Player.PLAYER_STATE_RESOURCE_GOLD)
        assert result == 1000
```

**Step 2: 运行测试验证失败**

```bash
pytest tests/handles/test_player.py::TestPlayerExtendedStates -v
```

Expected: 失败，`_state_data` 属性不存在

**Step 3: 修改 Player 类**

在 `src/jass_runner/natives/handle.py` 的 `Player.__init__` 方法中添加：

```python
# 在 __init__ 方法末尾添加
# 通用状态存储字典（用于非资源类状态）
self._state_data: Dict[int, int] = {}
```

在文件顶部确保导入 Dict：
```python
from typing import Dict, List, Optional, Tuple, Any
```

**Step 4: 修改 get_state 方法**

在 `get_state` 方法末尾添加：

```python
# 其他状态从字典读取，默认为 0
return self._state_data.get(state_type, 0)
```

**Step 5: 修改 set_state 方法**

在 `set_state` 方法末尾添加：

```python
# 其他状态存入字典
self._state_data[state_type] = value
return value
```

**Step 6: 运行测试验证通过**

```bash
pytest tests/handles/test_player.py::TestPlayerExtendedStates -v
```

Expected: 3 个测试通过

**Step 7: 提交**

```bash
git add src/jass_runner/natives/handle.py tests/handles/test_player.py
git commit -m "feat: 扩展 Player 类支持通用状态存储"
```

---

## Task 2: 实现 ConvertPlayerState Native 函数

**Files:**
- Modify: `src/jass_runner/natives/player_state_natives.py`
- Test: `tests/natives/test_player_state.py`

**Step 1: 编写测试**

在 `tests/natives/test_player_state.py` 中添加（如果不存在则创建文件）：

```python
"""玩家状态相关 native 函数测试。"""

from unittest.mock import MagicMock
from src.jass_runner.natives.player_state_natives import (
    ConvertPlayerState,
    GetPlayerState,
    SetPlayerState,
)


class TestConvertPlayerState:
    """测试 ConvertPlayerState native 函数。"""

    def test_convert_player_state_returns_input(self):
        """测试 ConvertPlayerState 返回传入的整数。"""
        native = ConvertPlayerState()
        state_context = MagicMock()

        result = native.execute(state_context, 0)
        assert result == 0

        result = native.execute(state_context, 25)
        assert result == 25

    def test_convert_player_state_with_various_values(self):
        """测试不同 playerstate 值。"""
        native = ConvertPlayerState()
        state_context = MagicMock()

        # 测试资源状态
        assert native.execute(state_context, 1) == 1  # GOLD
        assert native.execute(state_context, 2) == 2  # LUMBER

        # 测试其他状态
        assert native.execute(state_context, 11) == 11  # OBSERVER
        assert native.execute(state_context, 25) == 25  # NO_CREEP_SLEEP
```

**Step 2: 运行测试验证失败**

```bash
pytest tests/natives/test_player_state.py::TestConvertPlayerState -v
```

Expected: 失败，`ConvertPlayerState` 未定义

**Step 3: 实现 ConvertPlayerState**

在 `src/jass_runner/natives/player_state_natives.py` 中添加：

```python
class ConvertPlayerState(NativeFunction):
    """将整数转换为玩家状态类型。

    在 Warcraft 3 中，这是一个类型转换函数，
    在我们的实现中直接返回传入的整数。
    """

    @property
    def name(self) -> str:
        return "ConvertPlayerState"

    def execute(self, state_context: 'StateContext', player_state: int) -> int:
        """执行 ConvertPlayerState。

        参数：
            state_context: 状态上下文
            player_state: 玩家状态类型整数

        返回：
            传入的玩家状态类型整数
        """
        logger.info(f"[ConvertPlayerState] 转换玩家状态类型: {player_state}")
        return player_state
```

**Step 4: 运行测试验证通过**

```bash
pytest tests/natives/test_player_state.py::TestConvertPlayerState -v
```

Expected: 2 个测试通过

**Step 5: 提交**

```bash
git add src/jass_runner/natives/player_state_natives.py tests/natives/test_player_state.py
git commit -m "feat: 实现 ConvertPlayerState native 函数"
```

---

## Task 3: 注册 ConvertPlayerState Native 函数

**Files:**
- Modify: `src/jass_runner/natives/factory.py`
- Test: `tests/natives/test_factory.py`

**Step 1: 导入 ConvertPlayerState**

在 `src/jass_runner/natives/factory.py` 中，找到 `player_state_natives` 导入并添加：

```python
from .player_state_natives import (
    GetPlayerState,
    SetPlayerState,
    ConvertPlayerState,  # 新增
)
```

**Step 2: 注册 ConvertPlayerState**

在 `create_default_registry` 方法中，找到玩家状态 native 函数注册处并添加：

```python
# 注册玩家资源native函数
registry.register(GetPlayerState())
registry.register(SetPlayerState())
registry.register(ConvertPlayerState())  # 新增
```

**Step 3: 更新测试中的函数数量**

在 `tests/natives/test_factory.py` 中，将函数数量从 117 改为 118：

```python
assert len(all_funcs) == 118
```

**Step 4: 运行测试验证通过**

```bash
pytest tests/natives/test_factory.py -v
```

Expected: 测试通过

**Step 5: 提交**

```bash
git add src/jass_runner/natives/factory.py tests/natives/test_factory.py
git commit -m "feat: 注册 ConvertPlayerState native 函数"
```

---

## Task 4: 添加 playerstate 类型常量解析

**Files:**
- Modify: `src/jass_runner/vm/jass_vm.py`
- Test: `tests/integration/test_player_state.py`

**Step 1: 修改 _convert_constant_value 方法**

在 `src/jass_runner/vm/jass_vm.py` 中，找到 `_convert_constant_value` 方法，在 `alliancetype` 处理之后添加：

```python
elif const_type == 'playerstate':
    # 处理 ConvertPlayerState(0) 格式的函数调用
    try:
        import re
        match = re.search(r'ConvertPlayerState\((\d+)\)', const_value)
        if match:
            return int(match.group(1))
        else:
            return int(const_value)
    except (ValueError, AttributeError):
        return 0
```

**Step 2: 编写集成测试**

创建 `tests/integration/test_player_state_extended.py`：

```python
"""玩家状态扩展集成测试。

测试 ConvertPlayerState 和所有 playerstate 常量的使用。
"""

from jass_runner.vm.jass_vm import JassVM


class TestPlayerStateExtended:
    """测试玩家状态扩展功能。"""

    def test_player_state_constants_are_integers(self):
        """测试 playerstate 常量被正确解析为整数。"""
        vm = JassVM()

        # 检查资源状态常量
        assert vm.interpreter.global_context.variables.get(
            'PLAYER_STATE_RESOURCE_GOLD'
        ) == 1
        assert vm.interpreter.global_context.variables.get(
            'PLAYER_STATE_RESOURCE_LUMBER'
        ) == 2

        # 检查非资源状态常量
        assert vm.interpreter.global_context.variables.get(
            'PLAYER_STATE_NO_CREEP_SLEEP'
        ) == 25
        assert vm.interpreter.global_context.variables.get(
            'PLAYER_STATE_OBSERVER'
        ) == 11

    def test_convert_player_state_as_parameter(self):
        """测试 ConvertPlayerState 调用结果作为函数参数。

        这是关键测试：验证 ConvertPlayerState(25) 的返回值
        可以正确传递给 SetPlayerState 和 GetPlayerState。
        """
        jass_code = '''
function main takes nothing returns nothing
    local player p = Player(0)

    // 使用 ConvertPlayerState 返回值作为 SetPlayerState 参数
    call SetPlayerState(p, ConvertPlayerState(25), 1)

    // 使用 ConvertPlayerState 返回值作为 GetPlayerState 参数
    if GetPlayerState(p, ConvertPlayerState(25)) == 1 then
        call DisplayTextToPlayer(p, 0, 0, "No creep sleep enabled")
    endif
endfunction
'''
        vm = JassVM()
        try:
            vm.run(jass_code)
            success = True
        except Exception as e:
            print(f"Error: {e}")
            success = False

        assert success

    def test_set_and_get_non_resource_state(self):
        """测试设置和获取非资源状态。"""
        jass_code = '''
function main takes nothing returns nothing
    local player p = Player(0)

    // 设置观察者状态
    call SetPlayerState(p, PLAYER_STATE_OBSERVER, 1)

    // 验证状态已设置
    if GetPlayerState(p, PLAYER_STATE_OBSERVER) == 1 then
        call DisplayTextToPlayer(p, 0, 0, "Observer mode set")
    endif
endfunction
'''
        vm = JassVM()
        try:
            vm.run(jass_code)
            success = True
        except Exception:
            success = False

        assert success

    def test_resource_states_still_work(self):
        """测试资源状态仍然正常工作。"""
        jass_code = '''
function main takes nothing returns nothing
    local player p = Player(0)

    // 设置金币
    call SetPlayerState(p, PLAYER_STATE_RESOURCE_GOLD, 1000)

    // 验证金币
    if GetPlayerState(p, PLAYER_STATE_RESOURCE_GOLD) == 1000 then
        call DisplayTextToPlayer(p, 0, 0, "Gold set correctly")
    endif
endfunction
'''
        vm = JassVM()
        try:
            vm.run(jass_code)
            success = True
        except Exception:
            success = False

        assert success
```

**Step 3: 运行测试验证通过**

```bash
pytest tests/integration/test_player_state_extended.py -v
```

Expected: 4 个测试通过

**Step 4: 提交**

```bash
git add src/jass_runner/vm/jass_vm.py tests/integration/test_player_state_extended.py
git commit -m "feat: 添加 playerstate 类型常量解析"
```

---

## Task 5: 运行完整测试套件

**Step 1: 运行所有测试**

```bash
pytest tests/ -q
```

Expected: 所有测试通过（约 774+ 个）

**Step 2: 检查代码风格**

```bash
flake8 src/jass_runner/natives/player_state_natives.py \
       src/jass_runner/natives/handle.py \
       src/jass_runner/vm/jass_vm.py \
       tests/natives/test_player_state.py \
       tests/integration/test_player_state_extended.py
```

Expected: 无错误或警告

**Step 3: 最终提交**

```bash
git commit -m "feat: 完成 ConvertPlayerState 及扩展 PlayerState 支持

- 扩展 Player 类支持通用状态存储（_state_data 字典）
- 实现 ConvertPlayerState native 函数
- 注册 ConvertPlayerState native 函数
- 添加 playerstate 类型常量解析
- 支持 common.j 中所有 playerstate 常量
- 包含 ConvertPlayerState 作为函数参数的测试"
```

---

## 验证清单

- [ ] `ConvertPlayerState` 工作正常，返回传入的整数
- [ ] `PLAYER_STATE_NO_CREEP_SLEEP` 等常量被正确解析为整数
- [ ] `ConvertPlayerState(25)` 可作为 `SetPlayerState` 参数使用
- [ ] `ConvertPlayerState(25)` 可作为 `GetPlayerState` 参数使用
- [ ] 资源状态（GOLD, LUMBER等）仍然正常工作
- [ ] 非资源状态可以设置和获取
- [ ] 所有单元测试通过
- [ ] 所有集成测试通过
- [ ] 代码符合项目规范（中文注释、行数限制等）
