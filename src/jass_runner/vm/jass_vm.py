"""JASS 虚拟机。

此模块包含 JassVM 类，作为 JASS 执行的主要入口点，
集成了解析器、解释器、原生函数和计时器系统。
"""

import logging
from typing import Optional

from ..parser.parser import Parser
from ..interpreter.interpreter import Interpreter
from ..natives.factory import NativeFactory
from ..timer.system import TimerSystem
from ..timer.simulation import SimulationLoop


logger = logging.getLogger(__name__)


class JassVM:
    """JASS 虚拟机 - JASS 执行的主要入口点。"""

    def __init__(self, enable_timers: bool = True):
        """初始化 JASS 虚拟机。

        参数：
            enable_timers: 是否启用计时器系统
        """
        self.enable_timers = enable_timers

        # 初始化组件
        self.parser = None
        self.timer_system = TimerSystem() if enable_timers else None
        self.native_factory = NativeFactory(timer_system=self.timer_system)
        self.native_registry = self.native_factory.create_default_registry()
        self.interpreter = Interpreter(native_registry=self.native_registry)

        # 计时器的模拟循环
        self.simulation_loop: Optional[SimulationLoop] = None
        if enable_timers and self.timer_system:
            self.simulation_loop = SimulationLoop(self.timer_system)

        self.ast = None
        self.loaded = False

    def load_script(self, script_content: str):
        """加载并解析 JASS 脚本。"""
        self.parser = Parser(script_content)
        self.ast = self.parser.parse()
        self.loaded = True
        logger.info(f"已加载脚本，包含 {len(self.ast.functions) if hasattr(self.ast, 'functions') else 0} 个函数")

    def load_file(self, filepath: str):
        """从文件加载 JASS 脚本。"""
        with open(filepath, 'r', encoding='utf-8') as f:
            script_content = f.read()
        self.load_script(script_content)

    def execute(self):
        """执行已加载的脚本。"""
        if not self.loaded:
            raise RuntimeError("未加载脚本。请先调用 load_script()。")

        if self.ast is None:
            raise RuntimeError("解析脚本失败。没有可用的 AST。")

        logger.info("开始脚本执行")
        try:
            self.interpreter.execute(self.ast)
            logger.info("脚本执行成功完成")
        except Exception as e:
            logger.error(f"执行期间出错: {e}")
            raise

    def run_simulation(self, seconds: float = 10.0):
        """运行指定秒数的计时器模拟。"""
        if not self.enable_timers or not self.simulation_loop:
            logger.warning("计时器系统未启用")
            return

        logger.info(f"运行模拟 {seconds} 秒")
        self.simulation_loop.run_seconds(seconds)
        logger.info(f"模拟完成。模拟时间: {self.simulation_loop.get_simulated_time():.2f}秒")

    def run(self, script_content: str, simulate_seconds: float = 0.0):
        """加载并执行脚本，可选运行模拟。"""
        self.load_script(script_content)
        self.execute()

        if simulate_seconds > 0 and self.enable_timers:
            self.run_simulation(simulate_seconds)
