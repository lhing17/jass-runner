"""状态管理系统性能测试。"""

import time
import random
import pytest
from jass_runner.natives.state import StateContext
from jass_runner.natives.manager import HandleManager


def test_handle_creation_performance():
    """测试handle创建性能。"""
    state_context = StateContext()
    handle_manager = state_context.handle_manager

    # 预热
    for i in range(10):
        handle_manager.create_unit("hfoo", 0, 0.0, 0.0, 0.0)

    # 性能测试
    num_units = 1000
    start_time = time.time()

    for i in range(num_units):
        handle_manager.create_unit("hfoo", i % 12, float(i), float(i * 2), float(i % 360))

    end_time = time.time()
    elapsed = end_time - start_time

    # 验证性能要求：1000个单位的创建应在1秒内完成
    assert elapsed < 1.0, f"创建{num_units}个单位耗时{elapsed:.3f}秒，超过1秒限制"

    # 验证所有单位都已创建
    assert handle_manager.get_total_handles() >= num_units


def test_handle_lookup_performance():
    """测试handle查询性能。"""
    state_context = StateContext()
    handle_manager = state_context.handle_manager

    # 创建测试数据
    unit_ids = []
    num_units = 1000
    for i in range(num_units):
        unit = handle_manager.create_unit("hfoo", 0, 0.0, 0.0, 0.0)
        unit_ids.append(unit.id)

    # 预热
    for unit_id in unit_ids[:10]:
        handle_manager.get_unit(unit_id)

    # 性能测试：随机查询
    start_time = time.time()

    num_lookups = 10000
    for _ in range(num_lookups):
        random_unit_id = random.choice(unit_ids)
        unit = handle_manager.get_unit(random_unit_id)
        assert unit is not None

    end_time = time.time()
    elapsed = end_time - start_time

    # 验证性能要求：10000次查询应在0.5秒内完成
    assert elapsed < 0.5, f"{num_lookups}次查询耗时{elapsed:.3f}秒，超过0.5秒限制"


def test_handle_state_operations_performance():
    """测试状态操作性能。"""
    state_context = StateContext()
    handle_manager = state_context.handle_manager

    # 创建单位
    unit = handle_manager.create_unit("hfoo", 0, 0.0, 0.0, 0.0)
    unit_id = unit.id

    # 测试get_unit_state性能
    num_ops = 10000
    start_time = time.time()

    for _ in range(num_ops):
        handle_manager.get_unit_state(unit_id, "UNIT_STATE_LIFE")

    elapsed = time.time() - start_time
    assert elapsed < 0.5, f"{num_ops}次get_unit_state耗时{elapsed:.3f}秒"

    # 测试set_unit_state性能
    start_time = time.time()

    for i in range(num_ops):
        handle_manager.set_unit_state(unit_id, "UNIT_STATE_LIFE", float(i % 100))

    elapsed = time.time() - start_time
    assert elapsed < 0.5, f"{num_ops}次set_unit_state耗时{elapsed:.3f}秒"


def test_handle_lifecycle_performance():
    """测试完整生命周期性能。"""
    state_context = StateContext()
    handle_manager = state_context.handle_manager

    num_units = 1000

    # 创建
    start_time = time.time()
    unit_ids = []
    for i in range(num_units):
        unit = handle_manager.create_unit("hfoo", 0, float(i), float(i), 0.0)
        unit_ids.append(unit.id)
    create_time = time.time() - start_time

    # 查询
    start_time = time.time()
    for unit_id in unit_ids:
        handle_manager.get_unit(unit_id)
    lookup_time = time.time() - start_time

    # 销毁
    start_time = time.time()
    for unit_id in unit_ids:
        handle_manager.destroy_handle(unit_id)
    destroy_time = time.time() - start_time

    # 验证性能要求
    assert create_time < 1.0, f"创建{num_units}个单位耗时{create_time:.3f}秒"
    assert lookup_time < 0.5, f"查询{num_units}个单位耗时{lookup_time:.3f}秒"
    assert destroy_time < 0.5, f"销毁{num_units}个单位耗时{destroy_time:.3f}秒"
