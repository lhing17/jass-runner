# TimerDialog Native 函数实现计划

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 实现 timerdialog handle 类型和 5 个核心 native 函数（CreateTimerDialog, DestroyTimerDialog, TimerDialogSetTitle, TimerDialogDisplay, IsTimerDialogDisplayed）

**Architecture:** 遵循现有 handle 和 native 函数模式：TimerDialog 继承 Handle 基类，native 函数继承 NativeFunction 基类，通过 HandleManager 管理生命周期，在 NativeFactory 注册。

**Tech Stack:** Python 3.8+, 使用项目现有的 logging 模块记录操作。

---

## 文件结构

| 文件 | 操作 | 说明 |
|------|------|------|
| `src/jass_runner/natives/timerdialog.py` | 创建 | TimerDialog handle 类定义 |
| `src/jass_runner/natives/timerdialog_natives.py` | 创建 | 5 个 native 函数实现 |
| `src/jass_runner/natives/manager.py` | 修改 | 添加 create_timerdialog 和 get_timerdialog 方法 |
| `src/jass_runner/natives/factory.py` | 修改 | 导入并注册 timerdialog native 函数 |
| `src/jass_runner/natives/handle.py` | 修改 | 导入并导出 TimerDialog |
| `tests/natives/test_timerdialog_natives.py` | 创建 | 单元测试 |

---

## Chunk 1: TimerDialog Handle 类

### Task 1: 创建 TimerDialog handle 类

**Files:**
- Create: `src/jass_runner/natives/timerdialog.py`

- [ ] **Step 1: 创建 TimerDialog 类**

```python
"""TimerDialog handle 类。

此模块包含 TimerDialog 类，用于表示 JASS 中的 timerdialog 类型。
"""

from .handle_base import Handle


class TimerDialog(Handle):
    """计时器对话框 handle。

    属性：
        timer: 关联的 timer 对象
        title: 对话框标题
        displayed: 是否显示
    """

    def __init__(self, handle_id: str, timer):
        """初始化 TimerDialog。

        参数：
            handle_id: 唯一标识符
            timer: 关联的 timer 对象
        """
        super().__init__(handle_id, "timerdialog")
        self.timer = timer
        self.title = ""
        self.displayed = False
```

- [ ] **Step 2: 提交**

```bash
git add src/jass_runner/natives/timerdialog.py
git commit -m "feat: 添加 TimerDialog handle 类"
```

---

## Chunk 2: HandleManager 扩展

### Task 2: 扩展 HandleManager 支持 timerdialog

**Files:**
- Modify: `src/jass_runner/natives/manager.py`

- [ ] **Step 1: 导入 TimerDialog**

在文件顶部（第8行附近）添加导入：

```python
from .handle import Handle, Unit, Player, Item, Group, Rect, Effect, BoolExpr, Sound
from .hashtable import Hashtable
from .event_handles import PlayerUnitEvent, PlayerEvent, GameEvent, UnitEvent
from .timerdialog import TimerDialog  # 新增
```

- [ ] **Step 2: 添加 create_timerdialog 方法**

在文件末尾（get_unitevent 方法之后）添加：

```python
    def create_timerdialog(self, timer) -> TimerDialog:
        """创建 timerdialog 并返回。

        参数：
            timer: 关联的 timer 对象

        返回：
            创建的 TimerDialog 对象
        """
        handle_id = f"timerdialog_{self._generate_id()}"
        timerdialog = TimerDialog(handle_id, timer)
        self._register_handle(timerdialog)
        return timerdialog

    def get_timerdialog(self, handle_id: str) -> Optional[TimerDialog]:
        """获取 timerdialog 对象，进行类型检查。

        参数：
            handle_id: timerdialog ID

        返回：
            TimerDialog 对象，如果不存在或类型不匹配返回 None
        """
        handle = self.get_handle(handle_id)
        if isinstance(handle, TimerDialog):
            return handle
        return None
```

- [ ] **Step 3: 提交**

```bash
git add src/jass_runner/natives/manager.py
git commit -m "feat: HandleManager 添加 timerdialog 支持"
```

---

## Chunk 3: TimerDialog Native 函数

### Task 3: 创建 5 个 native 函数

**Files:**
- Create: `src/jass_runner/natives/timerdialog_natives.py`

- [ ] **Step 1: 创建 native 函数文件**

```python
"""TimerDialog 相关的 native 函数。

此模块包含与 timerdialog 相关的 JASS native 函数实现。
"""

import logging
from ..natives.base import NativeFunction


logger = logging.getLogger(__name__)


class CreateTimerDialog(NativeFunction):
    """创建 timerdialog，关联指定 timer。"""

    @property
    def name(self) -> str:
        return "CreateTimerDialog"

    def execute(self, state_context, timer, *args):
        """执行 CreateTimerDialog native 函数。

        参数：
            state_context: 状态上下文
            timer: 关联的 timer 对象

        返回：
            创建的 TimerDialog 对象
        """
        timerdialog = state_context.handle_manager.create_timerdialog(timer)
        timer_id = timer.id if hasattr(timer, 'id') else str(timer)
        logger.info(f"[CreateTimerDialog] 创建 timerdialog: {timerdialog.id} (关联 timer: {timer_id})")
        return timerdialog


class DestroyTimerDialog(NativeFunction):
    """销毁 timerdialog。"""

    @property
    def name(self) -> str:
        return "DestroyTimerDialog"

    def execute(self, state_context, timerdialog, *args):
        """执行 DestroyTimerDialog native 函数。

        参数：
            state_context: 状态上下文
            timerdialog: TimerDialog 对象

        返回：
            bool: 是否成功销毁
        """
        if not timerdialog:
            logger.warning("[DestroyTimerDialog] 无效的 timerdialog")
            return False

        handle_id = timerdialog.id if hasattr(timerdialog, 'id') else str(timerdialog)
        success = state_context.handle_manager.destroy_handle(handle_id)
        if success:
            logger.info(f"[DestroyTimerDialog] 销毁 timerdialog: {handle_id}")
        else:
            logger.warning(f"[DestroyTimerDialog] 未找到 timerdialog: {handle_id}")
        return success


class TimerDialogSetTitle(NativeFunction):
    """设置 timerdialog 标题。"""

    @property
    def name(self) -> str:
        return "TimerDialogSetTitle"

    def execute(self, state_context, timerdialog, title, *args):
        """执行 TimerDialogSetTitle native 函数。

        参数：
            state_context: 状态上下文
            timerdialog: TimerDialog 对象
            title: 标题字符串

        返回：
            bool: 是否成功设置
        """
        if not timerdialog:
            logger.warning("[TimerDialogSetTitle] 无效的 timerdialog")
            return False

        timerdialog.title = title
        handle_id = timerdialog.id if hasattr(timerdialog, 'id') else str(timerdialog)
        logger.info(f"[TimerDialogSetTitle] 设置 timerdialog {handle_id} 标题为: \"{title}\"")
        return True


class TimerDialogDisplay(NativeFunction):
    """设置 timerdialog 显示/隐藏。"""

    @property
    def name(self) -> str:
        return "TimerDialogDisplay"

    def execute(self, state_context, timerdialog, display, *args):
        """执行 TimerDialogDisplay native 函数。

        参数：
            state_context: 状态上下文
            timerdialog: TimerDialog 对象
            display: 是否显示（布尔值）

        返回：
            bool: 是否成功设置
        """
        if not timerdialog:
            logger.warning("[TimerDialogDisplay] 无效的 timerdialog")
            return False

        timerdialog.displayed = display
        handle_id = timerdialog.id if hasattr(timerdialog, 'id') else str(timerdialog)
        action = "显示" if display else "隐藏"
        logger.info(f"[TimerDialogDisplay] {action} timerdialog: {handle_id}")
        return True


class IsTimerDialogDisplayed(NativeFunction):
    """检查 timerdialog 是否显示。"""

    @property
    def name(self) -> str:
        return "IsTimerDialogDisplayed"

    def execute(self, state_context, timerdialog, *args):
        """执行 IsTimerDialogDisplayed native 函数。

        参数：
            state_context: 状态上下文
            timerdialog: TimerDialog 对象

        返回：
            bool: 是否显示
        """
        if not timerdialog:
            logger.warning("[IsTimerDialogDisplayed] 无效的 timerdialog")
            return False

        return timerdialog.displayed
```

- [ ] **Step 2: 提交**

```bash
git add src/jass_runner/natives/timerdialog_natives.py
git commit -m "feat: 添加 TimerDialog 相关 native 函数"
```

---

## Chunk 4: NativeFactory 注册

### Task 4: 在 NativeFactory 注册 native 函数

**Files:**
- Modify: `src/jass_runner/natives/factory.py`

- [ ] **Step 1: 导入 native 函数**

在文件顶部（第10行附近）添加导入：

```python
from .timer_natives import CreateTimer, TimerStart, TimerGetElapsed, DestroyTimer, PauseTimer, ResumeTimer
from .timerdialog_natives import (
    CreateTimerDialog,
    DestroyTimerDialog,
    TimerDialogSetTitle,
    TimerDialogDisplay,
    IsTimerDialogDisplayed,
)
from .trigger_natives import (
```

- [ ] **Step 2: 注册 native 函数**

在 `create_default_registry` 方法中，timer natives 注册之后（第265行附近）添加：

```python
        # 如果计时器系统可用，注册计时器原生函数
        if self._timer_system:
            registry.register(CreateTimer(self._timer_system))
            registry.register(TimerStart(self._timer_system))
            registry.register(TimerGetElapsed(self._timer_system))
            registry.register(DestroyTimer(self._timer_system))
            registry.register(PauseTimer(self._timer_system))
            registry.register(ResumeTimer(self._timer_system))

            # 注册 timerdialog 原生函数
            registry.register(CreateTimerDialog())
            registry.register(DestroyTimerDialog())
            registry.register(TimerDialogSetTitle())
            registry.register(TimerDialogDisplay())
            registry.register(IsTimerDialogDisplayed())
```

- [ ] **Step 3: 提交**

```bash
git add src/jass_runner/natives/factory.py
git commit -m "feat: 在 NativeFactory 注册 TimerDialog native 函数"
```

---

## Chunk 5: Handle 导出

### Task 5: 在 handle.py 导出 TimerDialog

**Files:**
- Modify: `src/jass_runner/natives/handle.py`

- [ ] **Step 1: 导入 TimerDialog**

在文件顶部（第9行附近）添加导入：

```python
from .handle_base import Handle
from .unit import Unit
from .player import Player
from .item import Item
from .group import Group
from .rect import Rect
from .effect import Effect
from .force import Force
from .boolexpr import BoolExpr, ConditionFunc, FilterFunc, AndExpr, OrExpr, NotExpr
from .timerdialog import TimerDialog  # 新增
```

- [ ] **Step 2: 更新 __all__**

在 `__all__` 列表末尾添加：

```python
__all__ = [
    "Handle",
    "Unit",
    "Player",
    "Item",
    "Group",
    "Rect",
    "Effect",
    "Force",
    "BoolExpr",
    "ConditionFunc",
    "FilterFunc",
    "AndExpr",
    "OrExpr",
    "NotExpr",
    "Sound",
    "TimerDialog",  # 新增
]
```

- [ ] **Step 3: 提交**

```bash
git add src/jass_runner/natives/handle.py
git commit -m "feat: 在 handle 模块导出 TimerDialog"
```

---

## Chunk 6: 单元测试

### Task 6: 编写单元测试

**Files:**
- Create: `tests/natives/test_timerdialog_natives.py`

- [ ] **Step 1: 创建测试文件**

```python
"""TimerDialog native 函数测试。"""

import pytest
from unittest.mock import MagicMock, patch
from jass_runner.natives.timerdialog import TimerDialog
from jass_runner.natives.timerdialog_natives import (
    CreateTimerDialog,
    DestroyTimerDialog,
    TimerDialogSetTitle,
    TimerDialogDisplay,
    IsTimerDialogDisplayed,
)


class TestCreateTimerDialog:
    """测试 CreateTimerDialog native 函数。"""

    def test_create_timer_dialog(self):
        """测试创建 timerdialog。"""
        native = CreateTimerDialog()
        state_context = MagicMock()
        mock_timer = MagicMock()
        mock_timer.id = "timer_1"

        mock_timerdialog = MagicMock()
        mock_timerdialog.id = "timerdialog_1"
        state_context.handle_manager.create_timerdialog.return_value = mock_timerdialog

        result = native.execute(state_context, mock_timer)

        assert result == mock_timerdialog
        state_context.handle_manager.create_timerdialog.assert_called_once_with(mock_timer)


class TestDestroyTimerDialog:
    """测试 DestroyTimerDialog native 函数。"""

    def test_destroy_timer_dialog_success(self):
        """测试成功销毁 timerdialog。"""
        native = DestroyTimerDialog()
        state_context = MagicMock()
        mock_timerdialog = MagicMock()
        mock_timerdialog.id = "timerdialog_1"
        state_context.handle_manager.destroy_handle.return_value = True

        result = native.execute(state_context, mock_timerdialog)

        assert result is True
        state_context.handle_manager.destroy_handle.assert_called_once_with("timerdialog_1")

    def test_destroy_timer_dialog_invalid(self):
        """测试销毁无效的 timerdialog。"""
        native = DestroyTimerDialog()
        state_context = MagicMock()

        result = native.execute(state_context, None)

        assert result is False


class TestTimerDialogSetTitle:
    """测试 TimerDialogSetTitle native 函数。"""

    def test_set_title_success(self):
        """测试成功设置标题。"""
        native = TimerDialogSetTitle()
        state_context = MagicMock()
        mock_timerdialog = MagicMock()
        mock_timerdialog.id = "timerdialog_1"

        result = native.execute(state_context, mock_timerdialog, "游戏时间")

        assert result is True
        assert mock_timerdialog.title == "游戏时间"

    def test_set_title_invalid_timerdialog(self):
        """测试设置无效 timerdialog 的标题。"""
        native = TimerDialogSetTitle()
        state_context = MagicMock()

        result = native.execute(state_context, None, "游戏时间")

        assert result is False


class TestTimerDialogDisplay:
    """测试 TimerDialogDisplay native 函数。"""

    def test_display_show(self):
        """测试显示 timerdialog。"""
        native = TimerDialogDisplay()
        state_context = MagicMock()
        mock_timerdialog = MagicMock()
        mock_timerdialog.id = "timerdialog_1"

        result = native.execute(state_context, mock_timerdialog, True)

        assert result is True
        assert mock_timerdialog.displayed is True

    def test_display_hide(self):
        """测试隐藏 timerdialog。"""
        native = TimerDialogDisplay()
        state_context = MagicMock()
        mock_timerdialog = MagicMock()
        mock_timerdialog.id = "timerdialog_1"

        result = native.execute(state_context, mock_timerdialog, False)

        assert result is True
        assert mock_timerdialog.displayed is False

    def test_display_invalid_timerdialog(self):
        """测试显示无效的 timerdialog。"""
        native = TimerDialogDisplay()
        state_context = MagicMock()

        result = native.execute(state_context, None, True)

        assert result is False


class TestIsTimerDialogDisplayed:
    """测试 IsTimerDialogDisplayed native 函数。"""

    def test_is_displayed_true(self):
        """测试检查 timerdialog 显示状态为 true。"""
        native = IsTimerDialogDisplayed()
        state_context = MagicMock()
        mock_timerdialog = MagicMock()
        mock_timerdialog.displayed = True

        result = native.execute(state_context, mock_timerdialog)

        assert result is True

    def test_is_displayed_false(self):
        """测试检查 timerdialog 显示状态为 false。"""
        native = IsTimerDialogDisplayed()
        state_context = MagicMock()
        mock_timerdialog = MagicMock()
        mock_timerdialog.displayed = False

        result = native.execute(state_context, mock_timerdialog)

        assert result is False

    def test_is_displayed_invalid(self):
        """测试检查无效 timerdialog 的显示状态。"""
        native = IsTimerDialogDisplayed()
        state_context = MagicMock()

        result = native.execute(state_context, None)

        assert result is False


class TestTimerDialogClass:
    """测试 TimerDialog 类。"""

    def test_timerdialog_creation(self):
        """测试 TimerDialog 创建。"""
        mock_timer = MagicMock()
        timerdialog = TimerDialog("timerdialog_1", mock_timer)

        assert timerdialog.id == "timerdialog_1"
        assert timerdialog.type_name == "timerdialog"
        assert timerdialog.timer == mock_timer
        assert timerdialog.title == ""
        assert timerdialog.displayed is False
        assert timerdialog.alive is True

    def test_timerdialog_destroy(self):
        """测试 TimerDialog 销毁。"""
        mock_timer = MagicMock()
        timerdialog = TimerDialog("timerdialog_1", mock_timer)

        timerdialog.destroy()

        assert timerdialog.alive is False
```

- [ ] **Step 2: 运行测试**

```bash
pytest tests/natives/test_timerdialog_natives.py -v
```

预期输出：所有测试通过

- [ ] **Step 3: 提交**

```bash
git add tests/natives/test_timerdialog_natives.py
git commit -m "test: 添加 TimerDialog native 函数单元测试"
```

---

## Chunk 7: 集成验证

### Task 7: 运行完整测试套件

- [ ] **Step 1: 运行所有测试**

```bash
pytest tests/ -x -v
```

预期输出：所有测试通过（包括新的 timerdialog 测试）

- [ ] **Step 2: 提交（如有需要）**

---

## 验证清单

- [ ] TimerDialog handle 类已创建
- [ ] HandleManager 支持 create_timerdialog 和 get_timerdialog
- [ ] 5 个 native 函数已实现（CreateTimerDialog, DestroyTimerDialog, TimerDialogSetTitle, TimerDialogDisplay, IsTimerDialogDisplayed）
- [ ] NativeFactory 已注册所有 native 函数
- [ ] handle.py 已导出 TimerDialog
- [ ] 单元测试全部通过
- [ ] 完整测试套件通过
