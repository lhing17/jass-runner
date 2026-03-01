"""协程运行器实现。"""

from typing import Any, List, Optional
from .coroutine import Coroutine
from .scheduler import SleepScheduler
from .errors import CoroutineStackOverflow


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
