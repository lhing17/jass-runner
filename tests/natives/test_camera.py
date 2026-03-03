"""测试 Camera 相关 native 函数。"""

import pytest
from src.jass_runner.natives.camera import GetCameraMargin
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
