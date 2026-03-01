"""协程系统模块。

此模块包含协程执行引擎和信号系统，用于支持JASS脚本的异步执行。
"""

from enum import Enum


class CoroutineStatus(Enum):
    """协程状态枚举。"""
    PENDING = "pending"      # 刚创建，未开始执行
    RUNNING = "running"      # 正在执行
    SLEEPING = "sleeping"    # 调用 TriggerSleepAction 后暂停
    FINISHED = "finished"    # 执行完成
