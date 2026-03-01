"""协程系统模块。

提供 JASS 异步执行支持，包括 TriggerSleepAction 和 ExecuteFunc。
"""

from enum import Enum


class CoroutineStatus(Enum):
    """协程状态枚举。"""
    PENDING = "pending"      # 刚创建，未开始执行
    RUNNING = "running"      # 正在执行
    SLEEPING = "sleeping"    # 调用 TriggerSleepAction 后暂停
    FINISHED = "finished"    # 执行完成


from .signals import SleepSignal
from .exceptions import SleepInterrupt
from .coroutine import Coroutine
from .scheduler import SleepScheduler
from .runner import CoroutineRunner
from .errors import CoroutineError, CoroutineStackOverflow

__all__ = [
    'CoroutineStatus',
    'SleepSignal',
    'SleepInterrupt',
    'Coroutine',
    'SleepScheduler',
    'CoroutineRunner',
    'CoroutineError',
    'CoroutineStackOverflow',
]
