"""Handle基类测试。"""


def test_handle_base_class():
    """测试Handle基类的创建和基本属性。"""
    from jass_runner.natives.handle import Handle

    # 创建Handle实例
    handle = Handle("test_001", "test_type")

    # 验证基本属性
    assert handle.id == "test_001"
    assert handle.type_name == "test_type"
    assert handle.alive is True
    assert handle.is_alive() is True


def test_handle_destroy():
    """测试Handle销毁功能。"""
    from jass_runner.natives.handle import Handle

    handle = Handle("test_002", "test_type")
    assert handle.is_alive() is True

    # 销毁handle
    handle.destroy()
    assert handle.alive is False
    assert handle.is_alive() is False


def test_unit_class():
    """测试Unit类的创建和属性。"""
    from jass_runner.natives.handle import Handle, Unit

    # 创建Unit实例
    unit = Unit("unit_001", "hfoo", 0, 100.0, 200.0, 270.0)

    # 验证继承自Handle
    assert isinstance(unit, Handle)
    assert unit.id == "unit_001"
    assert unit.type_name == "unit"
    assert unit.alive is True

    # 验证Unit特有属性
    assert unit.unit_type == "hfoo"
    assert unit.player_id == 0
    assert unit.x == 100.0
    assert unit.y == 200.0
    assert unit.facing == 270.0
    assert unit.life == 100.0
    assert unit.max_life == 100.0
    assert unit.mana == 50.0
    assert unit.max_mana == 50.0


def test_unit_destroy():
    """测试Unit销毁功能。"""
    from jass_runner.natives.handle import Unit

    unit = Unit("unit_002", "hfoo", 0, 0.0, 0.0, 0.0)
    assert unit.is_alive() is True
    assert unit.life == 100.0

    # 销毁unit
    unit.destroy()
    assert unit.alive is False
    assert unit.is_alive() is False
    assert unit.life == 0  # 生命值应设为0


def test_player_class():
    """测试Player类的创建和属性。"""
    from jass_runner.natives.handle import Handle, Player

    # 创建Player实例
    player = Player("player_0", 0)

    # 验证继承自Handle
    assert isinstance(player, Handle)
    assert player.id == "player_0"
    assert player.type_name == "player"
    assert player.alive is True

    # 验证Player特有属性
    assert player.player_id == 0
    assert player.name == "玩家0"
    assert player.race == "human"
    assert player.color == 0
    assert player.slot_state == "player"
    assert player.controller == "user"


def test_player_default_values():
    """测试Player默认值的差异化。"""
    from jass_runner.natives.handle import Player

    # 测试玩家8-11（电脑）
    for i in range(8, 12):
        player = Player(f"player_{i}", i)
        assert player.controller == "computer"
        assert player.slot_state == "player"

    # 测试玩家12-15（中立/空）
    for i in range(12, 16):
        player = Player(f"player_{i}", i)
        assert player.controller == "neutral"
        assert player.slot_state == "empty"


def test_item_class():
    """测试Item类的创建和属性。"""
    from jass_runner.natives.handle import Handle, Item

    # 创建Item实例
    item = Item("item_001", "ratf", 100.0, 200.0)

    # 验证继承自Handle
    assert isinstance(item, Handle)
    assert item.id == "item_001"
    assert item.type_name == "item"
    assert item.alive is True

    # 验证Item特有属性
    assert item.item_type == "ratf"
    assert item.x == 100.0
    assert item.y == 200.0


def test_item_destroy():
    """测试Item销毁功能。"""
    from jass_runner.natives.handle import Item

    item = Item("item_002", "ratf", 50.0, 75.0)
    assert item.is_alive() is True

    # 销毁item
    item.destroy()
    assert item.alive is False
    assert item.is_alive() is False


def test_unit_has_z_coordinate():
    """测试 Unit 对象有 z 坐标属性。"""
    from jass_runner.natives.handle import Unit

    unit = Unit("unit_001", "hfoo", 0, 100.0, 200.0, 0.0)
    assert hasattr(unit, 'z')
    assert unit.z == 0.0  # 默认 z 为 0


def test_unit_with_custom_z():
    """测试可以设置 Unit 的 z 坐标。"""
    from jass_runner.natives.handle import Unit

    unit = Unit("unit_001", "hfoo", 0, 100.0, 200.0, 0.0)
    unit.z = 50.0
    assert unit.z == 50.0
