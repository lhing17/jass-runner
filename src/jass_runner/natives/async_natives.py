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


class ExecuteFunc(NativeFunction):
    """JASS 原生函数：创建新协程执行指定函数。"""

    def __init__(self):
        """初始化 ExecuteFunc，interpreter 将通过属性设置。"""
        self.interpreter = None

    @property
    def name(self) -> str:
        return "ExecuteFunc"

    def execute(self, state_context, func_name: str) -> None:
        """
        参数：
            state_context: 状态上下文
            func_name: 要执行的函数名称

        行为：
            创建新协程执行函数，但不等待其完成
            当前协程继续执行
        """
        if not self.interpreter:
            return  # interpreter 未设置，静默返回

        func = self.interpreter.functions.get(func_name)
        if not func:
            return  # 函数不存在静默返回

        self.interpreter.coroutine_runner.execute_func(
            self.interpreter, func, []
        )
