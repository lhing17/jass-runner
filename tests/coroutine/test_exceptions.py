"""测试协程异常定义。"""

import pytest


class TestSleepInterrupt:
    """测试 SleepInterrupt 异常类。"""

    def test_sleep_interrupt_creation(self):
        """测试 SleepInterrupt 异常可以被正确创建。"""
        from jass_runner.coroutine.exceptions import SleepInterrupt

        exc = SleepInterrupt(2.0)
        assert exc.duration == 2.0

    def test_sleep_interrupt_message(self):
        """测试 SleepInterrupt 异常的消息包含持续时间信息。"""
        from jass_runner.coroutine.exceptions import SleepInterrupt

        exc = SleepInterrupt(3.5)
        assert "3.5" in str(exc)
        assert "sleep" in str(exc).lower() or "等待" in str(exc)

    def test_sleep_interrupt_is_exception(self):
        """测试 SleepInterrupt 是 Exception 的子类。"""
        from jass_runner.coroutine.exceptions import SleepInterrupt

        assert issubclass(SleepInterrupt, Exception)

    def test_sleep_interrupt_zero_duration(self):
        """测试 SleepInterrupt 支持零持续时间。"""
        from jass_runner.coroutine.exceptions import SleepInterrupt

        exc = SleepInterrupt(0.0)
        assert exc.duration == 0.0
