"""协程异常定义。"""


class SleepInterrupt(Exception):
    """睡眠中断异常，用于从深层调用栈传递睡眠信号。"""

    def __init__(self, duration: float):
        """
        参数：
            duration: 等待时间（秒）
        """
        super().__init__(f"Sleep for {duration} seconds")
        self.duration = duration
