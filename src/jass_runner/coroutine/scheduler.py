"""协程调度器实现。"""

from typing import List
from .coroutine import Coroutine


class SleepScheduler:
    """管理所有睡眠中的协程。"""

    def __init__(self):
        self._sleeping: List[Coroutine] = []

    def add(self, coroutine: Coroutine):
        """添加睡眠中的协程。"""
        self._sleeping.append(coroutine)

    def wake_ready(self, current_time: float) -> List[Coroutine]:
        """获取并移除所有到期的协程。

        参数：
            current_time: 当前时间

        返回：
            到期的协程列表
        """
        ready = [c for c in self._sleeping
                 if current_time >= c.wake_time]
        self._sleeping = [c for c in self._sleeping
                         if current_time < c.wake_time]

        for c in ready:
            c.wake(current_time)

        return ready

    def is_empty(self) -> bool:
        """检查是否没有睡眠中的协程。"""
        return len(self._sleeping) == 0
