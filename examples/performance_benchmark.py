"""性能基准测试脚本。

此脚本测试状态管理系统的性能指标。
"""

import sys
import os
import time
import random

# 添加src到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from jass_runner.natives.manager import HandleManager


def benchmark_handle_creation():
    """测试handle创建性能。"""
    print("=" * 50)
    print("性能测试: Handle创建")
    print("=" * 50)

    test_sizes = [100, 1000, 10000]

    for size in test_sizes:
        manager = HandleManager()

        start = time.perf_counter()
        for i in range(size):
            manager.create_unit("hfoo", 0, float(i), float(i), 0.0)
        elapsed = time.perf_counter() - start

        print(f"创建{size}个单位: {elapsed*1000:.2f} ms ({size/elapsed:.0f} 单位/秒)")

    print()


def benchmark_handle_lookup():
    """测试handle查询性能。"""
    print("=" * 50)
    print("性能测试: Handle查询")
    print("=" * 50)

    manager = HandleManager()

    # 创建测试数据
    unit_ids = []
    for i in range(1000):
        unit = manager.create_unit("hfoo", 0, float(i), float(i), 0.0)
        unit_ids.append(unit.id)

    # 测试查询性能
    num_lookups = 10000
    start = time.perf_counter()

    for _ in range(num_lookups):
        random_id = random.choice(unit_ids)
        manager.get_unit(random_id)

    elapsed = time.perf_counter() - start

    print(f"{num_lookups}次随机查询: {elapsed*1000:.2f} ms ({num_lookups/elapsed:.0f} 查询/秒)")
    print()


def benchmark_state_operations():
    """测试状态操作性能。"""
    print("=" * 50)
    print("性能测试: 状态操作")
    print("=" * 50)

    manager = HandleManager()

    # 创建单位
    unit = manager.create_unit("hfoo", 0, 100.0, 200.0, 270.0)

    # 测试get_unit_state
    num_ops = 10000
    start = time.perf_counter()

    for _ in range(num_ops):
        manager.get_unit_state(unit.id, "UNIT_STATE_LIFE")

    elapsed = time.perf_counter() - start
    print(f"{num_ops}次get_unit_state: {elapsed*1000:.2f} ms")

    # 测试set_unit_state
    start = time.perf_counter()

    for i in range(num_ops):
        manager.set_unit_state(unit.id, "UNIT_STATE_LIFE", float(i % 100))

    elapsed = time.perf_counter() - start
    print(f"{num_ops}次set_unit_state: {elapsed*1000:.2f} ms")
    print()


def benchmark_memory_usage():
    """测试内存使用情况。"""
    print("=" * 50)
    print("性能测试: 内存使用")
    print("=" * 50)

    import gc

    test_sizes = [100, 1000, 5000]

    for size in test_sizes:
        gc.collect()  # 强制垃圾回收

        manager = HandleManager()

        # 创建单位
        for i in range(size):
            manager.create_unit("hfoo", 0, float(i), float(i), 0.0)

        # 估算内存使用（简化计算）
        # 每个单位大约占用几百字节
        estimated_bytes = size * 200  # 粗略估计
        estimated_kb = estimated_bytes / 1024

        print(f"{size}个单位估计内存: {estimated_kb:.2f} KB")

    print()


def benchmark_lifecycle():
    """测试完整生命周期性能。"""
    print("=" * 50)
    print("性能测试: 完整生命周期")
    print("=" * 50)

    num_units = 1000
    manager = HandleManager()

    # 创建
    start = time.perf_counter()
    unit_ids = []
    for i in range(num_units):
        unit = manager.create_unit("hfoo", 0, float(i), float(i), 0.0)
        unit_ids.append(unit.id)
    create_time = time.perf_counter() - start

    # 查询
    start = time.perf_counter()
    for unit_id in unit_ids:
        manager.get_unit(unit_id)
    lookup_time = time.perf_counter() - start

    # 销毁
    start = time.perf_counter()
    for unit_id in unit_ids:
        manager.destroy_handle(unit_id)
    destroy_time = time.perf_counter() - start

    print(f"创建{num_units}个单位: {create_time*1000:.2f} ms")
    print(f"查询{num_units}个单位: {lookup_time*1000:.2f} ms")
    print(f"销毁{num_units}个单位: {destroy_time*1000:.2f} ms")
    print(f"总计: {(create_time + lookup_time + destroy_time)*1000:.2f} ms")
    print()


if __name__ == "__main__":
    print("\n")
    print("*" * 50)
    print("JASS Runner 性能基准测试")
    print("*" * 50)
    print("\n")

    benchmark_handle_creation()
    benchmark_handle_lookup()
    benchmark_state_operations()
    benchmark_memory_usage()
    benchmark_lifecycle()

    print("=" * 50)
    print("性能测试完成!")
    print("=" * 50)
