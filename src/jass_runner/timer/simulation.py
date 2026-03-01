"""基于帧的模拟循环。

此模块包含 SimulationLoop 类，用于基于帧的计时器系统模拟。
"""

from typing import Callable, Optional, Any
from .system import TimerSystem
from ..coroutine import CoroutineRunner


class SimulationLoop:
    """用于 JASS 计时器系统和协程的基于帧的模拟循环。

    此类通过离散时间步长（帧）而非实时来模拟计时器系统，
    允许快速模拟长时间的游戏行为。同时集成协程运行器，
    支持 JASS 脚本的异步执行。
    """

    def __init__(self, timer_system: TimerSystem = None, fps: float = 30.0, frame_duration: float = None):
        """初始化模拟循环。

        参数：
            timer_system: TimerSystem 实例（可选，如果不提供则创建新的）
            fps: 每秒帧数，默认为 30.0 FPS
            frame_duration: 每帧的持续时间（秒），如果设置则覆盖 fps 参数（向后兼容）
        """
        if frame_duration is not None:
            self.frame_duration = frame_duration
            self.fps = 1.0 / frame_duration
        else:
            self.fps = fps
            self.frame_duration = 1.0 / fps

        self.current_time = 0.0
        self.frame_count = 0
        self.timer_system = timer_system if timer_system else TimerSystem()
        self.coroutine_runner = CoroutineRunner()
        self._running = False
        self._frame_callback: Optional[Callable] = None

    def run(self, interpreter: Any, ast: Any, max_frames: int = None) -> dict:
        """运行模拟（主入口）。

        参数：
            interpreter: 解释器实例
            ast: AST 根节点
            max_frames: 最大帧数限制（可选）

        返回：
            包含 'frames'、'time'、'success' 的字典
        """
        self._running = True
        self._start_main(interpreter, ast)

        while self._running:
            self._update_frame()
            if self.coroutine_runner.is_finished():
                break
            if max_frames and self.frame_count >= max_frames:
                break

        return {
            'frames': self.frame_count,
            'time': self.current_time,
            'success': self.coroutine_runner.is_finished()
        }

    def _update_frame(self):
        """单帧更新。"""
        delta = self.frame_duration
        self.current_time += delta
        self.frame_count += 1
        self.coroutine_runner.update(delta)
        self.timer_system.update(delta)

    def _start_main(self, interpreter: Any, ast: Any):
        """启动主协程。

        参数：
            interpreter: 解释器实例
            ast: AST 根节点
        """
        from ..interpreter.coroutine import JassCoroutine

        # 初始化全局变量
        if hasattr(ast, 'globals') and ast.globals:
            for global_decl in ast.globals:
                interpreter.execute_global_declaration(global_decl)

        # 注册所有函数
        if hasattr(ast, 'functions'):
            for func in ast.functions:
                interpreter.functions[func.name] = func

        # 查找 main 函数并创建协程
        main_func = interpreter.functions.get('main')
        if main_func:
            coroutine = JassCoroutine(interpreter, main_func)
            coroutine.start()
            self.coroutine_runner._active.append(coroutine)
            self.coroutine_runner._main_coroutine = coroutine

    def run_frames(self, num_frames: int):
        """运行指定帧数的模拟。

        参数：
            num_frames: 要运行的帧数
        """
        for i in range(num_frames):
            self._update_frame()

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
        return self.frame_count * self.frame_duration
