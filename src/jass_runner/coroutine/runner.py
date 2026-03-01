"""协程运行器实现。"""

from typing import Any, List, Optional
from .coroutine import Coroutine
from .scheduler import SleepScheduler


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
