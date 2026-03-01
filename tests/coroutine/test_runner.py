"""测试协程运行器。"""

import pytest


class TestCoroutineRunner:
    """测试 CoroutineRunner 类。"""

    def test_runner_creation(self):
        """测试 CoroutineRunner 创建。"""
        from jass_runner.coroutine.runner import CoroutineRunner

        runner = CoroutineRunner()

        assert runner._active == []
        assert runner._current_time == 0.0
        assert runner._frame_count == 0
        assert runner.max_coroutines == 100
        assert runner._main_coroutine is None

    def test_runner_execute_func(self):
        """测试 ExecuteFunc 创建新协程。"""
        from unittest.mock import Mock
        from jass_runner.coroutine.runner import CoroutineRunner
        from jass_runner.coroutine import CoroutineStatus

        runner = CoroutineRunner()
        interpreter = Mock()
        func = Mock()
        func.body = []  # 空函数体

        coroutine = runner.execute_func(interpreter, func)

        assert coroutine is not None
        assert coroutine.status == CoroutineStatus.RUNNING
        assert len(runner._active) == 1
