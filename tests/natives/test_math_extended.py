"""数学扩展Native函数测试。

确认math_extended模块中的数学函数能够正确执行。
"""

import math
import pytest
from jass_runner.natives.math_extended import Tan, ModuloInteger, ModuloReal, R2S, S2R, I2S, S2I


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


class TestR2S:
    """测试R2S native函数（实数转字符串）。"""

    def test_integer_real_formats_with_three_decimals(self):
        """测试整数实数格式化为3位小数：42.0 -> "42.000"。"""
        # 准备
        r2s = R2S()
        state_context = None

        # 执行
        result = r2s.execute(state_context, 42.0)

        # 验证
        assert result == "42.000"
        assert isinstance(result, str)

    def test_pi_formats_with_three_decimals(self):
        """测试π格式化为3位小数：3.14159 -> "3.142"。"""
        # 准备
        r2s = R2S()
        state_context = None

        # 执行
        result = r2s.execute(state_context, 3.14159)

        # 验证
        assert result == "3.142"

    def test_negative_number_formats_with_three_decimals(self):
        """测试负数格式化为3位小数：-5.5 -> "-5.500"。"""
        # 准备
        r2s = R2S()
        state_context = None

        # 执行
        result = r2s.execute(state_context, -5.5)

        # 验证
        assert result == "-5.500"

    def test_name_is_correct(self):
        """测试R2S函数名称正确。"""
        # 准备
        r2s = R2S()

        # 验证
        assert r2s.name == "R2S"


class TestS2R:
    """测试S2R native函数（字符串转实数）。"""

    def test_valid_decimal_string(self):
        """测试有效小数字符串："3.14" -> 3.14。"""
        # 准备
        s2r = S2R()
        state_context = None

        # 执行
        result = s2r.execute(state_context, "3.14")

        # 验证
        assert result == pytest.approx(3.14, abs=1e-10)
        assert isinstance(result, float)

    def test_integer_string_returns_float(self):
        """测试整数字符串转为实数："42" -> 42.0。"""
        # 准备
        s2r = S2R()
        state_context = None

        # 执行
        result = s2r.execute(state_context, "42")

        # 验证
        assert result == pytest.approx(42.0, abs=1e-10)

    def test_invalid_string_returns_zero(self):
        """测试无效字符串返回0.0："not_a_number" -> 0.0。"""
        # 准备
        s2r = S2R()
        state_context = None

        # 执行
        result = s2r.execute(state_context, "not_a_number")

        # 验证
        assert result == 0.0

    def test_empty_string_returns_zero(self):
        """测试空字符串返回0.0："" -> 0.0。"""
        # 准备
        s2r = S2R()
        state_context = None

        # 执行
        result = s2r.execute(state_context, "")

        # 验证
        assert result == 0.0

    def test_name_is_correct(self):
        """测试S2R函数名称正确。"""
        # 准备
        s2r = S2R()

        # 验证
        assert s2r.name == "S2R"


class TestI2S:
    """测试I2S native函数（整数转字符串）。"""

    def test_positive_integer(self):
        """测试正整数：42 -> "42"。"""
        # 准备
        i2s = I2S()
        state_context = None

        # 执行
        result = i2s.execute(state_context, 42)

        # 验证
        assert result == "42"
        assert isinstance(result, str)

    def test_negative_integer(self):
        """测试负整数：-10 -> "-10"。"""
        # 准备
        i2s = I2S()
        state_context = None

        # 执行
        result = i2s.execute(state_context, -10)

        # 验证
        assert result == "-10"

    def test_zero(self):
        """测试零：0 -> "0"。"""
        # 准备
        i2s = I2S()
        state_context = None

        # 执行
        result = i2s.execute(state_context, 0)

        # 验证
        assert result == "0"

    def test_name_is_correct(self):
        """测试I2S函数名称正确。"""
        # 准备
        i2s = I2S()

        # 验证
        assert i2s.name == "I2S"


class TestS2I:
    """测试S2I native函数（字符串转整数）。"""

    def test_valid_integer_string(self):
        """测试有效整数字符串："42" -> 42。"""
        # 准备
        s2i = S2I()
        state_context = None

        # 执行
        result = s2i.execute(state_context, "42")

        # 验证
        assert result == 42
        assert isinstance(result, int)

    def test_negative_integer_string(self):
        """测试负数字符串："-10" -> -10。"""
        # 准备
        s2i = S2I()
        state_context = None

        # 执行
        result = s2i.execute(state_context, "-10")

        # 验证
        assert result == -10

    def test_invalid_string_returns_zero(self):
        """测试无效字符串返回0："not_a_number" -> 0。"""
        # 准备
        s2i = S2I()
        state_context = None

        # 执行
        result = s2i.execute(state_context, "not_a_number")

        # 验证
        assert result == 0

    def test_empty_string_returns_zero(self):
        """测试空字符串返回0："" -> 0。"""
        # 准备
        s2i = S2I()
        state_context = None

        # 执行
        result = s2i.execute(state_context, "")

        # 验证
        assert result == 0

    def test_name_is_correct(self):
        """测试S2I函数名称正确。"""
        # 准备
        s2i = S2I()

        # 验证
        assert s2i.name == "S2I"
