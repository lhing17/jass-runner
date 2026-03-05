# Rect Native 函数实现计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 实现 Rect 类型的核心 native 函数（9个），支持创建、修改和查询矩形区域。

**Architecture:** 基于现有 HandleManager 和 Rect 类，实现构造函数（Rect, RemoveRect）、修改函数（SetRect, MoveRectTo）和查询函数（GetRectCenterX/Y, GetRectMinX/Y, GetRectMaxX/Y）。

**Tech Stack:** Python 3.8+, pytest, 现有 JASS Runner 框架

---

## 前置知识

### 相关文件位置
- `src/jass_runner/natives/rect.py` - Rect 类定义
- `src/jass_runner/natives/manager.py` - HandleManager
- `src/jass_runner/natives/state.py` - StateContext
- `src/jass_runner/natives/factory.py` - NativeFactory
- `docs/plans/2026-03-05-rect-natives-design.md` - 详细设计文档

### 现有代码参考
- `src/jass_runner/natives/camera.py` - native 函数实现模式
- `src/jass_runner/natives/location.py` - Location native 函数实现模式

---

## Task 1: 创建 Rect 和 RemoveRect native 函数

**Files:**
- Create: `src/jass_runner/natives/rect_natives.py`
- Test: `tests/natives/test_rect_natives.py`

**Step 1: 编写失败测试**

```python
"""Rect native 函数测试。"""

import pytest
from unittest.mock import Mock

from jass_runner.natives.rect_natives import Rect, RemoveRect
from jass_runner.natives.rect import Rect as RectClass


class TestRect:
    """测试 Rect native 函数。"""

    def test_name_is_correct(self):
        """测试函数名称正确。"""
        native = Rect()
        assert native.name == "Rect"

    def test_execute_creates_rect(self):
        """测试执行创建 Rect。"""
        native = Rect()

        mock_state_context = Mock()
        mock_handle_manager = Mock()
        mock_handle_manager.create_handle.return_value = "rect_001"
        mock_state_context.handle_manager = mock_handle_manager

        result = native.execute(mock_state_context, -100.0, -100.0, 100.0, 100.0)

        assert result == "rect_001"
        mock_handle_manager.create_handle.assert_called_once()
        call_args = mock_handle_manager.create_handle.call_args
        assert call_args[0][1] == "rect"

    def test_execute_without_handle_manager(self):
        """测试没有 handle_manager 时返回 None。"""
        native = Rect()

        mock_state_context = Mock()
        del mock_state_context.handle_manager

        result = native.execute(mock_state_context, -100.0, -100.0, 100.0, 100.0)

        assert result is None


class TestRemoveRect:
    """测试 RemoveRect native 函数。"""

    def test_name_is_correct(self):
        """测试函数名称正确。"""
        native = RemoveRect()
        assert native.name == "RemoveRect"

    def test_execute_removes_rect(self):
        """测试执行移除 Rect。"""
        native = RemoveRect()

        mock_state_context = Mock()
        mock_handle_manager = Mock()
        mock_state_context.handle_manager = mock_handle_manager

        result = native.execute(mock_state_context, "rect_001")

        mock_handle_manager.remove_handle.assert_called_once_with("rect_001")

    def test_execute_with_none_rect(self):
        """测试 rect 为 None 时不报错。"""
        native = RemoveRect()

        mock_state_context = Mock()
        mock_handle_manager = Mock()
        mock_state_context.handle_manager = mock_handle_manager

        result = native.execute(mock_state_context, None)

        mock_handle_manager.remove_handle.assert_not_called()
```

**Step 2: 运行测试验证失败**

Run: `pytest tests/natives/test_rect_natives.py -v`
Expected: FAIL with "ModuleNotFoundError: No module named 'jass_runner.natives.rect_natives'"

**Step 3: 编写最小实现**

```python
"""Rect native 函数实现。

此模块包含 JASS Rect 类型相关的 native 函数实现。
"""

import logging
from .base import NativeFunction
from .rect import Rect as RectClass

logger = logging.getLogger(__name__)


class Rect(NativeFunction):
    """创建 Rect 对象（JASS Rect native 函数）。"""

    @property
    def name(self) -> str:
        """获取 native 函数名称。"""
        return "Rect"

    def execute(self, state_context, minx: float, miny: float,
                maxx: float, maxy: float):
        """执行 Rect native 函数。

        参数：
            state_context: 状态上下文
            minx: 最小 X 坐标
            miny: 最小 Y 坐标
            maxx: 最大 X 坐标
            maxy: 最大 Y 坐标

        返回：
            Rect handle ID，失败返回 None
        """
        if state_context is None or not hasattr(state_context, 'handle_manager'):
            logger.error("[Rect] state_context or handle_manager not found")
            return None

        handle_manager = state_context.handle_manager

        # 创建 Rect 对象
        rect_id = handle_manager.generate_id("rect")
        rect_obj = RectClass(rect_id, minx, miny, maxx, maxy)

        # 注册到 handle manager
        handle_manager.create_handle(rect_id, "rect", rect_obj)

        logger.info(f"[Rect] 创建矩形: {rect_id}, 边界=({minx},{miny})-({maxx},{maxy})")

        return rect_id


class RemoveRect(NativeFunction):
    """移除 Rect 对象（JASS RemoveRect native 函数）。"""

    @property
    def name(self) -> str:
        """获取 native 函数名称。"""
        return "RemoveRect"

    def execute(self, state_context, rect_id: str):
        """执行 RemoveRect native 函数。

        参数：
            state_context: 状态上下文
            rect_id: Rect handle ID

        返回：
            None
        """
        if state_context is None or not hasattr(state_context, 'handle_manager'):
            logger.error("[RemoveRect] state_context or handle_manager not found")
            return None

        if rect_id is None:
            logger.warning("[RemoveRect] 尝试移除 None 矩形")
            return None

        handle_manager = state_context.handle_manager
        handle_manager.remove_handle(rect_id)

        logger.info(f"[RemoveRect] 移除矩形: {rect_id}")

        return None
```

**Step 4: 运行测试验证通过**

Run: `pytest tests/natives/test_rect_natives.py -v`
Expected: PASS (6 tests)

**Step 5: 提交**

```bash
git add tests/natives/test_rect_natives.py src/jass_runner/natives/rect_natives.py
git commit -m "$(cat <<'EOF'
feat(natives): 添加 Rect 和 RemoveRect native 函数

实现 Rect 构造函数和 RemoveRect 析构函数，
支持创建和移除矩形区域对象。

Co-Authored-By: Claude (kimi-k2.5) <noreply@anthropic.com>
EOF
)"
```

---

## Task 2: 实现 Rect 查询函数

**Files:**
- Modify: `src/jass_runner/natives/rect_natives.py`
- Modify: `tests/natives/test_rect_natives.py`

**Step 1: 编写失败测试**

在 `tests/natives/test_rect_natives.py` 中添加：

```python
class TestGetRectQueries:
    """测试 Rect 查询函数。"""

    def test_get_rect_center_x(self):
        """测试 GetRectCenterX 返回中心 X 坐标。"""
        from jass_runner.natives.rect_natives import GetRectCenterX

        native = GetRectCenterX()

        mock_state_context = Mock()
        mock_handle_manager = Mock()

        # 创建模拟 Rect 对象
        mock_rect = Mock()
        mock_rect.min_x = -100.0
        mock_rect.max_x = 100.0
        mock_handle_manager.get_handle.return_value = mock_rect
        mock_state_context.handle_manager = mock_handle_manager

        result = native.execute(mock_state_context, "rect_001")

        assert result == 0.0  # (-100 + 100) / 2

    def test_get_rect_center_y(self):
        """测试 GetRectCenterY 返回中心 Y 坐标。"""
        from jass_runner.natives.rect_natives import GetRectCenterY

        native = GetRectCenterY()

        mock_state_context = Mock()
        mock_handle_manager = Mock()

        mock_rect = Mock()
        mock_rect.min_y = -50.0
        mock_rect.max_y = 50.0
        mock_handle_manager.get_handle.return_value = mock_rect
        mock_state_context.handle_manager = mock_handle_manager

        result = native.execute(mock_state_context, "rect_001")

        assert result == 0.0  # (-50 + 50) / 2

    def test_get_rect_min_x(self):
        """测试 GetRectMinX 返回最小 X 坐标。"""
        from jass_runner.natives.rect_natives import GetRectMinX

        native = GetRectMinX()

        mock_state_context = Mock()
        mock_handle_manager = Mock()

        mock_rect = Mock()
        mock_rect.min_x = -100.0
        mock_handle_manager.get_handle.return_value = mock_rect
        mock_state_context.handle_manager = mock_handle_manager

        result = native.execute(mock_state_context, "rect_001")

        assert result == -100.0

    def test_get_rect_min_y(self):
        """测试 GetRectMinY 返回最小 Y 坐标。"""
        from jass_runner.natives.rect_natives import GetRectMinY

        native = GetRectMinY()

        mock_state_context = Mock()
        mock_handle_manager = Mock()

        mock_rect = Mock()
        mock_rect.min_y = -50.0
        mock_handle_manager.get_handle.return_value = mock_rect
        mock_state_context.handle_manager = mock_handle_manager

        result = native.execute(mock_state_context, "rect_001")

        assert result == -50.0

    def test_get_rect_max_x(self):
        """测试 GetRectMaxX 返回最大 X 坐标。"""
        from jass_runner.natives.rect_natives import GetRectMaxX

        native = GetRectMaxX()

        mock_state_context = Mock()
        mock_handle_manager = Mock()

        mock_rect = Mock()
        mock_rect.max_x = 100.0
        mock_handle_manager.get_handle.return_value = mock_rect
        mock_state_context.handle_manager = mock_handle_manager

        result = native.execute(mock_state_context, "rect_001")

        assert result == 100.0

    def test_get_rect_max_y(self):
        """测试 GetRectMaxY 返回最大 Y 坐标。"""
        from jass_runner.natives.rect_natives import GetRectMaxY

        native = GetRectMaxY()

        mock_state_context = Mock()
        mock_handle_manager = Mock()

        mock_rect = Mock()
        mock_rect.max_y = 50.0
        mock_handle_manager.get_handle.return_value = mock_rect
        mock_state_context.handle_manager = mock_handle_manager

        result = native.execute(mock_state_context, "rect_001")

        assert result == 50.0

    def test_get_rect_with_invalid_handle(self):
        """测试无效 handle 返回 0.0。"""
        from jass_runner.natives.rect_natives import GetRectCenterX

        native = GetRectCenterX()

        mock_state_context = Mock()
        mock_handle_manager = Mock()
        mock_handle_manager.get_handle.return_value = None
        mock_state_context.handle_manager = mock_handle_manager

        result = native.execute(mock_state_context, "invalid_rect")

        assert result == 0.0
```

**Step 2: 运行测试验证失败**

Run: `pytest tests/natives/test_rect_natives.py::TestGetRectQueries -v`
Expected: FAIL with "ImportError"

**Step 3: 编写实现**

在 `src/jass_runner/natives/rect_natives.py` 中添加：

```python
class GetRectCenterX(NativeFunction):
    """获取 Rect 中心 X 坐标。"""

    @property
    def name(self) -> str:
        return "GetRectCenterX"

    def execute(self, state_context, rect_id: str) -> float:
        """执行 GetRectCenterX native 函数。

        参数：
            state_context: 状态上下文
            rect_id: Rect handle ID

        返回：
            中心 X 坐标，失败返回 0.0
        """
        if state_context is None or not hasattr(state_context, 'handle_manager'):
            logger.error("[GetRectCenterX] state_context or handle_manager not found")
            return 0.0

        if rect_id is None:
            return 0.0

        handle_manager = state_context.handle_manager
        rect_obj = handle_manager.get_handle(rect_id)

        if rect_obj is None:
            logger.warning(f"[GetRectCenterX] Rect not found: {rect_id}")
            return 0.0

        center_x = (rect_obj.min_x + rect_obj.max_x) / 2.0
        return center_x


class GetRectCenterY(NativeFunction):
    """获取 Rect 中心 Y 坐标。"""

    @property
    def name(self) -> str:
        return "GetRectCenterY"

    def execute(self, state_context, rect_id: str) -> float:
        """执行 GetRectCenterY native 函数。

        参数：
            state_context: 状态上下文
            rect_id: Rect handle ID

        返回：
            中心 Y 坐标，失败返回 0.0
        """
        if state_context is None or not hasattr(state_context, 'handle_manager'):
            logger.error("[GetRectCenterY] state_context or handle_manager not found")
            return 0.0

        if rect_id is None:
            return 0.0

        handle_manager = state_context.handle_manager
        rect_obj = handle_manager.get_handle(rect_id)

        if rect_obj is None:
            logger.warning(f"[GetRectCenterY] Rect not found: {rect_id}")
            return 0.0

        center_y = (rect_obj.min_y + rect_obj.max_y) / 2.0
        return center_y


class GetRectMinX(NativeFunction):
    """获取 Rect 最小 X 坐标。"""

    @property
    def name(self) -> str:
        return "GetRectMinX"

    def execute(self, state_context, rect_id: str) -> float:
        """执行 GetRectMinX native 函数。

        参数：
            state_context: 状态上下文
            rect_id: Rect handle ID

        返回：
            最小 X 坐标，失败返回 0.0
        """
        if state_context is None or not hasattr(state_context, 'handle_manager'):
            logger.error("[GetRectMinX] state_context or handle_manager not found")
            return 0.0

        if rect_id is None:
            return 0.0

        handle_manager = state_context.handle_manager
        rect_obj = handle_manager.get_handle(rect_id)

        if rect_obj is None:
            logger.warning(f"[GetRectMinX] Rect not found: {rect_id}")
            return 0.0

        return rect_obj.min_x


class GetRectMinY(NativeFunction):
    """获取 Rect 最小 Y 坐标。"""

    @property
    def name(self) -> str:
        return "GetRectMinY"

    def execute(self, state_context, rect_id: str) -> float:
        """执行 GetRectMinY native 函数。

        参数：
            state_context: 状态上下文
            rect_id: Rect handle ID

        返回：
            最小 Y 坐标，失败返回 0.0
        """
        if state_context is None or not hasattr(state_context, 'handle_manager'):
            logger.error("[GetRectMinY] state_context or handle_manager not found")
            return 0.0

        if rect_id is None:
            return 0.0

        handle_manager = state_context.handle_manager
        rect_obj = handle_manager.get_handle(rect_id)

        if rect_obj is None:
            logger.warning(f"[GetRectMinY] Rect not found: {rect_id}")
            return 0.0

        return rect_obj.min_y


class GetRectMaxX(NativeFunction):
    """获取 Rect 最大 X 坐标。"""

    @property
    def name(self) -> str:
        return "GetRectMaxX"

    def execute(self, state_context, rect_id: str) -> float:
        """执行 GetRectMaxX native 函数。

        参数：
            state_context: 状态上下文
            rect_id: Rect handle ID

        返回：
            最大 X 坐标，失败返回 0.0
        """
        if state_context is None or not hasattr(state_context, 'handle_manager'):
            logger.error("[GetRectMaxX] state_context or handle_manager not found")
            return 0.0

        if rect_id is None:
            return 0.0

        handle_manager = state_context.handle_manager
        rect_obj = handle_manager.get_handle(rect_id)

        if rect_obj is None:
            logger.warning(f"[GetRectMaxX] Rect not found: {rect_id}")
            return 0.0

        return rect_obj.max_x


class GetRectMaxY(NativeFunction):
    """获取 Rect 最大 Y 坐标。"""

    @property
    def name(self) -> str:
        return "GetRectMaxY"

    def execute(self, state_context, rect_id: str) -> float:
        """执行 GetRectMaxY native 函数。

        参数：
            state_context: 状态上下文
            rect_id: Rect handle ID

        返回：
            最大 Y 坐标，失败返回 0.0
        """
        if state_context is None or not hasattr(state_context, 'handle_manager'):
            logger.error("[GetRectMaxY] state_context or handle_manager not found")
            return 0.0

        if rect_id is None:
            return 0.0

        handle_manager = state_context.handle_manager
        rect_obj = handle_manager.get_handle(rect_id)

        if rect_obj is None:
            logger.warning(f"[GetRectMaxY] Rect not found: {rect_id}")
            return 0.0

        return rect_obj.max_y
```

**Step 4: 运行测试验证通过**

Run: `pytest tests/natives/test_rect_natives.py -v`
Expected: PASS (13 tests)

**Step 5: 提交**

```bash
git add tests/natives/test_rect_natives.py src/jass_runner/natives/rect_natives.py
git commit -m "$(cat <<'EOF'
feat(natives): 添加 Rect 查询函数

实现 GetRectCenterX/Y、GetRectMinX/Y、GetRectMaxX/Y 六个查询函数，
支持获取矩形区域的边界和中心坐标。

Co-Authored-By: Claude (kimi-k2.5) <noreply@anthropic.com>
EOF
)"
```

---

## Task 3: 实现 SetRect 和 MoveRectTo

**Files:**
- Modify: `src/jass_runner/natives/rect_natives.py`
- Modify: `tests/natives/test_rect_natives.py`

**Step 1: 编写失败测试**

在 `tests/natives/test_rect_natives.py` 中添加：

```python
class TestSetRect:
    """测试 SetRect native 函数。"""

    def test_name_is_correct(self):
        """测试函数名称正确。"""
        from jass_runner.natives.rect_natives import SetRect

        native = SetRect()
        assert native.name == "SetRect"

    def test_set_rect_updates_bounds(self):
        """测试 SetRect 更新矩形边界。"""
        from jass_runner.natives.rect_natives import SetRect

        native = SetRect()

        mock_state_context = Mock()
        mock_handle_manager = Mock()

        # 创建模拟 Rect 对象
        mock_rect = Mock()
        mock_rect.min_x = -100.0
        mock_rect.max_x = 100.0
        mock_handle_manager.get_handle.return_value = mock_rect
        mock_state_context.handle_manager = mock_handle_manager

        native.execute(mock_state_context, "rect_001", -50.0, -50.0, 50.0, 50.0)

        assert mock_rect.min_x == -50.0
        assert mock_rect.min_y == -50.0
        assert mock_rect.max_x == 50.0
        assert mock_rect.max_y == 50.0

    def test_set_rect_with_invalid_handle(self):
        """测试无效 handle 不报错。"""
        from jass_runner.natives.rect_natives import SetRect

        native = SetRect()

        mock_state_context = Mock()
        mock_handle_manager = Mock()
        mock_handle_manager.get_handle.return_value = None
        mock_state_context.handle_manager = mock_handle_manager

        # 应该不抛出异常
        native.execute(mock_state_context, "invalid_rect", -50.0, -50.0, 50.0, 50.0)


class TestMoveRectTo:
    """测试 MoveRectTo native 函数。"""

    def test_name_is_correct(self):
        """测试函数名称正确。"""
        from jass_runner.natives.rect_natives import MoveRectTo

        native = MoveRectTo()
        assert native.name == "MoveRectTo"

    def test_move_rect_to_moves_center(self):
        """测试 MoveRectTo 移动矩形中心。"""
        from jass_runner.natives.rect_natives import MoveRectTo

        native = MoveRectTo()

        mock_state_context = Mock()
        mock_handle_manager = Mock()

        # 创建模拟 Rect 对象，初始为 (-100, -100) 到 (100, 100)
        mock_rect = Mock()
        mock_rect.min_x = -100.0
        mock_rect.max_x = 100.0
        mock_rect.min_y = -100.0
        mock_rect.max_y = 100.0
        mock_handle_manager.get_handle.return_value = mock_rect
        mock_state_context.handle_manager = mock_handle_manager

        # 移动到 (500, 500)，保持宽高 200x200
        native.execute(mock_state_context, "rect_001", 500.0, 500.0)

        # 新的边界应该是 (400, 400) 到 (600, 600)
        assert mock_rect.min_x == 400.0
        assert mock_rect.max_x == 600.0
        assert mock_rect.min_y == 400.0
        assert mock_rect.max_y == 600.0

    def test_move_rect_to_with_invalid_handle(self):
        """测试无效 handle 不报错。"""
        from jass_runner.natives.rect_natives import MoveRectTo

        native = MoveRectTo()

        mock_state_context = Mock()
        mock_handle_manager = Mock()
        mock_handle_manager.get_handle.return_value = None
        mock_state_context.handle_manager = mock_handle_manager

        # 应该不抛出异常
        native.execute(mock_state_context, "invalid_rect", 0.0, 0.0)
```

**Step 2: 运行测试验证失败**

Run: `pytest tests/natives/test_rect_natives.py::TestSetRect -v`
Expected: FAIL with "ImportError"

**Step 3: 编写实现**

在 `src/jass_runner/natives/rect_natives.py` 中添加：

```python
class SetRect(NativeFunction):
    """设置 Rect 边界（JASS SetRect native 函数）。"""

    @property
    def name(self) -> str:
        return "SetRect"

    def execute(self, state_context, rect_id: str,
                minx: float, miny: float, maxx: float, maxy: float):
        """执行 SetRect native 函数。

        参数：
            state_context: 状态上下文
            rect_id: Rect handle ID
            minx: 新的最小 X 坐标
            miny: 新的最小 Y 坐标
            maxx: 新的最大 X 坐标
            maxy: 新的最大 Y 坐标

        返回：
            None
        """
        if state_context is None or not hasattr(state_context, 'handle_manager'):
            logger.error("[SetRect] state_context or handle_manager not found")
            return None

        if rect_id is None:
            logger.warning("[SetRect] rect_id is None")
            return None

        handle_manager = state_context.handle_manager
        rect_obj = handle_manager.get_handle(rect_id)

        if rect_obj is None:
            logger.warning(f"[SetRect] Rect not found: {rect_id}")
            return None

        # 更新矩形边界
        rect_obj.min_x = minx
        rect_obj.min_y = miny
        rect_obj.max_x = maxx
        rect_obj.max_y = maxy

        logger.info(f"[SetRect] 设置矩形边界: {rect_id}, ({minx},{miny})-({maxx},{maxy})")

        return None


class MoveRectTo(NativeFunction):
    """移动 Rect 到指定中心点（JASS MoveRectTo native 函数）。"""

    @property
    def name(self) -> str:
        return "MoveRectTo"

    def execute(self, state_context, rect_id: str, newCenterX: float, newCenterY: float):
        """执行 MoveRectTo native 函数。

        保持矩形宽高不变，移动中心点到指定位置。

        参数：
            state_context: 状态上下文
            rect_id: Rect handle ID
            newCenterX: 新的中心 X 坐标
            newCenterY: 新的中心 Y 坐标

        返回：
            None
        """
        if state_context is None or not hasattr(state_context, 'handle_manager'):
            logger.error("[MoveRectTo] state_context or handle_manager not found")
            return None

        if rect_id is None:
            logger.warning("[MoveRectTo] rect_id is None")
            return None

        handle_manager = state_context.handle_manager
        rect_obj = handle_manager.get_handle(rect_id)

        if rect_obj is None:
            logger.warning(f"[MoveRectTo] Rect not found: {rect_id}")
            return None

        # 计算当前宽高
        width = rect_obj.max_x - rect_obj.min_x
        height = rect_obj.max_y - rect_obj.min_y

        # 计算新的边界（保持宽高不变）
        rect_obj.min_x = newCenterX - width / 2.0
        rect_obj.max_x = newCenterX + width / 2.0
        rect_obj.min_y = newCenterY - height / 2.0
        rect_obj.max_y = newCenterY + height / 2.0

        logger.info(f"[MoveRectTo] 移动矩形: {rect_id} 到中心 ({newCenterX}, {newCenterY})")

        return None
```

**Step 4: 运行测试验证通过**

Run: `pytest tests/natives/test_rect_natives.py -v`
Expected: PASS (19 tests)

**Step 5: 提交**

```bash
git add tests/natives/test_rect_natives.py src/jass_runner/natives/rect_natives.py
git commit -m "$(cat <<'EOF'
feat(natives): 添加 SetRect 和 MoveRectTo 函数

实现 SetRect 用于设置矩形边界，MoveRectTo 用于移动矩形中心点
同时保持矩形尺寸不变。

Co-Authored-By: Claude (kimi-k2.5) <noreply@anthropic.com>
EOF
)"
```

---

## Task 4: 注册 Rect Native 函数到工厂

**Files:**
- Modify: `src/jass_runner/natives/factory.py`
- Test: `tests/natives/test_factory.py`

**Step 1: 修改 factory.py**

添加导入：

```python
from .rect_natives import (
    Rect, RemoveRect, SetRect, MoveRectTo,
    GetRectCenterX, GetRectCenterY, GetRectMinX, GetRectMinY, GetRectMaxX, GetRectMaxY,
)
```

在 `create_default_registry` 方法中添加注册：

```python
# 注册 Rect native 函数
registry.register(Rect())
registry.register(RemoveRect())
registry.register(SetRect())
registry.register(MoveRectTo())
registry.register(GetRectCenterX())
registry.register(GetRectCenterY())
registry.register(GetRectMinX())
registry.register(GetRectMinY())
registry.register(GetRectMaxX())
registry.register(GetRectMaxY())
```

**Step 2: 更新测试中的函数数量**

修改 `tests/natives/test_factory.py`：

```python
assert len(all_funcs) == 160  # 150 + 10 (rect natives)
```

**Step 3: 运行测试验证**

Run: `pytest tests/natives/test_factory.py -v`
Expected: PASS

验证 native 函数已注册：

```python
python -c "
from jass_runner.natives.factory import NativeFactory
factory = NativeFactory()
registry = factory.create_default_registry()
funcs = ['Rect', 'RemoveRect', 'SetRect', 'MoveRectTo', 'GetRectCenterX', 'GetRectCenterY', 'GetRectMinX', 'GetRectMinY', 'GetRectMaxX', 'GetRectMaxY']
for func in funcs:
    native = registry.get(func)
    print(f'{func}: {native is not None}')
"
```

Expected: 全部 True

**Step 4: 提交**

```bash
git add src/jass_runner/natives/factory.py tests/natives/test_factory.py
git commit -m "$(cat <<'EOF'
feat(natives): 注册 Rect native 函数到工厂

在 NativeFactory 中注册全部10个 Rect native 函数。

Co-Authored-By: Claude (kimi-k2.5) <noreply@anthropic.com>
EOF
)"
```

---

## Task 5: 运行完整测试套件

**Step 1: 运行所有相关测试**

```bash
pytest tests/natives/test_rect_natives.py tests/natives/test_factory.py -v
```

Expected: 所有测试通过

**Step 2: 运行完整测试套件**

```bash
pytest
```

Expected: 所有测试通过

**Step 3: 最终提交**

```bash
git commit -m "$(cat <<'EOF'
feat: 完整实现 Rect 核心 native 函数

实现 Rect 类型的9个核心 native 函数：
- 构造函数：Rect, RemoveRect
- 修改函数：SetRect, MoveRectTo
- 查询函数：GetRectCenterX/Y, GetRectMinX/Y, GetRectMaxX/Y

支持创建、修改和查询矩形区域。

Co-Authored-By: Claude (kimi-k2.5) <noreply@anthropic.com>
EOF
)" --allow-empty
```

---

## 完成检查清单

- [ ] Rect 和 RemoveRect 实现和测试
- [ ] 6个查询函数实现和测试
- [ ] SetRect 和 MoveRectTo 实现和测试
- [ ] NativeFactory 注册
- [ ] 完整测试套件通过

## 实现后验证

验证以下 JASS 代码可以正常工作：

```jass
set gg_rct_Region_001 = Rect(-1000.0, -1000.0, 1000.0, 1000.0)
set centerX = GetRectCenterX(gg_rct_Region_001)
call SetRect(gg_rct_Region_001, -500.0, -500.0, 500.0, 500.0)
call RemoveRect(gg_rct_Region_001)
```
