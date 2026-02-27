"""运行完整的 JASS 示例。"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import logging
from jass_runner.vm.jass_vm import JassVM


def main():
    # 设置日志
    logging.basicConfig(level=logging.INFO, format='%(message)s')

    # 读取 JASS 脚本
    script_path = os.path.join(os.path.dirname(__file__), 'complete_example.j')
    with open(script_path, 'r', encoding='utf-8') as f:
        jass_code = f.read()

    # 创建启用计时器的虚拟机
    vm = JassVM(enable_timers=True)

    print("=" * 60)
    print("JASS 运行器 - 完整示例")
    print("=" * 60)

    # 加载并执行
    vm.load_script(jass_code)
    vm.execute()

    # 运行 10 秒模拟
    print("\n" + "=" * 60)
    print("运行模拟 10 秒...")
    print("=" * 60)
    vm.run_simulation(10.0)

    print("\n" + "=" * 60)
    print("模拟完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()
