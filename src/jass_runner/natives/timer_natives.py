"""与计时器相关的原生函数。"""

import logging
from ..natives.base import NativeFunction


logger = logging.getLogger(__name__)


class CreateTimer(NativeFunction):
    """创建一个新计时器。"""

    def __init__(self, timer_system):
        self._timer_system = timer_system

    @property
    def name(self) -> str:
        return "CreateTimer"

    def execute(self, state_context, *args, **kwargs):
        """执行 CreateTimer 原生函数。"""
        timer_id = self._timer_system.create_timer()
        logger.info(f"[CreateTimer] Created timer: {timer_id}")
        return timer_id


class TimerStart(NativeFunction):
    """启动一个计时器。"""

    def __init__(self, timer_system):
        self._timer_system = timer_system

    @property
    def name(self) -> str:
        return "TimerStart"

    def execute(self, state_context, timer_id: str, timeout: float, periodic: bool, callback_func: str, *args):
        """执行 TimerStart 原生函数。"""
        timer = self._timer_system.get_timer(timer_id)
        if not timer:
            logger.warning(f"[TimerStart] Timer not found: {timer_id}")
            return False

        # 在实际实现中，callback_func 将是一个 JASS 函数引用
        # 目前，我们创建一个简单的回调来记录日志
        def callback_wrapper():
            logger.info(f"[TimerCallback] Timer {timer_id} fired with args: {args}")

        timer.start(timeout, periodic, callback_wrapper, *args)
        logger.info(f"[TimerStart] Started timer {timer_id}: timeout={timeout}, periodic={periodic}")
        return True


class TimerGetElapsed(NativeFunction):
    """获取计时器的经过时间。"""

    def __init__(self, timer_system):
        self._timer_system = timer_system

    @property
    def name(self) -> str:
        return "TimerGetElapsed"

    def execute(self, state_context, timer_id: str):
        """执行 TimerGetElapsed 原生函数。"""
        elapsed = self._timer_system.get_elapsed_time(timer_id)
        if elapsed is None:
            logger.warning(f"[TimerGetElapsed] Timer not found: {timer_id}")
            return 0.0

        logger.info(f"[TimerGetElapsed] Timer {timer_id} elapsed: {elapsed}")
        return elapsed
