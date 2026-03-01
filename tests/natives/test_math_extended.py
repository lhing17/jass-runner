"""数学扩展Native函数测试。

确认math_extended模块中的数学函数能够正确执行。
"""

import math
import pytest
from jass_runner.natives.math_extended import Tan, ModuloInteger, ModuloReal


class TestTan:
    """测试Tan native函数。"""

    def test_tan_zero_returns_zero(self):
        """测试tan(0)返回0。"""
        # 准备
        tan = Tan()
        state_context = None  # Tan函数不需要状态上下文

        # 执行
        result = tan.execute(state_context, 0.0)

        # 验证
        assert result == pytest.approx(0.0, abs=1e-10)

    def test_tan_pi_over_four_returns_one(self):
        """测试tan(π/4)返回1。"""
        # 准备
        tan = Tan()
        state_context = None

        # 执行
        result = tan.execute(state_context, math.pi / 4)

        # 验证
        assert result == pytest.approx(1.0, abs=1e-10)

    def test_tan_pi_returns_zero(self):
        """测试tan(π)返回0。"""
        # 准备
        tan = Tan()
        state_context = None

        # 执行
        result = tan.execute(state_context, math.pi)

        # 验证
        assert result == pytest.approx(0.0, abs=1e-10)

    def test_tan_returns_float(self):
        """测试Tan函数返回实数类型。"""
        # 准备
        tan = Tan()
        state_context = None

        # 执行
        result = tan.execute(state_context, math.pi / 4)

        # 验证
        assert isinstance(result, float)

    def test_tan_name_is_correct(self):
        """测试Tan函数名称正确。"""
        # 准备
        tan = Tan()

        # 验证
        assert tan.name == "Tan"


class TestModuloInteger:
    """测试ModuloInteger native函数。"""

    def test_positive_numbers(self):
        """测试正数取模：10 % 3 = 1。"""
        # 准备
        mod = ModuloInteger()
        state_context = None

        # 执行
        result = mod.execute(state_context, 10, 3)

        # 验证
        assert result == 1
        assert isinstance(result, int)

    def test_exact_division(self):
        """测试整除：12 % 3 = 0。"""
        # 准备
        mod = ModuloInteger()
        state_context = None

        # 执行
        result = mod.execute(state_context, 12, 3)

        # 验证
        assert result == 0

    def test_negative_dividend(self):
        """测试负被除数：-10 % 3 = 2（Python行为）。"""
        # 准备
        mod = ModuloInteger()
        state_context = None

        # 执行
        result = mod.execute(state_context, -10, 3)

        # 验证
        assert result == 2

    def test_divisor_zero(self):
        """测试除数为0时返回0。"""
        # 准备
        mod = ModuloInteger()
        state_context = None

        # 执行
        result = mod.execute(state_context, 10, 0)

        # 验证
        assert result == 0

    def test_name_is_correct(self):
        """测试ModuloInteger函数名称正确。"""
        # 准备
        mod = ModuloInteger()

        # 验证
        assert mod.name == "ModuloInteger"


class TestModuloReal:
    """测试ModuloReal native函数。"""

    def test_positive_numbers(self):
        """测试正实数：10.5 % 3.0 = 1.5。"""
        # 准备
        mod = ModuloReal()
        state_context = None

        # 执行
        result = mod.execute(state_context, 10.5, 3.0)

        # 验证
        assert result == pytest.approx(1.5, abs=1e-10)
        assert isinstance(result, float)

    def test_divisor_zero(self):
        """测试除数为0时返回0.0。"""
        # 准备
        mod = ModuloReal()
        state_context = None

        # 执行
        result = mod.execute(state_context, 10.5, 0.0)

        # 验证
        assert result == 0.0

    def test_name_is_correct(self):
        """测试ModuloReal函数名称正确。"""
        # 准备
        mod = ModuloReal()

        # 验证
        assert mod.name == "ModuloReal"
