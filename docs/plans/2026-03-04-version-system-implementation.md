# Version系统实现计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 实现VersionGet和ConvertVersion native函数，支持版本检测功能。

**Architecture:** 采用简单整数常量方案，VersionGet始终返回冰封王座版本(1)，ConvertVersion直接返回传入值。

**Tech Stack:** Python, pytest

---

## Phase 1: Native函数实现

### Task 1: 创建version_natives.py并实现VersionGet

**Files:**
- Create: `src/jass_runner/natives/version_natives.py`
- Create: `tests/natives/test_version_natives.py`

**Step 1: 编写失败测试**

```python
import pytest
from unittest.mock import MagicMock
from jass_runner.natives.version_natives import VersionGet, VERSION_FROZEN_THRONE


class TestVersionGet:
    """测试VersionGet native函数。"""

    def test_version_get_returns_frozen_throne(self):
        """测试VersionGet返回冰封王座版本。"""
        # 准备
        native = VersionGet()
        mock_state = MagicMock()

        # 执行
        result = native.execute(mock_state)

        # 验证
        assert result == VERSION_FROZEN_THRONE
        assert result == 1
```

**Step 2: 运行测试验证失败**

```bash
pytest tests/natives/test_version_natives.py::TestVersionGet::test_version_get_returns_frozen_throne -v
```

Expected: FAIL - VersionGet未定义

**Step 3: 实现VersionGet**

创建 `src/jass_runner/natives/version_natives.py`：

```python
"""版本相关 native 函数实现。

此模块包含与游戏版本相关的 JASS native 函数。
"""

import logging
from .base import NativeFunction

logger = logging.getLogger(__name__)

# 版本常量
VERSION_REIGN_OF_CHAOS = 0   # 混乱之治
VERSION_FROZEN_THRONE = 1    # 冰封王座


class VersionGet(NativeFunction):
    """获取当前游戏版本。

    在本模拟器中，始终返回冰封王座版本。
    """

    @property
    def name(self) -> str:
        return "VersionGet"

    def execute(self, state_context) -> int:
        """获取当前游戏版本。

        参数：
            state_context: 状态上下文

        返回：
            VERSION_FROZEN_THRONE (1)
        """
        logger.info("[VersionGet] 返回游戏版本: 冰封王座 (1)")
        return VERSION_FROZEN_THRONE
```

**Step 4: 运行测试验证通过**

```bash
pytest tests/natives/test_version_natives.py::TestVersionGet::test_version_get_returns_frozen_throne -v
```

Expected: PASS

**Step 5: Commit**

```bash
git add tests/natives/test_version_natives.py src/jass_runner/natives/version_natives.py
git commit -m "feat(version): 实现VersionGet native函数"
```

---

### Task 2: 实现ConvertVersion

**Files:**
- Modify: `src/jass_runner/natives/version_natives.py`
- Modify: `tests/natives/test_version_natives.py`

**Step 1: 编写失败测试**

在 `test_version_natives.py` 中添加：

```python
class TestConvertVersion:
    """测试ConvertVersion native函数。"""

    def test_convert_version_returns_input(self):
        """测试ConvertVersion返回传入的值。"""
        # 准备
        native = ConvertVersion()
        mock_state = MagicMock()

        # 执行
        result = native.execute(mock_state, 0)

        # 验证
        assert result == 0

    def test_convert_version_with_frozen_throne(self):
        """测试ConvertVersion处理冰封王座版本。"""
        # 准备
        native = ConvertVersion()
        mock_state = MagicMock()

        # 执行
        result = native.execute(mock_state, VERSION_FROZEN_THRONE)

        # 验证
        assert result == VERSION_FROZEN_THRONE
        assert result == 1
```

**Step 2: 运行测试验证失败**

```bash
pytest tests/natives/test_version_natives.py::TestConvertVersion -v
```

Expected: FAIL - ConvertVersion未定义

**Step 3: 实现ConvertVersion**

在 `version_natives.py` 中添加：

```python
class ConvertVersion(NativeFunction):
    """转换版本类型。

    在本实现中，直接返回传入的版本值。
    """

    @property
    def name(self) -> str:
        return "ConvertVersion"

    def execute(self, state_context, version: int) -> int:
        """转换版本类型。

        参数：
            state_context: 状态上下文
            version: 版本整数值

        返回：
            传入的版本值
        """
        logger.info(f"[ConvertVersion] 转换版本: {version}")
        return version
```

**Step 4: 运行测试验证通过**

```bash
pytest tests/natives/test_version_natives.py::TestConvertVersion -v
```

Expected: PASS

**Step 5: Commit**

```bash
git add tests/natives/test_version_natives.py src/jass_runner/natives/version_natives.py
git commit -m "feat(version): 实现ConvertVersion native函数"
```

---

## Phase 2: 注册和集成

### Task 3: 在工厂中注册Version native函数

**Files:**
- Modify: `src/jass_runner/natives/factory.py`

**Step 1: 添加导入**

在文件顶部添加：

```python
from .version_natives import (
    VersionGet,
    ConvertVersion,
    VERSION_REIGN_OF_CHAOS,
    VERSION_FROZEN_THRONE,
)
```

**Step 2: 在create_default_registry中注册**

在方法末尾（return registry之前）添加：

```python
        # 注册版本相关 native 函数
        registry.register(VersionGet())
        registry.register(ConvertVersion())
```

**Step 3: 运行所有version相关测试**

```bash
pytest tests/natives/test_version_natives.py -v
```

Expected: 所有测试PASS

**Step 4: Commit**

```bash
git add src/jass_runner/natives/factory.py
git commit -m "feat(version): 在工厂中注册Version相关native函数"
```

---

## Phase 3: 验证

### Task 4: 运行所有测试

**Step 1: 运行所有version相关测试**

```bash
pytest tests/natives/test_version_natives.py -v
```

Expected: 所有测试PASS

**Step 2: 运行完整测试套件**

```bash
pytest
```

Expected: 所有测试PASS

**Step 3: 更新factory测试中的函数数量统计**

如果 `tests/natives/test_factory.py` 中的 `test_create_default_registry` 测试失败（函数数量不匹配），更新断言：

```python
assert len(all_funcs) == 145  # 143 + 2 (version)
```

然后提交：

```bash
git add tests/natives/test_factory.py
git commit -m "test: 更新native函数数量统计以包含version函数"
```

**Step 4: 最终提交**

```bash
git log --oneline -5
```

确认所有提交都已记录。

---

## 总结

实现完成后，项目将支持以下JASS代码：

```jass
globals
    integer bj_gameVersion
endglobals

function InitGlobals takes nothing returns nothing
    set bj_gameVersion = VersionGet()
endfunction
```

**实现文件清单：**
- `src/jass_runner/natives/version_natives.py` - VersionGet和ConvertVersion实现
- `src/jass_runner/natives/factory.py` - 注册新的native函数
- `tests/natives/test_version_natives.py` - 单元测试
