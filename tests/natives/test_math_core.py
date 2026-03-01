"""数学Native函数测试。

此模块包含数学相关native函数的测试，如SquareRoot等。
"""

import pytest
import math
from jass_runner.natives.math_core import SquareRoot
from jass_runner.natives.state import StateContext


@pytest.fixture
def state_context():
    """提供测试用的StateContext实例。"""
    return StateContext()


class TestSquareRoot:
    """测试SquareRoot类的功能。"""

    def test_name_returns_square_root(self):
        """测试name属性返回正确的函数名。"""
        native = SquareRoot()
        assert native.name == "SquareRoot"

    def test_positive_number_returns_sqrt(self, state_context):
        """测试正数返回正确的平方根。"""
        native = SquareRoot()
        result = native.execute(state_context, 16.0)
        assert result == 4.0
        assert isinstance(result, float)

    def test_perfect_square_returns_exact(self, state_context):
        """测试完全平方数返回精确值。"""
        native = SquareRoot()
        result = native.execute(state_context, 25.0)
        assert result == 5.0

    def test_zero_returns_zero(self, state_context):
        """测试0的平方根返回0。"""
        native = SquareRoot()
        result = native.execute(state_context, 0.0)
        assert result == 0.0

    def test_one_returns_one(self, state_context):
        """测试1的平方根返回1。"""
        native = SquareRoot()
        result = native.execute(state_context, 1.0)
        assert result == 1.0

    def test_negative_returns_zero(self, state_context):
        """测试负数返回0（不抛出异常）。"""
        native = SquareRoot()
        result = native.execute(state_context, -4.0)
        assert result == 0.0

    def test_float_returns_correct_sqrt(self, state_context):
        """测试浮点数返回正确的平方根。"""
        native = SquareRoot()
        result = native.execute(state_context, 2.0)
        assert abs(result - math.sqrt(2.0)) < 1e-10

    def test_large_number(self, state_context):
        """测试大数字的平方根。"""
        native = SquareRoot()
        result = native.execute(state_context, 10000.0)
        assert result == 100.0
