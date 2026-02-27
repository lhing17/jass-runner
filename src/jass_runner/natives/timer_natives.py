"""与计时器相关的原生函数。"""

import logging
from ..natives.base import NativeFunction
from ..timer.timer import Timer


logger = logging.getLogger(__name__)


class CreateTimer(NativeFunction):
    """创建一个新计时器。"""

    def __init__(self, timer_system):
        self._timer_system = timer_system

    @property
    def name(self) -> str:
        return "CreateTimer"

    def execute(self, state_context, *args, **kwargs) -> Timer:
        """执行 CreateTimer 原生函数。

        参数：
            state_context: 状态上下文

        返回：
            Timer: 创建的计时器对象
        """
        timer_id = self._timer_system.create_timer()
        timer = self._timer_system.get_timer(timer_id)
        logger.info(f"[CreateTimer] Created timer: {timer_id}")
        return timer


class TimerStart(NativeFunction):
    """启动一个计时器。"""

    def __init__(self, timer_system):
        self._timer_system = timer_system

    @property
    def name(self) -> str:
        return "TimerStart"

    def execute(self, state_context, timer: Timer, timeout: float, periodic: bool, callback_func, *args):
        """执行 TimerStart 原生函数。

        参数：
            state_context: 状态上下文
            timer: Timer 对象
            timeout: 超时时间（秒）
            periodic: 是否周期性触发
            callback_func: 回调函数
            *args: 额外参数

        返回：
            bool: 是否成功启动
        """
        if not timer or not isinstance(timer, Timer):
            logger.warning(f"[TimerStart] Invalid timer: {timer}")
            return False

        timer_id = timer.timer_id

        # 在实际实现中，callback_func 将是一个 JASS 函数引用
        # 目前，我们创建一个包装器来调用回调并记录日志
        def callback_wrapper():
            logger.info(f"[TimerCallback] Timer {timer_id} fired with args: {args}")
            if callback_func and callable(callback_func):
                callback_func()

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

    def execute(self, state_context, timer: Timer) -> float:
        """执行 TimerGetElapsed 原生函数。

        参数：
            state_context: 状态上下文
            timer: Timer 对象

        返回：
            float: 经过的时间，如果计时器无效则返回 0.0
        """
        if not timer or not isinstance(timer, Timer):
            logger.warning(f"[TimerGetElapsed] Invalid timer: {timer}")
            return 0.0

        elapsed = timer.elapsed
        logger.info(f"[TimerGetElapsed] Timer {timer.timer_id} elapsed: {elapsed}")
        return elapsed


class DestroyTimer(NativeFunction):
    """销毁一个计时器。"""

    def __init__(self, timer_system):
        self._timer_system = timer_system

    @property
    def name(self) -> str:
        return "DestroyTimer"

    def execute(self, state_context, timer: Timer):
        """执行 DestroyTimer 原生函数。

        参数：
            state_context: 状态上下文
            timer: Timer 对象

        返回：
            bool: 是否成功销毁
        """
        if not timer or not isinstance(timer, Timer):
            logger.warning(f"[DestroyTimer] Invalid timer: {timer}")
            return False

        timer_id = timer.timer_id
        timer.destroy()
        success = self._timer_system.destroy_timer(timer_id)
        if success:
            logger.info(f"[DestroyTimer] Destroyed timer: {timer_id}")
        else:
            logger.warning(f"[DestroyTimer] Timer not found: {timer_id}")
        return success


class PauseTimer(NativeFunction):
    """暂停一个计时器。"""

    def __init__(self, timer_system):
        self._timer_system = timer_system

    @property
    def name(self) -> str:
        return "PauseTimer"

    def execute(self, state_context, timer: Timer):
        """执行 PauseTimer 原生函数。

        参数：
            state_context: 状态上下文
            timer: Timer 对象

        返回：
            bool: 是否成功暂停
        """
        if not timer or not isinstance(timer, Timer):
            logger.warning(f"[PauseTimer] Invalid timer: {timer}")
            return False

        timer.pause()
        logger.info(f"[PauseTimer] Paused timer: {timer.timer_id}")
        return True


class ResumeTimer(NativeFunction):
    """恢复一个计时器。"""

    def __init__(self, timer_system):
        self._timer_system = timer_system

    @property
    def name(self) -> str:
        return "ResumeTimer"

    def execute(self, state_context, timer: Timer):
        """执行 ResumeTimer 原生函数。

        参数：
            state_context: 状态上下文
            timer: Timer 对象

        返回：
            bool: 是否成功恢复
        """
        if not timer or not isinstance(timer, Timer):
            logger.warning(f"[ResumeTimer] Invalid timer: {timer}")
            return False

        timer.resume()
        logger.info(f"[ResumeTimer] Resumed timer: {timer.timer_id}")
        return True
