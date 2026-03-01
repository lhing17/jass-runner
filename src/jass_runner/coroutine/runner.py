"""协程运行器实现。"""

from typing import Any, List, Optional
from .coroutine import Coroutine
from .scheduler import SleepScheduler
from .errors import CoroutineStackOverflow
from . import CoroutineStatus
from .signals import SleepSignal


class CoroutineRunner:
    """协程调度器，与 SimulationLoop 集成。"""

    DEFAULT_MAX_COROUTINES = 100

    def __init__(self, max_coroutines: int = None):
        """
        参数：
            max_coroutines: 最大并发协程数，默认100
        """
        self._active: List[Coroutine] = []
        self._scheduler = SleepScheduler()
        self._current_time = 0.0
        self._frame_count = 0
        self.max_coroutines = max_coroutines or self.DEFAULT_MAX_COROUTINES
        self._main_coroutine: Optional[Coroutine] = None

    def execute_func(self, interpreter: Any, func: Any,
                     args: list = None) -> Coroutine:
        """
        ExecuteFunc - 创建新协程（简单顺序执行）。

        参数：
            interpreter: 解释器实例
            func: 函数定义
            args: 函数参数

        返回：
            新创建的协程

        异常：
            CoroutineStackOverflow: 如果协程数超过限制
        """
        args = args or []

        # 限制并发协程数
        total = len(self._active) + len(self._scheduler._sleeping)
        if total >= self.max_coroutines:
            raise CoroutineStackOverflow(
                f"协程数超过限制({self.max_coroutines})"
            )

        # 创建新协程
        coroutine = Coroutine(interpreter, func, args)
        coroutine.start()
        self._active.append(coroutine)
        return coroutine

    def update(self, delta_time: float):
        """
        每帧调用，更新协程状态。

        参数：
            delta_time: 时间增量（秒）
        """
        self._current_time += delta_time
        self._frame_count += 1

        # 1. 唤醒到期的协程
        ready = self._scheduler.wake_ready(self._current_time)
        self._active.extend(ready)

        # 2. 执行活跃协程
        still_active = []
        for coroutine in self._active:
            signal = coroutine.resume()

            if signal:  # 遇到 SleepSignal
                coroutine.sleep(signal.duration, self._current_time)
                self._scheduler.add(coroutine)
            elif coroutine.status == CoroutineStatus.FINISHED:
                pass  # 协程完成，不加入活跃列表
            else:
                still_active.append(coroutine)

        self._active = still_active

    def is_finished(self) -> bool:
        """
        检查所有协程是否完成。

        返回：
            True 如果所有协程都已完成
        """
        return (len(self._active) == 0 and
                self._scheduler.is_empty() and
                self._main_coroutine is not None and
                self._main_coroutine.status == CoroutineStatus.FINISHED)
