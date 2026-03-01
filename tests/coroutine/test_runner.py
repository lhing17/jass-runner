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

    def test_runner_update(self):
        """测试 CoroutineRunner 的 update 方法。"""
        from unittest.mock import Mock, MagicMock
        from jass_runner.coroutine.runner import CoroutineRunner
        from jass_runner.coroutine import CoroutineStatus

        runner = CoroutineRunner()

        # 创建一个模拟协程
        mock_coroutine = Mock()
        mock_coroutine.status = CoroutineStatus.RUNNING
        mock_coroutine.resume.return_value = None  # 不睡眠，直接完成

        # 模拟 resume 后状态变为 FINISHED
        def side_effect():
            mock_coroutine.status = CoroutineStatus.FINISHED
            return None

        mock_coroutine.resume.side_effect = side_effect

        runner._active.append(mock_coroutine)

        # 执行一帧更新
        runner.update(0.033)  # 约30fps

        assert runner._current_time == 0.033
        assert runner._frame_count == 1
        # 协程已完成，应从活跃列表移除
        assert len(runner._active) == 0

    def test_runner_is_finished(self):
        """测试 CoroutineRunner 的 is_finished 方法。"""
        from unittest.mock import Mock
        from jass_runner.coroutine.runner import CoroutineRunner
        from jass_runner.coroutine import CoroutineStatus

        runner = CoroutineRunner()

        # 初始状态：未开始，不算完成
        assert not runner.is_finished()

        # 设置主协程
        mock_main = Mock()
        mock_main.status = CoroutineStatus.PENDING
        runner._main_coroutine = mock_main

        assert not runner.is_finished()

        # 主协程完成
        mock_main.status = CoroutineStatus.FINISHED
        assert runner.is_finished()
