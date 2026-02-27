"""基于帧的模拟循环。

此模块包含 SimulationLoop 类，用于基于帧的计时器系统模拟。
"""

from typing import Callable, Optional
from .system import TimerSystem


class SimulationLoop:
    """用于 JASS 计时器系统的基于帧的模拟循环。

    此类通过离散时间步长（帧）而非实时来模拟计时器系统，
    允许快速模拟长时间的游戏行为。
    """

    def __init__(self, timer_system: TimerSystem, frame_duration: float = 0.033):
        """初始化模拟循环。

        参数：
            timer_system: TimerSystem 实例
            frame_duration: 每帧的持续时间（秒），默认为 0.033（约 30 FPS）
        """
        self.timer_system = timer_system
        self.frame_duration = frame_duration
        self.current_frame: int = 0
        self.running: bool = False
        self._frame_callback: Optional[Callable] = None

    def run_frames(self, num_frames: int):
        """运行指定帧数的模拟。

        参数：
            num_frames: 要运行的帧数
        """
        self.running = True

        for i in range(num_frames):
            # 累加当前帧数
            self.current_frame += 1

            # 如果设置了帧回调，则调用
            if self._frame_callback:
                self._frame_callback(self.current_frame)

            # 使用帧持续时间更新计时器系统
            self.timer_system.update(self.frame_duration)

            # 模拟帧延迟（在实际模拟中，这是真实时间）
            # 为了快速模拟，我们实际上不睡眠

        self.running = False

    def run_seconds(self, seconds: float):
        """运行指定秒数的模拟。

        参数：
            seconds: 要模拟的秒数
        """
        num_frames = int(seconds / self.frame_duration)
        self.run_frames(num_frames)

    def set_frame_callback(self, callback: Callable):
        """设置每帧调用的回调函数。

        参数：
            callback: 每帧调用的回调函数，接收帧号作为参数
        """
        self._frame_callback = callback

    def get_simulated_time(self) -> float:
        """获取总模拟时间（秒）。

        返回：
            总模拟时间（秒）
        """
        return self.current_frame * self.frame_duration
