"""状态管理系统集成测试。"""

import os
import pytest
from jass_runner.interpreter.interpreter import Interpreter
from jass_runner.natives.factory import NativeFactory
from jass_runner.natives.basic import CreateUnit, GetUnitState, KillUnit
from jass_runner.parser.parser import Parser


def test_state_management_end_to_end():
    """测试状态管理系统的端到端功能。"""
    # 加载测试脚本
    script_path = os.path.join(os.path.dirname(__file__), "../../examples/state_management_test.j")
    with open(script_path, "r", encoding="utf-8") as f:
        code = f.read()

    # 解析JASS代码
    parser = Parser(code)
    ast = parser.parse()

    # 确保没有解析错误
    assert not parser.errors, f"解析错误: {parser.errors}"

    # 创建解释器
    factory = NativeFactory()
    native_registry = factory.create_default_registry()
    interpreter = Interpreter(native_registry=native_registry)

    # 执行脚本（不应抛出异常）
    interpreter.execute(ast)

    # 验证执行成功 - 检查handle manager中有单位被创建
    handle_manager = interpreter.state_context.handle_manager
    assert handle_manager.get_total_handles() > 0


def test_state_persistence():
    """测试CreateUnit和GetUnitState之间的状态共享。"""
    from jass_runner.interpreter.context import ExecutionContext
    from jass_runner.natives.state import StateContext

    # 创建测试上下文
    state_context = StateContext()
    context = ExecutionContext(native_registry=None, state_context=state_context)

    # 创建CreateUnit函数实例
    create_unit_func = CreateUnit()
    assert create_unit_func.name == "CreateUnit"

    # 创建单位
    unit = create_unit_func.execute(state_context, 0, 1213484355, 100.0, 200.0, 270.0)  # 1213484355 = 'hfoo'
    assert unit is not None
    assert unit.id.startswith("unit_")

    # 创建GetUnitState函数实例
    get_unit_state_func = GetUnitState()
    assert get_unit_state_func.name == "GetUnitState"

    # 查询单位状态
    life = get_unit_state_func.execute(state_context, unit, 0)  # 0 = UNIT_STATE_LIFE
    max_life = get_unit_state_func.execute(state_context, unit, 1)  # 1 = UNIT_STATE_MAX_LIFE

    # 验证状态共享（应该返回相同的值）
    assert life == 100.0
    assert max_life == 100.0

    # 验证单位确实存在于handle manager中
    handle_manager = state_context.handle_manager
    unit_from_manager = handle_manager.get_unit(unit.id)
    assert unit_from_manager is not None
    assert unit_from_manager.life == 100.0
    assert unit_from_manager.max_life == 100.0


def test_handle_lifecycle():
    """测试handle的完整生命周期：创建、查询、销毁。"""
    from jass_runner.interpreter.context import ExecutionContext
    from jass_runner.natives.state import StateContext

    # 创建测试上下文
    state_context = StateContext()
    context = ExecutionContext(native_registry=None, state_context=state_context)
    handle_manager = state_context.handle_manager

    # 创建CreateUnit函数实例
    create_unit_func = CreateUnit()

    # 创建单位
    unit = create_unit_func.execute(state_context, 0, 1213484355, 100.0, 200.0, 270.0)
    unit_id = unit.id

    # 验证单位存在且存活
    unit_from_manager = handle_manager.get_unit(unit_id)
    assert unit_from_manager is not None
    assert unit_from_manager.is_alive() is True
    assert unit_from_manager.life == 100.0

    # 查询状态
    get_unit_state_func = GetUnitState()
    life_before = get_unit_state_func.execute(state_context, unit, 0)
    assert life_before == 100.0

    # 杀死单位
    kill_unit_func = KillUnit()
    kill_result = kill_unit_func.execute(state_context, unit)
    assert kill_result is True

    # 验证单位在HandleManager中被标记为死亡
    # 注意：get_handle和get_unit只返回存活的handle
    dead_unit = handle_manager.get_unit(unit_id)
    assert dead_unit is None  # 已死亡的单位返回None

    # 再次查询状态（应返回0）
    life_after = get_unit_state_func.execute(state_context, unit, 0)
    assert life_after == 0.0

    # 尝试再次杀死（应返回False，因为单位已死亡）
    kill_result_again = kill_unit_func.execute(state_context, unit)
    assert kill_result_again is False


def test_error_handling_scenarios():
    """测试状态管理系统的错误处理。"""
    from jass_runner.interpreter.context import ExecutionContext
    from jass_runner.natives.state import StateContext

    state_context = StateContext()
    context = ExecutionContext(native_registry=None, state_context=state_context)

    # 测试1: 查询不存在的单位
    get_unit_state_func = GetUnitState()
    result = get_unit_state_func.execute(state_context, None, 0)
    assert result == 0.0  # 应返回默认值

    # 测试2: 杀死None单位
    kill_unit_func = KillUnit()
    result = kill_unit_func.execute(state_context, None)
    assert result is False  # 应返回False

    # 测试3: 查询已死亡的单位
    # 先创建并杀死一个单位
    create_unit_func = CreateUnit()
    unit = create_unit_func.execute(state_context, 0, 1213484355, 0.0, 0.0, 0.0)

    # 杀死单位
    kill_result = kill_unit_func.execute(state_context, unit)
    assert kill_result is True

    # 查询已死亡的单位
    life_after_death = get_unit_state_func.execute(state_context, unit, 0)
    assert life_after_death == 0.0

    # 测试4: 使用无效的状态类型
    result = get_unit_state_func.execute(state_context, unit, 999)
    assert result == 0.0  # 应返回默认值


def test_multi_player_scenario():
    """测试多玩家场景下的状态管理。"""
    from jass_runner.interpreter.context import ExecutionContext
    from jass_runner.natives.state import StateContext

    state_context = StateContext()
    context = ExecutionContext(native_registry=None, state_context=state_context)
    handle_manager = state_context.handle_manager

    # 为不同玩家创建单位
    create_unit_func = CreateUnit()
    get_unit_state_func = GetUnitState()

    player_units = {}
    for player_id in range(4):  # 4个玩家
        unit_ids = []
        for i in range(3):  # 每个玩家3个单位
            unit = create_unit_func.execute(
                state_context, player_id, 1213484355,  # 'hfoo'
                float(player_id * 100), float(i * 50), 0.0
            )
            unit_ids.append(unit)
        player_units[player_id] = unit_ids

    # 验证每个玩家的单位
    for player_id, units in player_units.items():
        for unit in units:
            unit_from_manager = handle_manager.get_unit(unit.id)
            assert unit_from_manager is not None
            assert unit_from_manager.player_id == player_id

            # 查询状态
            life = get_unit_state_func.execute(state_context, unit, 0)
            assert life == 100.0

    # 玩家1杀死玩家0的一个单位
    kill_unit_func = KillUnit()
    target_unit = player_units[0][0]  # 玩家0的第一个单位
    kill_result = kill_unit_func.execute(state_context, target_unit)
    assert kill_result is True

    # 验证单位已死亡
    dead_unit = handle_manager.get_unit(target_unit.id)
    assert dead_unit is None

    # 玩家0的单位数量减少
    assert len(player_units[0]) == 3  # ID列表不变
    # 但实际存活单位减少
    alive_count = 0
    for unit in player_units[0]:
        if handle_manager.get_unit(unit.id) is not None:
            alive_count += 1
    assert alive_count == 2
