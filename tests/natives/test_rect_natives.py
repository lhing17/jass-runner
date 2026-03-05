"""Rect native函数的测试。

此模块包含 Rect 和 RemoveRect native函数的单元测试。
"""

import pytest
from unittest.mock import MagicMock


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
