"""基础原生函数测试。"""

import pytest
from jass_runner.natives.basic import (
    DisplayTextToPlayer, KillUnit, CreateUnit, GetUnitState, PlayerNative,
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
    from jass_runner.natives.handle import Player

    native = DisplayTextToPlayer()
    assert native.name == "DisplayTextToPlayer"

    # 获取Player对象
    player = state_context.handle_manager.get_player(0)

    # 测试执行
    result = native.execute(state_context, player, 0.0, 0.0, "Hello World")
    assert result is None


def test_player_native(state_context):
    """测试Player原生函数。"""
    from jass_runner.natives.handle import Player

    native = PlayerNative()
    assert native.name == "Player"

    # 测试获取玩家0
    result = native.execute(state_context, 0)
    assert isinstance(result, Player)
    assert result.player_id == 0

    # 测试获取玩家15
    result = native.execute(state_context, 15)
    assert isinstance(result, Player)
    assert result.player_id == 15


def test_kill_unit(state_context):
    """测试KillUnit原生函数。"""
    from jass_runner.natives.handle import Unit

    native = KillUnit()
    assert native.name == "KillUnit"

    # 先创建一个单位
    unit = state_context.handle_manager.create_unit("hfoo", 0, 0.0, 0.0, 0.0)

    # 测试击杀存在的单位
    result = native.execute(state_context, unit)
    assert result is True

    # 验证单位已被销毁
    retrieved_unit = state_context.handle_manager.get_unit(unit.id)
    assert retrieved_unit is None or not retrieved_unit.is_alive()

    # 测试使用None单位
    result = native.execute(state_context, None)
    assert result is False


def test_create_unit(state_context):
    """测试CreateUnit原生函数。"""
    from jass_runner.natives.handle import Unit

    native = CreateUnit()
    assert native.name == "CreateUnit"

    # 使用fourcc整数创建单位（'hfoo' = 1213484355）
    unit_type_int = fourcc_to_int("hfoo")
    result = native.execute(state_context, 0, unit_type_int, 100.0, 200.0, 90.0)

    # 验证返回的是Unit对象
    assert isinstance(result, Unit)
    assert result.id.startswith("unit_")
    assert result.unit_type == "hfoo"
    assert result.player_id == 0
    assert result.x == 100.0
    assert result.y == 200.0
    assert result.facing == 90.0

    # 验证可以通过handle manager获取
    retrieved_unit = state_context.handle_manager.get_unit(result.id)
    assert retrieved_unit is result


def test_get_unit_state(state_context):
    """测试GetUnitState原生函数。"""
    native = GetUnitState()
    assert native.name == "GetUnitState"

    # 先创建一个单位
    unit = state_context.handle_manager.create_unit("hfoo", 0, 0.0, 0.0, 0.0)

    # 测试获取生命值
    result = native.execute(state_context, unit, UNIT_STATE_LIFE)
    assert isinstance(result, float)
    assert result > 0.0

    # 测试获取魔法值
    result = native.execute(state_context, unit, UNIT_STATE_MANA)
    assert isinstance(result, float)

    # 测试获取None单位的状态
    result = native.execute(state_context, None, UNIT_STATE_LIFE)
    assert result == 0.0

    # 测试未知状态类型
    result = native.execute(state_context, unit, 999)
    assert result == 0.0


def test_unit_lifecycle_integration(state_context):
    """测试单位完整生命周期集成。"""
    from jass_runner.natives.handle import Unit

    create_native = CreateUnit()
    get_state_native = GetUnitState()
    kill_native = KillUnit()

    # 创建单位
    unit_type_int = fourcc_to_int("hkni")  # 骑士
    unit = create_native.execute(state_context, 1, unit_type_int, 50.0, 75.0, 180.0)

    # 验证返回的是Unit对象
    assert isinstance(unit, Unit)

    # 验证单位存在
    assert state_context.handle_manager.get_unit(unit.id) is not None

    # 获取初始生命值
    initial_life = get_state_native.execute(state_context, unit, UNIT_STATE_LIFE)
    assert initial_life > 0.0

    # 击杀单位
    kill_result = kill_native.execute(state_context, unit)
    assert kill_result is True

    # 验证单位已被销毁
    assert state_context.handle_manager.get_unit(unit.id) is None


def test_create_item(state_context):
    """测试CreateItem原生函数。"""
    from jass_runner.natives.basic import CreateItem
    from jass_runner.natives.handle import Item

    native = CreateItem()
    assert native.name == "CreateItem"

    # 使用fourcc整数创建物品（'ratf' = 攻击之爪）
    item_type_int = fourcc_to_int("ratf")
    result = native.execute(state_context, item_type_int, 100.0, 200.0)

    # 验证返回的是Item对象
    assert isinstance(result, Item)
    assert result.id.startswith("item_")
    assert result.item_type == "ratf"
    assert result.x == 100.0
    assert result.y == 200.0

    # 验证可以通过handle manager获取
    retrieved_item = state_context.handle_manager.get_item(result.id)
    assert retrieved_item is result


def test_remove_item(state_context):
    """测试RemoveItem原生函数。"""
    from jass_runner.natives.basic import CreateItem, RemoveItem
    from jass_runner.natives.handle import Item

    remove_native = RemoveItem()
    assert remove_native.name == "RemoveItem"

    # 先创建一个物品
    item_type_int = fourcc_to_int("ratf")
    item = state_context.handle_manager.create_item("ratf", 100.0, 200.0)

    # 测试移除存在的物品
    result = remove_native.execute(state_context, item)
    assert result is None  # RemoveItem返回nothing

    # 验证物品已被销毁
    retrieved_item = state_context.handle_manager.get_item(item.id)
    assert retrieved_item is None or not retrieved_item.is_alive()

    # 测试使用None物品
    result = remove_native.execute(state_context, None)
    assert result is None


def test_item_lifecycle_integration(state_context):
    """测试物品完整生命周期集成。"""
    from jass_runner.natives.basic import CreateItem, RemoveItem
    from jass_runner.natives.handle import Item

    create_native = CreateItem()
    remove_native = RemoveItem()

    # 创建物品
    item_type_int = fourcc_to_int("ratf")  # 攻击之爪
    item = create_native.execute(state_context, item_type_int, 50.0, 75.0)

    # 验证返回的是Item对象
    assert isinstance(item, Item)

    # 验证物品存在
    assert state_context.handle_manager.get_item(item.id) is not None

    # 移除物品
    remove_native.execute(state_context, item)

    # 验证物品已被销毁
    assert state_context.handle_manager.get_item(item.id) is None
