"""协程实现。"""

from typing import Any, Optional, Generator
from . import CoroutineStatus
from .signals import SleepSignal


class Coroutine:
    """包装 JASS 函数执行的协程。"""

    def __init__(self, interpreter: Any, func: Any, args: list = None):
        """
        参数：
            interpreter: 解释器实例
            func: 函数定义节点
            args: 函数参数列表
        """
        self.interpreter = interpreter
        self.func = func
        self.args = args or []
        self.status = CoroutineStatus.PENDING
        self.generator: Optional[Generator] = None
        self.wake_time: float = 0.0
        self.return_value: Any = None

    def start(self):
        """启动协程，创建生成器。"""
        self.generator = self._run()
        self.status = CoroutineStatus.RUNNING

    def _run(self):
        """实际的生成器函数（子类实现）。"""
        raise NotImplementedError()

    def resume(self):
        """恢复执行。"""
        raise NotImplementedError()

    def wake(self, current_time: float):
        """从睡眠中唤醒。"""
        raise NotImplementedError()

    def sleep(self, duration: float, current_time: float):
        """设置睡眠状态。"""
        raise NotImplementedError()
