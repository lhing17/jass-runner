"""异步相关 native 函数实现。

此模块包含与协程和异步执行相关的 JASS native 函数。
"""

from .base import NativeFunction
from ..coroutine.exceptions import SleepInterrupt


class TriggerSleepAction(NativeFunction):
    """JASS 原生函数：暂停当前协程指定时间。"""

    @property
    def name(self) -> str:
        return "TriggerSleepAction"

    def execute(self, state_context, timeout: float) -> None:
        """
        参数：
            state_context: 状态上下文
            timeout: 等待时间（秒）

        异常：
            SleepInterrupt: 总是抛出，用于挂起当前协程
        """
        raise SleepInterrupt(timeout)
