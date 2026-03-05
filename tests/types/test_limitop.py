"""LimitOp类型测试。

测试LimitOp比较操作符类的功能。
"""

import pytest
from jass_runner.types.limitop import LimitOp


class TestLimitOpConstants:
    """测试LimitOp常量定义。"""

    def test_less_than_constant(self):
        """测试LESS_THAN常量值为0。"""
        assert LimitOp.LESS_THAN == 0

    def test_less_than_or_equal_constant(self):
        """测试LESS_THAN_OR_EQUAL常量值为1。"""
        assert LimitOp.LESS_THAN_OR_EQUAL == 1

    def test_equal_constant(self):
        """测试EQUAL常量值为2。"""
        assert LimitOp.EQUAL == 2

    def test_greater_than_or_equal_constant(self):
        """测试GREATER_THAN_OR_EQUAL常量值为3。"""
        assert LimitOp.GREATER_THAN_OR_EQUAL == 3

    def test_greater_than_constant(self):
        """测试GREATER_THAN常量值为4。"""
        assert LimitOp.GREATER_THAN == 4

    def test_not_equal_constant(self):
        """测试NOT_EQUAL常量值为5。"""
        assert LimitOp.NOT_EQUAL == 5


class TestLimitOpCompare:
    """测试LimitOp.compare方法。"""

    def test_compare_less_than_true(self):
        """测试LESS_THAN比较，当a<b时返回True。"""
        assert LimitOp.compare(LimitOp.LESS_THAN, 1.0, 2.0) is True

    def test_compare_less_than_false(self):
        """测试LESS_THAN比较，当a>=b时返回False。"""
        assert LimitOp.compare(LimitOp.LESS_THAN, 2.0, 1.0) is False
        assert LimitOp.compare(LimitOp.LESS_THAN, 1.0, 1.0) is False

    def test_compare_equal_true(self):
        """测试EQUAL比较，当a==b时返回True。"""
        assert LimitOp.compare(LimitOp.EQUAL, 1.0, 1.0) is True

    def test_compare_equal_with_epsilon(self):
        """测试EQUAL比较使用epsilon处理浮点数精度。"""
        assert LimitOp.compare(LimitOp.EQUAL, 1.0, 1.0005) is True
        assert LimitOp.compare(LimitOp.EQUAL, 1.0, 1.002) is False

    def test_compare_greater_than_true(self):
        """测试GREATER_THAN比较，当a>b时返回True。"""
        assert LimitOp.compare(LimitOp.GREATER_THAN, 2.0, 1.0) is True

    def test_compare_greater_than_false(self):
        """测试GREATER_THAN比较，当a<=b时返回False。"""
        assert LimitOp.compare(LimitOp.GREATER_THAN, 1.0, 2.0) is False
        assert LimitOp.compare(LimitOp.GREATER_THAN, 1.0, 1.0) is False

    def test_compare_not_equal_true(self):
        """测试NOT_EQUAL比较，当a!=b时返回True。"""
        assert LimitOp.compare(LimitOp.NOT_EQUAL, 1.0, 2.0) is True

    def test_compare_not_equal_false(self):
        """测试NOT_EQUAL比较，当a==b时返回False。"""
        assert LimitOp.compare(LimitOp.NOT_EQUAL, 1.0, 1.0) is False

    def test_compare_less_than_or_equal(self):
        """测试LESS_THAN_OR_EQUAL比较。"""
        assert LimitOp.compare(LimitOp.LESS_THAN_OR_EQUAL, 1.0, 2.0) is True
        assert LimitOp.compare(LimitOp.LESS_THAN_OR_EQUAL, 1.0, 1.0) is True
        assert LimitOp.compare(LimitOp.LESS_THAN_OR_EQUAL, 2.0, 1.0) is False

    def test_compare_greater_than_or_equal(self):
        """测试GREATER_THAN_OR_EQUAL比较。"""
        assert LimitOp.compare(LimitOp.GREATER_THAN_OR_EQUAL, 2.0, 1.0) is True
        assert LimitOp.compare(LimitOp.GREATER_THAN_OR_EQUAL, 1.0, 1.0) is True
        assert LimitOp.compare(LimitOp.GREATER_THAN_OR_EQUAL, 1.0, 2.0) is False
