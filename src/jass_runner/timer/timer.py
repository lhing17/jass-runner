"""用于 JASS 计时器模拟的 Timer 类。"""

from typing import Callable, Optional


class Timer:
    """表示一个 JASS 计时器。"""

    def __init__(self, timer_id: str):
        self.timer_id = timer_id
        self.elapsed: float = 0.0
        self.timeout: float = 0.0
        self.periodic: bool = False
        self.running: bool = False
        self.callback: Optional[Callable] = None
        self.callback_args = ()

    def start(self, timeout: float, periodic: bool, callback: Callable, *args):
        """启动计时器。"""
        self.timeout = timeout
        self.periodic = periodic
        self.callback = callback
        self.callback_args = args
        self.running = True
        self.elapsed = 0.0

    def update(self, delta_time: float) -> bool:
        """更新计时器的经过时间。如果计时器触发则返回 True。"""
        if not self.running:
            return False

        self.elapsed += delta_time

        if self.elapsed >= self.timeout:
            if self.callback:
                self.callback(*self.callback_args)

            if self.periodic:
                self.elapsed = 0.0
                return True
            else:
                self.running = False
                return True

        return False

    def pause(self):
        """暂停计时器。"""
        self.running = False

    def resume(self):
        """恢复计时器。"""
        self.running = True

    def destroy(self):
        """销毁计时器。"""
        self.running = False
        self.callback = None
        self.callback_args = ()
