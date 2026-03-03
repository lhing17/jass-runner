"""测试 Camera 相关 native 函数。"""

import pytest
from src.jass_runner.natives.camera import GetCameraMargin, SetCameraBounds
from src.jass_runner.natives.state import StateContext


class TestGetCameraMargin:
    """测试 GetCameraMargin 类。"""

    def test_valid_left_margin_returns_100(self):
        """测试 LEFT 边距类型返回 100.0。"""
        native = GetCameraMargin()
        context = StateContext()

        result = native.execute(context, 0)  # CAMERA_MARGIN_LEFT

        assert result == 100.0

    def test_valid_right_margin_returns_100(self):
        """测试 RIGHT 边距类型返回 100.0。"""
        native = GetCameraMargin()
        context = StateContext()

        result = native.execute(context, 1)  # CAMERA_MARGIN_RIGHT

        assert result == 100.0

    def test_valid_top_margin_returns_100(self):
        """测试 TOP 边距类型返回 100.0。"""
        native = GetCameraMargin()
        context = StateContext()

        result = native.execute(context, 2)  # CAMERA_MARGIN_TOP

        assert result == 100.0

    def test_valid_bottom_margin_returns_100(self):
        """测试 BOTTOM 边距类型返回 100.0。"""
        native = GetCameraMargin()
        context = StateContext()

        result = native.execute(context, 3)  # CAMERA_MARGIN_BOTTOM

        assert result == 100.0

    def test_invalid_margin_returns_0(self):
        """测试无效边距类型返回 0.0。"""
        native = GetCameraMargin()
        context = StateContext()

        result = native.execute(context, 99)

        assert result == 0.0

    def test_negative_margin_returns_0(self):
        """测试负值边距类型返回 0.0。"""
        native = GetCameraMargin()
        context = StateContext()

        result = native.execute(context, -1)

        assert result == 0.0


class TestSetCameraBounds:
    """测试 SetCameraBounds 类。"""

    def test_bounds_are_stored_in_context(self):
        """测试边界值正确存储在 StateContext 中。"""
        native = SetCameraBounds()
        context = StateContext()

        native.execute(context, 0.0, 0.0, 100.0, 100.0, 200.0, 200.0, 300.0, 300.0)

        assert context.camera_bounds['x1'] == 0.0
        assert context.camera_bounds['y1'] == 0.0
        assert context.camera_bounds['x2'] == 100.0
        assert context.camera_bounds['y2'] == 100.0
        assert context.camera_bounds['x3'] == 200.0
        assert context.camera_bounds['y3'] == 200.0
        assert context.camera_bounds['x4'] == 300.0
        assert context.camera_bounds['y4'] == 300.0

    def test_negative_bounds_are_stored(self):
        """测试负坐标边界值也能正确存储。"""
        native = SetCameraBounds()
        context = StateContext()

        native.execute(context, -11520.0, -11776.0, 11520.0, 11264.0,
                      -11520.0, 11264.0, 11520.0, -11776.0)

        assert context.camera_bounds['x1'] == -11520.0
        assert context.camera_bounds['y2'] == 11264.0
