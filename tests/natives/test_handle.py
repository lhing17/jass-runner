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
