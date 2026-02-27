"""基础原生函数测试。"""

import pytest
from jass_runner.natives.basic import (
    DisplayTextToPlayer, KillUnit, CreateUnit, GetUnitState,
    UNIT_STATE_LIFE, UNIT_STATE_MANA
)
from jass_runner.natives.state import StateContext
from jass_runner.utils import fourcc_to_int


@pytest.fixture
def state_context():
    """提供测试用的StateContext实例。"""
    return StateContext()


def test_display_text_to_player(state_context):
    """测试DisplayTextToPlayer原生函数。"""
    native = DisplayTextToPlayer()
    assert native.name == "DisplayTextToPlayer"

    # 测试执行
    result = native.execute(state_context, 0, 0.0, 0.0, "Hello World")
    assert result is None


def test_kill_unit(state_context):
    """测试KillUnit原生函数。"""
    native = KillUnit()
    assert native.name == "KillUnit"

    # 先创建一个单位
    unit_id = state_context.handle_manager.create_unit("hfoo", 0, 0.0, 0.0, 0.0)

    # 测试击杀存在的单位
    result = native.execute(state_context, unit_id)
    assert result is True

    # 验证单位已被销毁
    unit = state_context.handle_manager.get_unit(unit_id)
    assert unit is None or not unit.is_alive()

    # 测试击杀不存在的单位
    result = native.execute(state_context, "non_existent_unit")
    assert result is False

    # 测试使用None单位
    result = native.execute(state_context, None)
    assert result is False


def test_create_unit(state_context):
    """测试CreateUnit原生函数。"""
    native = CreateUnit()
    assert native.name == "CreateUnit"

    # 使用fourcc整数创建单位（'hfoo' = 1213484355）
    unit_type_int = fourcc_to_int("hfoo")
    result = native.execute(state_context, 0, unit_type_int, 100.0, 200.0, 90.0)

    assert isinstance(result, str)
    assert result.startswith("unit_")

    # 验证单位确实被创建
    unit = state_context.handle_manager.get_unit(result)
    assert unit is not None
    assert unit.unit_type == "hfoo"
    assert unit.player_id == 0
    assert unit.x == 100.0
    assert unit.y == 200.0
    assert unit.facing == 90.0


def test_get_unit_state(state_context):
    """测试GetUnitState原生函数。"""
    native = GetUnitState()
    assert native.name == "GetUnitState"

    # 先创建一个单位
    unit_id = state_context.handle_manager.create_unit("hfoo", 0, 0.0, 0.0, 0.0)

    # 测试获取生命值
    result = native.execute(state_context, unit_id, UNIT_STATE_LIFE)
    assert isinstance(result, float)
    assert result > 0.0

    # 测试获取魔法值
    result = native.execute(state_context, unit_id, UNIT_STATE_MANA)
    assert isinstance(result, float)

    # 测试获取不存在单位的状态
    result = native.execute(state_context, "non_existent_unit", UNIT_STATE_LIFE)
    assert result == 0.0

    # 测试未知状态类型
    result = native.execute(state_context, unit_id, 999)
    assert result == 0.0


def test_unit_lifecycle_integration(state_context):
    """测试单位完整生命周期集成。"""
    create_native = CreateUnit()
    get_state_native = GetUnitState()
    kill_native = KillUnit()

    # 创建单位
    unit_type_int = fourcc_to_int("hkni")  # 骑士
    unit_id = create_native.execute(state_context, 1, unit_type_int, 50.0, 75.0, 180.0)

    # 验证单位存在
    assert state_context.handle_manager.get_unit(unit_id) is not None

    # 获取初始生命值
    initial_life = get_state_native.execute(state_context, unit_id, UNIT_STATE_LIFE)
    assert initial_life > 0.0

    # 击杀单位
    kill_result = kill_native.execute(state_context, unit_id)
    assert kill_result is True

    # 验证单位已被销毁
    assert state_context.handle_manager.get_unit(unit_id) is None

    # 再次获取状态应返回0
    life_after_kill = get_state_native.execute(state_context, unit_id, UNIT_STATE_LIFE)
    assert life_after_kill == 0.0
