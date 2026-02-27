"""HandleManager测试。"""


def test_handle_manager_creation():
    """测试HandleManager创建和基本属性。"""
    from jass_runner.natives.manager import HandleManager

    manager = HandleManager()
    # 初始化时创建16个玩家
    assert len(manager._handles) == 16
    assert "player" in manager._type_index
    assert manager._next_id == 1


def test_handle_manager_create_unit():
    """测试HandleManager创建单位功能。"""
    from jass_runner.natives.manager import HandleManager
    from jass_runner.natives.handle import Unit

    manager = HandleManager()

    # 创建单位
    unit = manager.create_unit("hfoo", 0, 100.0, 200.0, 270.0)

    # 验证返回的是Unit对象
    assert isinstance(unit, Unit)
    assert unit.id.startswith("unit_")

    # 验证单位已注册
    retrieved_unit = manager.get_unit(unit.id)
    assert retrieved_unit is unit
    assert unit.unit_type == "hfoo"
    assert unit.player_id == 0
    assert unit.x == 100.0
    assert unit.y == 200.0
    assert unit.facing == 270.0


def test_handle_manager_get_handle():
    """测试HandleManager获取handle功能。"""
    from jass_runner.natives.manager import HandleManager

    manager = HandleManager()

    # 创建单位
    unit = manager.create_unit("hfoo", 0, 0.0, 0.0, 0.0)

    # 测试获取handle
    handle = manager.get_handle(unit.id)
    assert handle is not None
    assert handle.id == unit.id

    # 测试获取不存在的handle
    assert manager.get_handle("nonexistent") is None


def test_handle_manager_destroy_handle():
    """测试HandleManager销毁handle功能。"""
    from jass_runner.natives.manager import HandleManager

    manager = HandleManager()

    # 创建单位
    unit = manager.create_unit("hfoo", 0, 0.0, 0.0, 0.0)

    # 验证单位存活
    assert unit.is_alive() is True

    # 销毁单位
    result = manager.destroy_handle(unit.id)
    assert result is True

    # 验证单位已销毁
    retrieved_unit = manager.get_unit(unit.id)
    assert retrieved_unit is None  # 已销毁的单位不应返回

    # 测试销毁不存在的handle
    result = manager.destroy_handle("nonexistent")
    assert result is False


def test_handle_manager_type_index():
    """测试HandleManager类型索引功能。"""
    from jass_runner.natives.manager import HandleManager

    manager = HandleManager()

    # 创建多个单位
    unit1 = manager.create_unit("hfoo", 0, 0.0, 0.0, 0.0)
    unit2 = manager.create_unit("hkni", 1, 100.0, 100.0, 90.0)

    # 验证类型索引（类型索引中存储的是ID字符串）
    assert "unit" in manager._type_index
    assert unit1.id in manager._type_index["unit"]
    assert unit2.id in manager._type_index["unit"]
    assert len(manager._type_index["unit"]) == 2


def test_handle_manager_get_unit_state():
    """测试HandleManager获取单位状态功能。"""
    from jass_runner.natives.manager import HandleManager

    manager = HandleManager()

    # 创建单位
    unit = manager.create_unit("hfoo", 0, 0.0, 0.0, 0.0)

    # 测试获取生命值
    life = manager.get_unit_state(unit.id, "UNIT_STATE_LIFE")
    assert life == 100.0

    # 测试获取魔法值
    mana = manager.get_unit_state(unit.id, "UNIT_STATE_MANA")
    assert mana == 50.0

    # 测试获取最大生命值
    max_life = manager.get_unit_state(unit.id, "UNIT_STATE_MAX_LIFE")
    assert max_life == 100.0

    # 测试获取最大魔法值
    max_mana = manager.get_unit_state(unit.id, "UNIT_STATE_MAX_MANA")
    assert max_mana == 50.0

    # 测试未知状态类型
    unknown = manager.get_unit_state(unit.id, "UNKNOWN_STATE")
    assert unknown == 0.0

    # 测试不存在的单位
    nonexistent = manager.get_unit_state("nonexistent", "UNIT_STATE_LIFE")
    assert nonexistent == 0.0

    # 测试已销毁的单位
    manager.destroy_handle(unit.id)
    destroyed = manager.get_unit_state(unit.id, "UNIT_STATE_LIFE")
    assert destroyed == 0.0


def test_handle_manager_set_unit_state():
    """测试HandleManager设置单位状态功能。"""
    from jass_runner.natives.manager import HandleManager

    manager = HandleManager()

    # 创建单位
    unit = manager.create_unit("hfoo", 0, 0.0, 0.0, 0.0)

    # 测试设置生命值
    result = manager.set_unit_state(unit.id, "UNIT_STATE_LIFE", 75.0)
    assert result is True
    assert manager.get_unit_state(unit.id, "UNIT_STATE_LIFE") == 75.0

    # 测试设置魔法值
    result = manager.set_unit_state(unit.id, "UNIT_STATE_MANA", 30.0)
    assert result is True
    assert manager.get_unit_state(unit.id, "UNIT_STATE_MANA") == 30.0

    # 测试设置最大生命值
    result = manager.set_unit_state(unit.id, "UNIT_STATE_MAX_LIFE", 150.0)
    assert result is True
    assert manager.get_unit_state(unit.id, "UNIT_STATE_MAX_LIFE") == 150.0

    # 测试设置最大魔法值
    result = manager.set_unit_state(unit.id, "UNIT_STATE_MAX_MANA", 75.0)
    assert result is True
    assert manager.get_unit_state(unit.id, "UNIT_STATE_MAX_MANA") == 75.0

    # 测试未知状态类型
    result = manager.set_unit_state(unit.id, "UNKNOWN_STATE", 100.0)
    assert result is False

    # 测试不存在的单位
    result = manager.set_unit_state("nonexistent", "UNIT_STATE_LIFE", 100.0)
    assert result is False

    # 测试已销毁的单位
    manager.destroy_handle(unit.id)
    result = manager.set_unit_state(unit.id, "UNIT_STATE_LIFE", 100.0)
    assert result is False


def test_handle_manager_statistics():
    """测试HandleManager统计功能。"""
    from jass_runner.natives.manager import HandleManager

    manager = HandleManager()

    # 初始状态（包含16个玩家）
    assert manager.get_total_handles() == 16
    assert manager.get_alive_handles() == 16
    assert manager.get_handle_type_count("unit") == 0
    assert manager.get_handle_type_count("player") == 16

    # 创建单位
    unit1 = manager.create_unit("hfoo", 0, 0.0, 0.0, 0.0)
    unit2 = manager.create_unit("hkni", 1, 100.0, 100.0, 90.0)

    # 验证统计
    assert manager.get_total_handles() == 18
    assert manager.get_alive_handles() == 18
    assert manager.get_handle_type_count("unit") == 2
    assert manager.get_handle_type_count("player") == 16

    # 销毁一个单位
    manager.destroy_handle(unit1.id)

    # 验证统计更新
    assert manager.get_total_handles() == 18  # 总数不变
    assert manager.get_alive_handles() == 17  # 存活数减少
    assert manager.get_handle_type_count("unit") == 2  # 类型计数不变

    # 测试不存在的类型
    assert manager.get_handle_type_count("nonexistent") == 0


def test_handle_manager_initializes_players():
    """测试HandleManager初始化时创建16个玩家。"""
    from jass_runner.natives.manager import HandleManager
    from jass_runner.natives.handle import Player

    manager = HandleManager()

    # 验证16个玩家已创建
    assert manager.get_handle_type_count("player") == 16
    assert manager.get_alive_handles() == 16

    # 验证可以通过ID获取玩家
    for i in range(16):
        player = manager.get_player(i)
        assert player is not None
        assert isinstance(player, Player)
        assert player.player_id == i
        assert player.id == f"player_{i}"


def test_handle_manager_get_player_invalid_id():
    """测试获取无效玩家ID。"""
    from jass_runner.natives.manager import HandleManager

    manager = HandleManager()

    # 测试无效ID
    assert manager.get_player(-1) is None
    assert manager.get_player(16) is None
    assert manager.get_player(100) is None


def test_handle_manager_get_player_by_handle():
    """测试通过handle ID获取玩家。"""
    from jass_runner.natives.manager import HandleManager
    from jass_runner.natives.handle import Player

    manager = HandleManager()

    # 测试获取存在的玩家
    player = manager.get_player_by_handle("player_0")
    assert player is not None
    assert isinstance(player, Player)
    assert player.player_id == 0

    # 测试获取不存在的玩家
    assert manager.get_player_by_handle("player_999") is None
    assert manager.get_player_by_handle("unit_1") is None


def test_handle_manager_create_item():
    """测试HandleManager创建物品功能。"""
    from jass_runner.natives.manager import HandleManager
    from jass_runner.natives.handle import Item

    manager = HandleManager()

    # 创建物品
    item = manager.create_item("ratf", 100.0, 200.0)

    # 验证返回的是Item对象
    assert isinstance(item, Item)
    assert item.id.startswith("item_")

    # 验证物品已注册
    retrieved_item = manager.get_item(item.id)
    assert retrieved_item is item
    assert item.item_type == "ratf"
    assert item.x == 100.0
    assert item.y == 200.0


def test_handle_manager_get_item():
    """测试HandleManager获取物品功能。"""
    from jass_runner.natives.manager import HandleManager

    manager = HandleManager()

    # 创建物品
    item = manager.create_item("ratf", 100.0, 200.0)

    # 测试获取物品
    retrieved = manager.get_item(item.id)
    assert retrieved is item

    # 测试获取不存在的物品
    assert manager.get_item("nonexistent") is None

    # 测试获取已销毁的物品
    manager.destroy_handle(item.id)
    assert manager.get_item(item.id) is None


def test_handle_manager_item_type_index():
    """测试HandleManager物品类型索引功能。"""
    from jass_runner.natives.manager import HandleManager

    manager = HandleManager()

    # 创建多个物品
    item1 = manager.create_item("ratf", 0.0, 0.0)
    item2 = manager.create_item("manh", 100.0, 100.0)

    # 验证类型索引
    assert "item" in manager._type_index
    assert item1.id in manager._type_index["item"]
    assert item2.id in manager._type_index["item"]
    assert len(manager._type_index["item"]) == 2


def test_handle_manager_mixed_handles():
    """测试HandleManager混合管理不同类型的handle。"""
    from jass_runner.natives.manager import HandleManager
    from jass_runner.natives.handle import Unit, Item

    manager = HandleManager()

    # 创建单位和物品
    unit = manager.create_unit("hfoo", 0, 0.0, 0.0, 0.0)
    item = manager.create_item("ratf", 100.0, 100.0)

    # 验证总数（16个玩家 + 1个单位 + 1个物品）
    assert manager.get_total_handles() == 18
    assert manager.get_alive_handles() == 18

    # 验证类型计数
    assert manager.get_handle_type_count("player") == 16
    assert manager.get_handle_type_count("unit") == 1
    assert manager.get_handle_type_count("item") == 1

    # 验证可以通过各自的方法获取
    assert manager.get_unit(unit.id) is unit
    assert manager.get_item(item.id) is item

    # 验证通过通用get_handle也能获取
    assert manager.get_handle(unit.id) is unit
    assert manager.get_handle(item.id) is item
