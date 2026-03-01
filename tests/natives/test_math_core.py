"""数学Native函数测试。

此模块包含数学相关native函数的测试，如SquareRoot等。
"""

import pytest
import math
from jass_runner.natives.math_core import SquareRoot, Pow, Cos, Sin, R2I, I2R
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


class TestPow:
    """测试Pow类的功能。"""

    def test_name_returns_pow(self):
        """测试name属性返回正确的函数名。"""
        native = Pow()
        assert native.name == "Pow"

    def test_positive_base_positive_exponent(self, state_context):
        """测试正底数正指数（如2.0^3.0 = 8.0）。"""
        native = Pow()
        result = native.execute(state_context, 2.0, 3.0)
        assert result == 8.0
        assert isinstance(result, float)

    def test_zero_exponent_returns_one(self, state_context):
        """测试0指数（如5.0^0.0 = 1.0）。"""
        native = Pow()
        result = native.execute(state_context, 5.0, 0.0)
        assert result == 1.0

    def test_negative_exponent(self, state_context):
        """测试负指数（如2.0^-1.0 = 0.5）。"""
        native = Pow()
        result = native.execute(state_context, 2.0, -1.0)
        assert result == 0.5

    def test_fractional_exponent(self, state_context):
        """测试分数指数（如4.0^0.5 = 2.0）。"""
        native = Pow()
        result = native.execute(state_context, 4.0, 0.5)
        assert result == 2.0

    def test_common_cases(self, state_context):
        """测试常见幂运算场景。"""
        native = Pow()
        # 平方
        result = native.execute(state_context, 3.0, 2.0)
        assert result == 9.0
        # 立方
        result = native.execute(state_context, 2.0, 3.0)
        assert result == 8.0
        # 开平方
        result = native.execute(state_context, 16.0, 0.5)
        assert result == 4.0

    def test_base_one_returns_one(self, state_context):
        """测试底数为1时总是返回1。"""
        native = Pow()
        result = native.execute(state_context, 1.0, 100.0)
        assert result == 1.0
        result = native.execute(state_context, 1.0, -5.0)
        assert result == 1.0

    def test_base_zero_positive_exponent(self, state_context):
        """测试底数为0时正指数返回0。"""
        native = Pow()
        result = native.execute(state_context, 0.0, 5.0)
        assert result == 0.0


class TestCos:
    """测试Cos类的功能。"""

    def test_name_returns_cos(self):
        """测试name属性返回正确的函数名。"""
        native = Cos()
        assert native.name == "Cos"

    def test_cos_zero_returns_one(self, state_context):
        """测试cos(0) = 1。"""
        native = Cos()
        result = native.execute(state_context, 0.0)
        assert abs(result - 1.0) < 0.0001

    def test_cos_pi_returns_minus_one(self, state_context):
        """测试cos(π) = -1。"""
        native = Cos()
        result = native.execute(state_context, math.pi)
        assert abs(result - (-1.0)) < 0.0001

    def test_cos_half_pi_returns_zero(self, state_context):
        """测试cos(π/2) = 0。"""
        native = Cos()
        result = native.execute(state_context, math.pi / 2)
        assert abs(result - 0.0) < 0.0001

    def test_returns_float(self, state_context):
        """测试返回类型为float。"""
        native = Cos()
        result = native.execute(state_context, 0.0)
        assert isinstance(result, float)


class TestSin:
    """测试Sin类的功能。"""

    def test_name_returns_sin(self):
        """测试name属性返回正确的函数名。"""
        native = Sin()
        assert native.name == "Sin"

    def test_sin_zero_returns_zero(self, state_context):
        """测试sin(0) = 0。"""
        native = Sin()
        result = native.execute(state_context, 0.0)
        assert abs(result - 0.0) < 0.0001

    def test_sin_half_pi_returns_one(self, state_context):
        """测试sin(π/2) = 1。"""
        native = Sin()
        result = native.execute(state_context, math.pi / 2)
        assert abs(result - 1.0) < 0.0001

    def test_sin_pi_returns_zero(self, state_context):
        """测试sin(π) = 0。"""
        native = Sin()
        result = native.execute(state_context, math.pi)
        assert abs(result - 0.0) < 0.0001

    def test_returns_float(self, state_context):
        """测试返回类型为float。"""
        native = Sin()
        result = native.execute(state_context, 0.0)
        assert isinstance(result, float)


class TestR2I:
    """测试R2I类的功能。"""

    def test_name_returns_r2i(self):
        """测试name属性返回正确的函数名。"""
        native = R2I()
        assert native.name == "R2I"

    def test_positive_real_truncates_toward_zero(self, state_context):
        """测试正实数向零截断（如3.7 -> 3）。"""
        native = R2I()
        result = native.execute(state_context, 3.7)
        assert result == 3
        assert isinstance(result, int)

    def test_negative_real_truncates_toward_zero(self, state_context):
        """测试负实数向零截断（如-3.7 -> -3）。"""
        native = R2I()
        result = native.execute(state_context, -3.7)
        assert result == -3
        assert isinstance(result, int)

    def test_integer_real_returns_same(self, state_context):
        """测试整数实数保持原值（如5.0 -> 5）。"""
        native = R2I()
        result = native.execute(state_context, 5.0)
        assert result == 5
        assert isinstance(result, int)

    def test_zero_returns_zero(self, state_context):
        """测试0.0转换为0。"""
        native = R2I()
        result = native.execute(state_context, 0.0)
        assert result == 0
        assert isinstance(result, int)


class TestI2R:
    """测试I2R类的功能。"""

    def test_name_returns_i2r(self):
        """测试name属性返回正确的函数名。"""
        native = I2R()
        assert native.name == "I2R"

    def test_positive_integer_converts_to_real(self, state_context):
        """测试正整数转换为实数（如42 -> 42.0）。"""
        native = I2R()
        result = native.execute(state_context, 42)
        assert result == 42.0
        assert isinstance(result, float)

    def test_negative_integer_converts_to_real(self, state_context):
        """测试负整数转换为实数（如-10 -> -10.0）。"""
        native = I2R()
        result = native.execute(state_context, -10)
        assert result == -10.0
        assert isinstance(result, float)

    def test_zero_converts_to_real(self, state_context):
        """测试0转换为0.0。"""
        native = I2R()
        result = native.execute(state_context, 0)
        assert result == 0.0
        assert isinstance(result, float)
