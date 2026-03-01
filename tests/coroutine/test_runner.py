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
