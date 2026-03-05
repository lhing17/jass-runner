"""Rect native函数的测试。

此模块包含 Rect 和 RemoveRect native函数的单元测试。
"""

import pytest
from unittest.mock import MagicMock, Mock


class TestGetRectCenterX:
    """测试 GetRectCenterX native函数的功能。"""

    def test_get_rect_center_x_returns_center(self):
        """测试 GetRectCenterX 返回矩形中心X坐标。"""
        from jass_runner.natives.rect_natives import GetRectCenterX
        from jass_runner.natives.manager import HandleManager

        # 准备
        state_context = MagicMock()
        state_context.handle_manager = HandleManager()
        get_center_x = GetRectCenterX()

        # 创建一个矩形 (0, 0) - (100, 100)
        rect = state_context.handle_manager.create_rect(0.0, 0.0, 100.0, 100.0)

        # 执行
        result = get_center_x.execute(state_context, rect)

        # 验证 - 中心X应为 50.0
        assert result == 50.0

    def test_get_rect_center_x_with_invalid_handle_returns_zero(self):
        """测试 GetRectCenterX 处理无效handle返回0.0。"""
        from jass_runner.natives.rect_natives import GetRectCenterX
        from jass_runner.natives.manager import HandleManager

        # 准备
        state_context = MagicMock()
        state_context.handle_manager = HandleManager()
        get_center_x = GetRectCenterX()

        # 执行 - 传入None
        result = get_center_x.execute(state_context, None)

        # 验证 - 应返回 0.0
        assert result == 0.0


class TestGetRectCenterY:
    """测试 GetRectCenterY native函数的功能。"""

    def test_get_rect_center_y_returns_center(self):
        """测试 GetRectCenterY 返回矩形中心Y坐标。"""
        from jass_runner.natives.rect_natives import GetRectCenterY
        from jass_runner.natives.manager import HandleManager

        # 准备
        state_context = MagicMock()
        state_context.handle_manager = HandleManager()
        get_center_y = GetRectCenterY()

        # 创建一个矩形 (0, 0) - (100, 200)
        rect = state_context.handle_manager.create_rect(0.0, 0.0, 100.0, 200.0)

        # 执行
        result = get_center_y.execute(state_context, rect)

        # 验证 - 中心Y应为 100.0
        assert result == 100.0


class TestGetRectMinX:
    """测试 GetRectMinX native函数的功能。"""

    def test_get_rect_min_x_returns_min_x(self):
        """测试 GetRectMinX 返回矩形最小X坐标。"""
        from jass_runner.natives.rect_natives import GetRectMinX
        from jass_runner.natives.manager import HandleManager

        # 准备
        state_context = MagicMock()
        state_context.handle_manager = HandleManager()
        get_min_x = GetRectMinX()

        # 创建一个矩形 (10.0, 20.0) - (100.0, 200.0)
        rect = state_context.handle_manager.create_rect(10.0, 20.0, 100.0, 200.0)

        # 执行
        result = get_min_x.execute(state_context, rect)

        # 验证
        assert result == 10.0


class TestGetRectMinY:
    """测试 GetRectMinY native函数的功能。"""

    def test_get_rect_min_y_returns_min_y(self):
        """测试 GetRectMinY 返回矩形最小Y坐标。"""
        from jass_runner.natives.rect_natives import GetRectMinY
        from jass_runner.natives.manager import HandleManager

        # 准备
        state_context = MagicMock()
        state_context.handle_manager = HandleManager()
        get_min_y = GetRectMinY()

        # 创建一个矩形 (10.0, 20.0) - (100.0, 200.0)
        rect = state_context.handle_manager.create_rect(10.0, 20.0, 100.0, 200.0)

        # 执行
        result = get_min_y.execute(state_context, rect)

        # 验证
        assert result == 20.0


class TestGetRectMaxX:
    """测试 GetRectMaxX native函数的功能。"""

    def test_get_rect_max_x_returns_max_x(self):
        """测试 GetRectMaxX 返回矩形最大X坐标。"""
        from jass_runner.natives.rect_natives import GetRectMaxX
        from jass_runner.natives.manager import HandleManager

        # 准备
        state_context = MagicMock()
        state_context.handle_manager = HandleManager()
        get_max_x = GetRectMaxX()

        # 创建一个矩形 (10.0, 20.0) - (100.0, 200.0)
        rect = state_context.handle_manager.create_rect(10.0, 20.0, 100.0, 200.0)

        # 执行
        result = get_max_x.execute(state_context, rect)

        # 验证
        assert result == 100.0


class TestGetRectMaxY:
    """测试 GetRectMaxY native函数的功能。"""

    def test_get_rect_max_y_returns_max_y(self):
        """测试 GetRectMaxY 返回矩形最大Y坐标。"""
        from jass_runner.natives.rect_natives import GetRectMaxY
        from jass_runner.natives.manager import HandleManager

        # 准备
        state_context = MagicMock()
        state_context.handle_manager = HandleManager()
        get_max_y = GetRectMaxY()

        # 创建一个矩形 (10.0, 20.0) - (100.0, 200.0)
        rect = state_context.handle_manager.create_rect(10.0, 20.0, 100.0, 200.0)

        # 执行
        result = get_max_y.execute(state_context, rect)

        # 验证
        assert result == 200.0


class TestRectNative:
    """测试 Rect native函数的功能。"""

    def test_rect_name_returns_rect(self):
        """测试 Rect 类的 name 属性返回 'Rect'。"""
        from jass_runner.natives.rect_natives import RectNative

        rect_native = RectNative()
        assert rect_native.name == "Rect"

    def test_rect_execute_creates_rect(self):
        """测试 Rect execute 方法创建 Rect 对象。"""
        from jass_runner.natives.rect_natives import RectNative
        from jass_runner.natives.manager import HandleManager

        # 准备
        state_context = MagicMock()
        state_context.handle_manager = HandleManager()
        rect_native = RectNative()

        # 执行
        result = rect_native.execute(state_context, 0.0, 0.0, 100.0, 100.0)

        # 验证
        assert result is not None
        assert result.min_x == 0.0
        assert result.min_y == 0.0
        assert result.max_x == 100.0
        assert result.max_y == 100.0
        assert result.type_name == "rect"

    def test_rect_execute_registers_with_handle_manager(self):
        """测试 Rect execute 方法通过 HandleManager 注册 Rect。"""
        from jass_runner.natives.rect_natives import RectNative
        from jass_runner.natives.manager import HandleManager

        # 准备
        state_context = MagicMock()
        state_context.handle_manager = HandleManager()
        rect_native = RectNative()

        # 执行前没有 rect 类型 handle
        initial_count = state_context.handle_manager.get_handle_type_count("rect")
        assert initial_count == 0

        # 执行
        result = rect_native.execute(state_context, 10.0, 20.0, 110.0, 120.0)

        # 验证 rect 已被注册
        assert state_context.handle_manager.get_handle_type_count("rect") == 1
        assert result.id is not None
        assert result.id.startswith("rect_")


class TestRemoveRectNative:
    """测试 RemoveRect native函数的功能。"""

    def test_remove_rect_name_returns_remove_rect(self):
        """测试 RemoveRect 类的 name 属性返回 'RemoveRect'。"""
        from jass_runner.natives.rect_natives import RemoveRect

        remove_rect = RemoveRect()
        assert remove_rect.name == "RemoveRect"

    def test_remove_rect_execute_removes_rect(self):
        """测试 RemoveRect execute 方法从 HandleManager 移除 Rect。"""
        from jass_runner.natives.rect_natives import RectNative, RemoveRect
        from jass_runner.natives.manager import HandleManager

        # 准备 - 先创建一个 Rect
        state_context = MagicMock()
        state_context.handle_manager = HandleManager()
        rect_native = RectNative()
        remove_rect = RemoveRect()

        rect = rect_native.execute(state_context, 0.0, 0.0, 100.0, 100.0)
        assert state_context.handle_manager.get_alive_handles() == 17  # 16 players + 1 rect

        # 执行 - 移除 Rect
        remove_rect.execute(state_context, rect)

        # 验证 rect 已被销毁（存活数减少，类型计数不变）
        assert state_context.handle_manager.get_alive_handles() == 16  # 16 players
        assert rect.is_alive() is False

    def test_remove_rect_execute_with_none(self):
        """测试 RemoveRect execute 方法处理 None 参数。"""
        from jass_runner.natives.rect_natives import RemoveRect
        from jass_runner.natives.manager import HandleManager

        # 准备
        state_context = MagicMock()
        state_context.handle_manager = HandleManager()
        remove_rect = RemoveRect()

        # 执行 - 不应抛出异常
        result = remove_rect.execute(state_context, None)

        # 验证 - 正常返回，没有异常
        assert result is None


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
        from jass_runner.natives.manager import HandleManager

        native = SetRect()

        # 准备
        state_context = MagicMock()
        state_context.handle_manager = HandleManager()

        # 创建矩形
        rect = state_context.handle_manager.create_rect(-100.0, -100.0, 100.0, 100.0)

        # 执行 - 更新边界
        native.execute(state_context, rect, -50.0, -50.0, 50.0, 50.0)

        # 验证 - 边界已更新
        assert rect.min_x == -50.0
        assert rect.min_y == -50.0
        assert rect.max_x == 50.0
        assert rect.max_y == 50.0

    def test_set_rect_with_invalid_handle(self):
        """测试无效 handle 不报错。"""
        from jass_runner.natives.rect_natives import SetRect
        from jass_runner.natives.manager import HandleManager

        native = SetRect()

        # 准备
        state_context = MagicMock()
        state_context.handle_manager = HandleManager()

        # 执行 - 传入None，应该不抛出异常
        result = native.execute(state_context, None, -50.0, -50.0, 50.0, 50.0)

        # 验证 - 正常返回None
        assert result is None


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
        from jass_runner.natives.manager import HandleManager

        native = MoveRectTo()

        # 准备
        state_context = MagicMock()
        state_context.handle_manager = HandleManager()

        # 创建矩形，初始为 (-100, -100) 到 (100, 100)，中心(0,0)，宽高200x200
        rect = state_context.handle_manager.create_rect(-100.0, -100.0, 100.0, 100.0)

        # 执行 - 移动到 (500, 500)，保持宽高 200x200
        native.execute(state_context, rect, 500.0, 500.0)

        # 验证 - 新的边界应该是 (400, 400) 到 (600, 600)
        assert rect.min_x == 400.0
        assert rect.max_x == 600.0
        assert rect.min_y == 400.0
        assert rect.max_y == 600.0

    def test_move_rect_to_with_invalid_handle(self):
        """测试无效 handle 不报错。"""
        from jass_runner.natives.rect_natives import MoveRectTo
        from jass_runner.natives.manager import HandleManager

        native = MoveRectTo()

        # 准备
        state_context = MagicMock()
        state_context.handle_manager = HandleManager()

        # 执行 - 传入None，应该不抛出异常
        result = native.execute(state_context, None, 0.0, 0.0)

        # 验证 - 正常返回None
        assert result is None
