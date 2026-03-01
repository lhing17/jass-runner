"""运行触发器示例 JASS 脚本。

此脚本演示如何使用 JassVM 运行触发器系统示例，
包括基础触发器、单位死亡事件和计时器触发器。
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import logging
from jass_runner.vm.jass_vm import JassVM


def run_example(script_name, title, simulate_seconds=0):
    """运行单个示例脚本。

    参数：
        script_name: JASS脚本文件名
        title: 示例标题
        simulate_seconds: 需要模拟运行的秒数，0表示不模拟
    """
    # 读取 JASS 脚本
    script_path = os.path.join(os.path.dirname(__file__), script_name)
    if not os.path.exists(script_path):
        print(f"Error: Script not found: {script_path}")
        return False

    with open(script_path, 'r', encoding='utf-8') as f:
        jass_code = f.read()

    print("\n" + "=" * 60)
    print(f"运行示例: {title}")
    print("=" * 60)

    # 创建启用计时器的虚拟机（触发器系统自动集成）
    vm = JassVM(enable_timers=True)

    try:
        # 加载并执行
        vm.load_script(jass_code)
        vm.execute()

        # 如果需要，运行模拟
        if simulate_seconds > 0:
            print(f"\n--- 模拟运行 {simulate_seconds} 秒 ---")
            vm.run_simulation(simulate_seconds)
            print("--- 模拟完成 ---")

        print(f"\n[成功] {title} 执行完成")
        return True

    except Exception as e:
        print(f"\n[错误] {title} 执行失败: {e}")
        return False


def main():
    # 设置日志 - 使用简洁格式
    logging.basicConfig(
        level=logging.INFO,
        format='%(message)s'
    )

    print("=" * 60)
    print("JASS Runner - 触发器系统示例")
    print("=" * 60)
    print("\n此脚本演示触发器系统的各种功能：")
    print("1. 基础触发器创建和事件注册")
    print("2. 单位死亡事件处理和条件过滤")
    print("3. 计时器事件和周期性触发")

    results = []

    # 1. 运行基础触发器示例
    results.append(run_example(
        'trigger_basic.j',
        '基础触发器示例',
        simulate_seconds=0
    ))

    # 2. 运行单位死亡事件示例
    results.append(run_example(
        'trigger_unit_death.j',
        '单位死亡事件处理示例',
        simulate_seconds=0
    ))

    # 3. 运行计时器触发器示例（需要模拟时间）
    results.append(run_example(
        'trigger_timer.j',
        '计时器触发器示例',
        simulate_seconds=12.0  # 运行12秒以观察多个触发
    ))

    # 显示总结果
    print("\n" + "=" * 60)
    print("示例运行总结")
    print("=" * 60)

    success_count = sum(1 for r in results if r)
    total_count = len(results)

    print(f"成功: {success_count}/{total_count}")

    if success_count == total_count:
        print("所有示例运行成功！")
    else:
        print("部分示例运行失败，请检查输出信息。")

    print("=" * 60)


if __name__ == "__main__":
    main()
