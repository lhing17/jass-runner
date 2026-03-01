"""协程信号定义。

此模块包含协程执行过程中使用的各种信号类，
用于控制协程的暂停、恢复等行为。
"""


class SleepSignal:
    """协程暂停信号，携带等待时间。

    当协程需要暂停执行一段时间时，会抛出此信号。
    调度器捕获该信号后，会在指定时间后恢复协程执行。
    """

    def __init__(self, duration: float):
        """
        参数：
            duration: 等待时间（秒）
        """
        self.duration = duration
