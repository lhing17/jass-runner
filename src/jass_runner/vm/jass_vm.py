"""JASS 虚拟机。

此模块包含 JassVM 类，作为 JASS 执行的主要入口点，
集成了解析器、解释器、原生函数和计时器系统。
"""

import logging
import os
import re
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
        self.blizzard_ast = None  # 存储 blizzard.j 的 AST
        self.blizzard_loaded = False  # blizzard.j 是否已加载

        # 加载 common.j 中的常量
        self._load_constants()

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

    def load_blizzard(self, path: str = None) -> bool:
        """
        加载 blizzard.j 作为前置脚本。

        参数:
            path: blizzard.j 的路径，None 则自动查找 resources/blizzard.j

        返回:
            bool: 加载成功返回 True，失败返回 False（仅记录警告）
        """
        # 自动查找路径
        if path is None:
            path = self._find_blizzard_path()
            if path is None:
                logger.warning("未找到 blizzard.j，已跳过加载")
                return False

        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()

            parser = Parser(content)
            self.blizzard_ast = parser.parse()
            self.blizzard_loaded = True
            logger.info(f"blizzard.j 已加载: {path}")
            return True

        except FileNotFoundError:
            logger.warning(f"blizzard.j 文件未找到: {path}")
            return False
        except Exception as e:
            logger.warning(f"blizzard.j 解析失败: {e}")
            return False

    def _find_blizzard_path(self) -> Optional[str]:
        """自动查找 blizzard.j 的默认路径。"""
        possible_paths = [
            'resources/blizzard.j',
            os.path.join(os.path.dirname(__file__), '..', '..', '..', 'resources', 'blizzard.j'),
            os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'resources', 'blizzard.j'),
        ]

        for p in possible_paths:
            normalized = os.path.normpath(p)
            if os.path.exists(normalized):
                return normalized
        return None

    def execute(self):
        """执行已加载的脚本。"""
        if not self.loaded:
            raise RuntimeError("未加载脚本。请先调用 load_script()。")

        if self.ast is None:
            raise RuntimeError("解析脚本失败。没有可用的 AST。")

        logger.info("开始脚本执行")
        try:
            # 如果已加载 blizzard.j，先执行它
            if self.blizzard_loaded and self.blizzard_ast is not None:
                logger.debug("执行 blizzard.j")
                self.interpreter.execute(self.blizzard_ast)

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

    def run(self, script_content: str, simulate_seconds: float = 0.0,
            load_blizzard: bool = False, blizzard_path: str = None):
        """
        加载并执行脚本，可选运行模拟。

        参数:
            script_content: JASS 脚本内容
            simulate_seconds: 模拟秒数
            load_blizzard: 是否加载 blizzard.j
            blizzard_path: 自定义 blizzard.j 路径
        """
        if load_blizzard:
            self.load_blizzard(blizzard_path)

        self.load_script(script_content)
        self.execute()

        if simulate_seconds > 0 and self.enable_timers:
            self.run_simulation(simulate_seconds)

    def _load_constants(self):
        """从 common.j 加载常量定义。"""
        common_j_paths = [
            'resources/common.j',
            os.path.join(os.path.dirname(__file__), '..', '..', '..', 'resources', 'common.j')
        ]

        for path in common_j_paths:
            if os.path.exists(path):
                self._parse_constants_from_file(path)
                break

    def _parse_constants_from_file(self, filepath: str):
        """解析文件中的常量定义。"""
        constant_pattern = re.compile(
            r'constant\s+(\w+)\s+(\w+)\s*=\s*([^\s]+)',
            re.MULTILINE
        )

        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        for match in constant_pattern.finditer(content):
            const_type = match.group(1)  # integer, real, boolean, etc.
            const_name = match.group(2)   # CAMERA_MARGIN_LEFT
            const_value = match.group(3) # 0, true, etc.

            # 转换值为Python类型并存储到解释器的全局变量
            value = self._convert_constant_value(const_type, const_value)
            self.interpreter.global_context.variables[const_name] = value

    def _convert_constant_value(self, const_type: str, const_value: str):
        """将JASS常量值转换为Python值。"""
        if const_type == 'integer':
            try:
                return int(const_value)
            except ValueError:
                return 0
        elif const_type == 'real':
            try:
                return float(const_value)
            except ValueError:
                return 0.0
        elif const_type == 'boolean':
            return const_value.lower() == 'true'
        else:
            # 对于handle类型和其他类型，存储字符串值
            return const_value
