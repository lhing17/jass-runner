"""运行计时器示例 JASS 脚本。"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import logging
from jass_runner.parser.parser import Parser
from jass_runner.interpreter.interpreter import Interpreter
from jass_runner.timer.system import TimerSystem
from jass_runner.timer.simulation import SimulationLoop
from jass_runner.natives.factory import NativeFactory


def main():
    # 设置日志
    logging.basicConfig(level=logging.INFO, format='%(message)s')

    # 读取 JASS 脚本
    script_path = os.path.join(os.path.dirname(__file__), 'timer_example.j')
    with open(script_path, 'r', encoding='utf-8') as f:
        jass_code = f.read()

    # 创建系统
    timer_system = TimerSystem()
    factory = NativeFactory(timer_system=timer_system)
    registry = factory.create_default_registry()

    # 解析和解释
    parser = Parser(jass_code)
    ast = parser.parse()

    interpreter = Interpreter(native_registry=registry)
    interpreter.execute(ast)

    # 运行模拟
    simulation = SimulationLoop(timer_system)
    print(f"Running simulation for 5 seconds...")
    simulation.run_seconds(5.0)
    print(f"Simulation complete. Simulated time: {simulation.get_simulated_time():.2f}s")


if __name__ == "__main__":
    main()
