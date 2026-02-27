"""状态管理系统演示脚本。

此脚本演示JASS Runner状态管理系统的核心功能。
"""

import sys
import os

# 添加src到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from jass_runner.natives.state import StateContext
from jass_runner.natives.manager import HandleManager
from jass_runner.utils.memory import MemoryTracker
from jass_runner.utils.performance import PerformanceMonitor, track_performance, get_global_monitor, reset_global_monitor


def demo_basic_operations():
    """演示基础操作。"""
    print("=" * 50)
    print("演示1: 基础单位操作")
    print("=" * 50)

    manager = HandleManager()

    # 创建单位
    unit = manager.create_unit("hfoo", 0, 100.0, 200.0, 270.0)
    print(f"创建单位: {unit.id}")

    # 查询状态
    print(f"单位类型: {unit.unit_type}")
    print(f"所属玩家: {unit.player_id}")
    print(f"位置: ({unit.x}, {unit.y})")
    print(f"面向: {unit.facing}")

    # 查询生命值
    life = manager.get_unit_state(unit.id, "UNIT_STATE_LIFE")
    max_life = manager.get_unit_state(unit.id, "UNIT_STATE_MAX_LIFE")
    print(f"生命值: {life}/{max_life}")

    # 单位受伤
    manager.set_unit_state(unit.id, "UNIT_STATE_LIFE", 50.0)
    print(f"受伤后生命值: {manager.get_unit_state(unit.id, 'UNIT_STATE_LIFE')}")

    # 销毁单位
    manager.destroy_handle(unit.id)
    print(f"单位已销毁，存活状态: {manager.get_unit(unit.id) is None}")
    print()


def demo_multi_player():
    """演示多玩家场景。"""
    print("=" * 50)
    print("演示2: 多玩家场景")
    print("=" * 50)

    manager = HandleManager()

    # 为4个玩家各创建单位
    player_units = {}
    for player_id in range(4):
        player_units[player_id] = []
        for i in range(3):
            unit = manager.create_unit(
                "hfoo",
                player_id,
                float(player_id * 100),
                float(i * 50),
                0.0
            )
            player_units[player_id].append(unit)

    # 显示统计
    print(f"总handle数: {manager.get_total_handles()}")
    print(f"存活handle数: {manager.get_alive_handles()}")
    print(f"单位类型数: {manager.get_handle_type_count('unit')}")

    # 显示每个玩家的单位
    for player_id, units in player_units.items():
        print(f"玩家{player_id}: {len(units)}个单位")

    # 模拟战斗：玩家1杀死玩家0的一个单位
    target = player_units[0][0]
    manager.destroy_handle(target.id)
    print(f"\n玩家1杀死玩家0的单位: {target.id}")
    print(f"存活handle数: {manager.get_alive_handles()}")
    print()


def demo_state_context():
    """演示状态上下文。"""
    print("=" * 50)
    print("演示3: 状态上下文")
    print("=" * 50)

    state = StateContext()

    # 创建单位
    unit = state.handle_manager.create_unit("hfoo", 0, 100.0, 200.0, 270.0)
    print(f"创建单位: {unit.id}")

    # 使用全局变量
    state.global_vars["game_time"] = 0.0
    state.global_vars["winner"] = None
    print(f"全局变量: {state.global_vars}")

    # 使用上下文局部存储
    store_a = state.get_context_store("context_a")
    store_a["temp_data"] = "value_a"

    store_b = state.get_context_store("context_b")
    store_b["temp_data"] = "value_b"

    print(f"上下文A存储: {store_a}")
    print(f"上下文B存储: {store_b}")
    print()


def demo_memory_tracking():
    """演示内存监控。"""
    print("=" * 50)
    print("演示4: 内存监控")
    print("=" * 50)

    tracker = MemoryTracker()
    manager = HandleManager()

    tracker.snapshot("初始状态")

    # 创建大量单位
    print("创建1000个单位...")
    for i in range(1000):
        manager.create_unit("hfoo", 0, float(i), float(i), 0.0)

    tracker.snapshot("创建1000单位后")

    # 销毁一半
    print("销毁500个单位...")
    for handle_id in list(manager._handles.keys())[:500]:
        manager.destroy_handle(handle_id)

    tracker.snapshot("销毁500单位后")

    # 显示统计
    stats = tracker.get_stats()
    print(f"\n内存统计:")
    print(f"  快照数量: {stats['snapshots_count']}")

    handle_stats = {
        "total": manager.get_total_handles(),
        "alive": manager.get_alive_handles(),
    }
    print(f"\nHandle统计:")
    print(f"  总数: {handle_stats['total']}")
    print(f"  存活: {handle_stats['alive']}")
    print()


def demo_performance_monitoring():
    """演示性能监控。"""
    print("=" * 50)
    print("演示5: 性能监控")
    print("=" * 50)

    reset_global_monitor()
    manager = HandleManager()

    @track_performance("create_unit_batch")
    def create_batch(count):
        for i in range(count):
            manager.create_unit("hfoo", 0, float(i), float(i), 0.0)

    @track_performance("get_unit_batch")
    def get_batch(unit_ids):
        for unit_id in unit_ids:
            manager.get_unit(unit_id)

    # 执行操作
    print("创建1000个单位...")
    create_batch(1000)

    print("查询所有单位...")
    unit_ids = list(manager._handles.keys())
    get_batch(unit_ids)

    # 显示报告
    print("\n性能报告:")
    monitor = get_global_monitor()
    report = monitor.get_report()

    for operation, stats in report.items():
        print(f"\n操作: {operation}")
        print(f"  调用次数: {stats['count']}")
        print(f"  平均耗时: {stats['avg']*1000:.3f} ms")
        print(f"  总耗时: {stats['total']*1000:.3f} ms")
    print()


if __name__ == "__main__":
    print("\n")
    print("*" * 50)
    print("JASS Runner 状态管理系统演示")
    print("*" * 50)
    print("\n")

    demo_basic_operations()
    demo_multi_player()
    demo_state_context()
    demo_memory_tracking()
    demo_performance_monitoring()

    print("=" * 50)
    print("演示完成!")
    print("=" * 50)
