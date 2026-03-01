"""测试协程调度器。"""

import pytest
from unittest.mock import Mock

from jass_runner.coroutine.coroutine import Coroutine
from jass_runner.coroutine.scheduler import SleepScheduler


class TestSleepScheduler:
    """测试 SleepScheduler 类。"""

    def test_scheduler_add_and_wake(self):
        """测试调度器添加和唤醒。"""
        scheduler = SleepScheduler()
        coroutine = Coroutine(Mock(), Mock())
        coroutine.sleep(2.0, 10.0)

        scheduler.add(coroutine)
        assert not scheduler.is_empty()

        # 时间未到，不应唤醒
        ready = scheduler.wake_ready(11.0)
        assert len(ready) == 0

        # 时间到了，应该唤醒
        ready = scheduler.wake_ready(12.0)
        assert len(ready) == 1
        assert ready[0] is coroutine
        assert scheduler.is_empty()

    def test_scheduler_empty_initially(self):
        """测试调度器初始状态为空。"""
        scheduler = SleepScheduler()
        assert scheduler.is_empty()

    def test_scheduler_wake_multiple_coroutines(self):
        """测试调度器唤醒多个协程。"""
        scheduler = SleepScheduler()

        coroutine1 = Coroutine(Mock(), Mock())
        coroutine1.sleep(1.0, 10.0)  # 在 11.0 唤醒

        coroutine2 = Coroutine(Mock(), Mock())
        coroutine2.sleep(2.0, 10.0)  # 在 12.0 唤醒

        coroutine3 = Coroutine(Mock(), Mock())
        coroutine3.sleep(3.0, 10.0)  # 在 13.0 唤醒

        scheduler.add(coroutine1)
        scheduler.add(coroutine2)
        scheduler.add(coroutine3)

        # 时间 11.5，只有 coroutine1 应该被唤醒
        ready = scheduler.wake_ready(11.5)
        assert len(ready) == 1
        assert ready[0] is coroutine1
        assert not scheduler.is_empty()

        # 时间 12.5，coroutine2 应该被唤醒
        ready = scheduler.wake_ready(12.5)
        assert len(ready) == 1
        assert ready[0] is coroutine2
        assert not scheduler.is_empty()

        # 时间 13.5，coroutine3 应该被唤醒
        ready = scheduler.wake_ready(13.5)
        assert len(ready) == 1
        assert ready[0] is coroutine3
        assert scheduler.is_empty()

    def test_scheduler_wake_all_at_same_time(self):
        """测试调度器同时唤醒所有到期的协程。"""
        scheduler = SleepScheduler()

        coroutine1 = Coroutine(Mock(), Mock())
        coroutine1.sleep(2.0, 10.0)  # 在 12.0 唤醒

        coroutine2 = Coroutine(Mock(), Mock())
        coroutine2.sleep(2.0, 10.0)  # 在 12.0 唤醒

        scheduler.add(coroutine1)
        scheduler.add(coroutine2)

        # 时间 12.0，两个都应该被唤醒
        ready = scheduler.wake_ready(12.0)
        assert len(ready) == 2
        assert scheduler.is_empty()

    def test_scheduler_wake_updates_status(self):
        """测试调度器唤醒时更新协程状态。"""
        from jass_runner.coroutine import CoroutineStatus

        scheduler = SleepScheduler()
        coroutine = Coroutine(Mock(), Mock())
        coroutine.sleep(2.0, 10.0)

        assert coroutine.status == CoroutineStatus.SLEEPING

        scheduler.add(coroutine)
        ready = scheduler.wake_ready(12.0)

        assert len(ready) == 1
        assert coroutine.status == CoroutineStatus.RUNNING
