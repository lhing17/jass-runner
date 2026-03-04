# Fog Native 函数实现计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 实现 Fog 相关的 native 函数（FogMaskEnable, FogEnable, IsFogMaskEnabled, IsFogEnabled）

**Architecture:** 创建独立的 `fog_natives.py` 模块，包含 `FogState` 状态管理类和四个 native 函数类。状态默认启用，函数调用时记录日志。

**Tech Stack:** Python 3.8+, pytest, 项目自定义的 NativeFunction 框架

---

## 前置知识

### Native 函数实现模式

参考现有实现（如 `camera.py`），每个 native 函数需要：

1. 继承 `NativeFunction` 基类
2. 定义 `name` 属性（函数名）
3. 定义 `parameters` 属性（参数列表）
4. 定义 `return_type` 属性（返回值类型）
5. 实现 `execute` 方法（执行逻辑）

### 状态管理

`FogState` 类将存储两个布尔值：
- `mask_enabled`: 黑色遮罩状态
- `fog_enabled`: 战争迷雾状态

状态实例将作为类变量或全局状态管理。

---

### Task 1: 创建 FogState 状态管理类

**Files:**
- Create: `src/jass_runner/natives/fog_natives.py`
- Test: `tests/natives/test_fog_natives.py`

**Step 1: 编写失败测试**

```python
def test_fog_state_default_values():
    """测试 FogState 默认值为启用状态。"""
    from jass_runner.natives.fog_natives import FogState

    state = FogState()

    assert state.mask_enabled is True
    assert state.fog_enabled is True
```

**Step 2: 运行测试验证失败**

Run: `pytest tests/natives/test_fog_natives.py::test_fog_state_default_values -v`
Expected: FAIL with "ModuleNotFoundError" 或 "ImportError"

**Step 3: 编写最小实现**

在 `src/jass_runner/natives/fog_natives.py` 中：

```python
"""Fog native 函数实现。

此模块包含战争迷雾相关的 native 函数。
"""

from typing import Any, List
from .base import NativeFunction


class FogState:
    """管理战争迷雾状态。"""

    def __init__(self):
        """初始化迷雾状态，默认为启用。"""
        self.mask_enabled = True
        self.fog_enabled = True
```

**Step 4: 运行测试验证通过**

Run: `pytest tests/natives/test_fog_natives.py::test_fog_state_default_values -v`
Expected: PASS

**Step 5: 提交**

```bash
git add tests/natives/test_fog_natives.py src/jass_runner/natives/fog_natives.py
git commit -m "feat: 添加 FogState 状态管理类"
```

---

### Task 2: 实现 FogMaskEnable native 函数

**Files:**
- Modify: `src/jass_runner/natives/fog_natives.py`
- Test: `tests/natives/test_fog_natives.py`

**Step 1: 编写失败测试**

```python
def test_fog_mask_enable_sets_state():
    """测试 FogMaskEnable 设置黑色遮罩状态。"""
    from jass_runner.natives.fog_natives import FogMaskEnable, FogState

    state = FogState()
    native = FogMaskEnable(state)

    # 禁用遮罩
    native.execute([False])
    assert state.mask_enabled is False

    # 启用遮罩
    native.execute([True])
    assert state.mask_enabled is True
```

**Step 2: 运行测试验证失败**

Run: `pytest tests/natives/test_fog_natives.py::test_fog_mask_enable_sets_state -v`
Expected: FAIL with "FogMaskEnable not defined"

**Step 3: 编写最小实现**

在 `src/jass_runner/natives/fog_natives.py` 中添加：

```python
class FogMaskEnable(NativeFunction):
    """启用或禁用黑色遮罩。"""

    name = "FogMaskEnable"
    parameters = ["boolean"]
    return_type = "nothing"

    def __init__(self, fog_state: FogState):
        """初始化。

        参数：
            fog_state: 迷雾状态管理器
        """
        self._fog_state = fog_state

    def execute(self, args: List[Any]) -> None:
        """执行函数。

        参数：
            args: [enable] - 是否启用黑色遮罩
        """
        enable = args[0]
        self._fog_state.mask_enabled = enable
        status = "启用" if enable else "禁用"
        print(f"[Fog] 黑色遮罩状态: {status}")
```

**Step 4: 运行测试验证通过**

Run: `pytest tests/natives/test_fog_natives.py::test_fog_mask_enable_sets_state -v`
Expected: PASS

**Step 5: 提交**

```bash
git add tests/natives/test_fog_natives.py src/jass_runner/natives/fog_natives.py
git commit -m "feat: 实现 FogMaskEnable native 函数"
```

---

### Task 3: 实现 FogEnable native 函数

**Files:**
- Modify: `src/jass_runner/natives/fog_natives.py`
- Test: `tests/natives/test_fog_natives.py`

**Step 1: 编写失败测试**

```python
def test_fog_enable_sets_state():
    """测试 FogEnable 设置战争迷雾状态。"""
    from jass_runner.natives.fog_natives import FogEnable, FogState

    state = FogState()
    native = FogEnable(state)

    # 禁用迷雾
    native.execute([False])
    assert state.fog_enabled is False

    # 启用迷雾
    native.execute([True])
    assert state.fog_enabled is True
```

**Step 2: 运行测试验证失败**

Run: `pytest tests/natives/test_fog_natives.py::test_fog_enable_sets_state -v`
Expected: FAIL with "FogEnable not defined"

**Step 3: 编写最小实现**

在 `src/jass_runner/natives/fog_natives.py` 中添加：

```python
class FogEnable(NativeFunction):
    """启用或禁用战争迷雾。"""

    name = "FogEnable"
    parameters = ["boolean"]
    return_type = "nothing"

    def __init__(self, fog_state: FogState):
        """初始化。

        参数：
            fog_state: 迷雾状态管理器
        """
        self._fog_state = fog_state

    def execute(self, args: List[Any]) -> None:
        """执行函数。

        参数：
            args: [enable] - 是否启用战争迷雾
        """
        enable = args[0]
        self._fog_state.fog_enabled = enable
        status = "启用" if enable else "禁用"
        print(f"[Fog] 战争迷雾状态: {status}")
```

**Step 4: 运行测试验证通过**

Run: `pytest tests/natives/test_fog_natives.py::test_fog_enable_sets_state -v`
Expected: PASS

**Step 5: 提交**

```bash
git add tests/natives/test_fog_natives.py src/jass_runner/natives/fog_natives.py
git commit -m "feat: 实现 FogEnable native 函数"
```

---

### Task 4: 实现 IsFogMaskEnabled native 函数

**Files:**
- Modify: `src/jass_runner/natives/fog_natives.py`
- Test: `tests/natives/test_fog_natives.py`

**Step 1: 编写失败测试**

```python
def test_is_fog_mask_enabled_returns_state():
    """测试 IsFogMaskEnabled 返回黑色遮罩状态。"""
    from jass_runner.natives.fog_natives import IsFogMaskEnabled, FogState

    state = FogState()
    native = IsFogMaskEnabled(state)

    # 默认启用
    result = native.execute([])
    assert result is True

    # 禁用后查询
    state.mask_enabled = False
    result = native.execute([])
    assert result is False
```

**Step 2: 运行测试验证失败**

Run: `pytest tests/natives/test_fog_natives.py::test_is_fog_mask_enabled_returns_state -v`
Expected: FAIL with "IsFogMaskEnabled not defined"

**Step 3: 编写最小实现**

在 `src/jass_runner/natives/fog_natives.py` 中添加：

```python
class IsFogMaskEnabled(NativeFunction):
    """查询黑色遮罩是否启用。"""

    name = "IsFogMaskEnabled"
    parameters = []
    return_type = "boolean"

    def __init__(self, fog_state: FogState):
        """初始化。

        参数：
            fog_state: 迷雾状态管理器
        """
        self._fog_state = fog_state

    def execute(self, args: List[Any]) -> bool:
        """执行函数。

        参数：
            args: 无参数

        返回：
            黑色遮罩是否启用
        """
        return self._fog_state.mask_enabled
```

**Step 4: 运行测试验证通过**

Run: `pytest tests/natives/test_fog_natives.py::test_is_fog_mask_enabled_returns_state -v`
Expected: PASS

**Step 5: 提交**

```bash
git add tests/natives/test_fog_natives.py src/jass_runner/natives/fog_natives.py
git commit -m "feat: 实现 IsFogMaskEnabled native 函数"
```

---

### Task 5: 实现 IsFogEnabled native 函数

**Files:**
- Modify: `src/jass_runner/natives/fog_natives.py`
- Test: `tests/natives/test_fog_natives.py`

**Step 1: 编写失败测试**

```python
def test_is_fog_enabled_returns_state():
    """测试 IsFogEnabled 返回战争迷雾状态。"""
    from jass_runner.natives.fog_natives import IsFogEnabled, FogState

    state = FogState()
    native = IsFogEnabled(state)

    # 默认启用
    result = native.execute([])
    assert result is True

    # 禁用后查询
    state.fog_enabled = False
    result = native.execute([])
    assert result is False
```

**Step 2: 运行测试验证失败**

Run: `pytest tests/natives/test_fog_natives.py::test_is_fog_enabled_returns_state -v`
Expected: FAIL with "IsFogEnabled not defined"

**Step 3: 编写最小实现**

在 `src/jass_runner/natives/fog_natives.py` 中添加：

```python
class IsFogEnabled(NativeFunction):
    """查询战争迷雾是否启用。"""

    name = "IsFogEnabled"
    parameters = []
    return_type = "boolean"

    def __init__(self, fog_state: FogState):
        """初始化。

        参数：
            fog_state: 迷雾状态管理器
        """
        self._fog_state = fog_state

    def execute(self, args: List[Any]) -> bool:
        """执行函数。

        参数：
            args: 无参数

        返回：
            战争迷雾是否启用
        """
        return self._fog_state.fog_enabled
```

**Step 4: 运行测试验证通过**

Run: `pytest tests/natives/test_fog_natives.py::test_is_fog_enabled_returns_state -v`
Expected: PASS

**Step 5: 提交**

```bash
git add tests/natives/test_fog_natives.py src/jass_runner/natives/fog_natives.py
git commit -m "feat: 实现 IsFogEnabled native 函数"
```

---

### Task 6: 在工厂中注册 Fog native 函数

**Files:**
- Modify: `src/jass_runner/natives/factory.py`
- Test: `tests/natives/test_fog_natives.py`（集成测试）

**Step 1: 编写失败测试**

```python
def test_fog_natives_registered_in_factory():
    """测试 Fog native 函数在工厂中被注册。"""
    from jass_runner.natives.factory import NativeFactory

    factory = NativeFactory()
    registry = factory.create_default_registry()

    # 验证所有函数都被注册
    assert registry.get("FogMaskEnable") is not None
    assert registry.get("FogEnable") is not None
    assert registry.get("IsFogMaskEnabled") is not None
    assert registry.get("IsFogEnabled") is not None
```

**Step 2: 运行测试验证失败**

Run: `pytest tests/natives/test_fog_natives.py::test_fog_natives_registered_in_factory -v`
Expected: FAIL with "FogMaskEnable not found in registry"

**Step 3: 编写实现**

在 `src/jass_runner/natives/factory.py` 中：

1. 添加导入：
```python
from .fog_natives import FogState, FogMaskEnable, FogEnable, IsFogMaskEnabled, IsFogEnabled
```

2. 在 `__init__` 中添加状态初始化：
```python
def __init__(self, timer_system=None):
    """初始化工厂。

    参数：
        timer_system: 可选的计时器系统实例
    """
    self._timer_system = timer_system
    self._fog_state = FogState()  # 添加这行
```

3. 在 `create_default_registry` 方法末尾（return 之前）添加注册：
```python
# 注册 Fog native 函数
registry.register(FogMaskEnable(self._fog_state))
registry.register(FogEnable(self._fog_state))
registry.register(IsFogMaskEnabled(self._fog_state))
registry.register(IsFogEnabled(self._fog_state))
```

**Step 4: 运行测试验证通过**

Run: `pytest tests/natives/test_fog_natives.py::test_fog_natives_registered_in_factory -v`
Expected: PASS

**Step 5: 提交**

```bash
git add tests/natives/test_fog_natives.py src/jass_runner/natives/factory.py
git commit -m "feat: 在工厂中注册 Fog native 函数"
```

---

### Task 7: 运行所有测试

**Step 1: 运行完整测试套件**

Run: `pytest tests/natives/test_fog_natives.py -v`
Expected: 所有测试 PASS

**Step 2: 运行项目整体测试**

Run: `pytest`
Expected: 所有测试 PASS

**Step 3: 提交**

```bash
git add .
git commit -m "test: 完成 Fog native 函数所有测试"
```

---

## 完成检查清单

- [x] FogState 状态管理类
- [x] FogMaskEnable native 函数
- [x] FogEnable native 函数
- [x] IsFogMaskEnabled native 函数
- [x] IsFogEnabled native 函数
- [x] 在工厂中注册所有函数
- [x] 所有单元测试通过
- [x] 整体测试套件通过
