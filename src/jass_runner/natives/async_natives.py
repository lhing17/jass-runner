"""异步相关 native 函数实现。

此模块包含与协程和异步执行相关的 JASS native 函数。
"""

from .base import NativeFunction
from ..coroutine.exceptions import SleepInterrupt
import logging

logger = logging.getLogger(__name__)


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
        # 从 state_context 获取 interpreter
        # 注意：这里假设 state_context.interpreter 是可用的
        # 在 Interpreter.execute_function 中，我们将 interpreter 注入到了 state_context
        interpreter = getattr(state_context, 'interpreter', None)

        if not interpreter:
            logger.warning("[ExecuteFunc] 无法获取 interpreter 实例")
            return

        func = interpreter.functions.get(func_name)
        if not func:
            logger.warning(f"[ExecuteFunc] 函数未找到: {func_name}")
            return

        if not interpreter.coroutine_runner:
             logger.warning("[ExecuteFunc] 协程运行器未初始化")
             return

        interpreter.coroutine_runner.execute_func(
            interpreter, func, []
        )
