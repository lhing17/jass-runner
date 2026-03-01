"""数学扩展Native函数测试。

确认math_extended模块中的数学函数能够正确执行。
"""

import math
import pytest
from jass_runner.natives.math_extended import Tan


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
