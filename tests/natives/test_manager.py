"""HandleManager测试。"""


def test_handle_manager_creation():
    """测试HandleManager创建和基本属性。"""
    from jass_runner.natives.manager import HandleManager

    manager = HandleManager()
    assert manager._handles == {}
    assert manager._type_index == {}
    assert manager._next_id == 1


def test_handle_manager_create_unit():
    """测试HandleManager创建单位功能。"""
    from jass_runner.natives.manager import HandleManager

    manager = HandleManager()

    # 创建单位
    unit_id = manager.create_unit("hfoo", 0, 100.0, 200.0, 270.0)

    # 验证返回的ID格式
    assert isinstance(unit_id, str)
    assert unit_id.startswith("unit_")

    # 验证单位已注册
    unit = manager.get_unit(unit_id)
    assert unit is not None
    assert unit.id == unit_id
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
    unit_id = manager.create_unit("hfoo", 0, 0.0, 0.0, 0.0)

    # 测试获取handle
    handle = manager.get_handle(unit_id)
    assert handle is not None
    assert handle.id == unit_id

    # 测试获取不存在的handle
    assert manager.get_handle("nonexistent") is None


def test_handle_manager_destroy_handle():
    """测试HandleManager销毁handle功能。"""
    from jass_runner.natives.manager import HandleManager

    manager = HandleManager()

    # 创建单位
    unit_id = manager.create_unit("hfoo", 0, 0.0, 0.0, 0.0)

    # 验证单位存活
    unit = manager.get_unit(unit_id)
    assert unit is not None
    assert unit.is_alive() is True

    # 销毁单位
    result = manager.destroy_handle(unit_id)
    assert result is True

    # 验证单位已销毁
    unit = manager.get_unit(unit_id)
    assert unit is None  # 已销毁的单位不应返回

    # 测试销毁不存在的handle
    result = manager.destroy_handle("nonexistent")
    assert result is False


def test_handle_manager_type_index():
    """测试HandleManager类型索引功能。"""
    from jass_runner.natives.manager import HandleManager

    manager = HandleManager()

    # 创建多个单位
    unit_id1 = manager.create_unit("hfoo", 0, 0.0, 0.0, 0.0)
    unit_id2 = manager.create_unit("hkni", 1, 100.0, 100.0, 90.0)

    # 验证类型索引
    assert "unit" in manager._type_index
    assert unit_id1 in manager._type_index["unit"]
    assert unit_id2 in manager._type_index["unit"]
    assert len(manager._type_index["unit"]) == 2


def test_handle_manager_get_unit_state():
    """测试HandleManager获取单位状态功能。"""
    from jass_runner.natives.manager import HandleManager

    manager = HandleManager()

    # 创建单位
    unit_id = manager.create_unit("hfoo", 0, 0.0, 0.0, 0.0)

    # 测试获取生命值
    life = manager.get_unit_state(unit_id, "UNIT_STATE_LIFE")
    assert life == 100.0

    # 测试获取魔法值
    mana = manager.get_unit_state(unit_id, "UNIT_STATE_MANA")
    assert mana == 50.0

    # 测试获取最大生命值
    max_life = manager.get_unit_state(unit_id, "UNIT_STATE_MAX_LIFE")
    assert max_life == 100.0

    # 测试获取最大魔法值
    max_mana = manager.get_unit_state(unit_id, "UNIT_STATE_MAX_MANA")
    assert max_mana == 50.0

    # 测试未知状态类型
    unknown = manager.get_unit_state(unit_id, "UNKNOWN_STATE")
    assert unknown == 0.0

    # 测试不存在的单位
    nonexistent = manager.get_unit_state("nonexistent", "UNIT_STATE_LIFE")
    assert nonexistent == 0.0

    # 测试已销毁的单位
    manager.destroy_handle(unit_id)
    destroyed = manager.get_unit_state(unit_id, "UNIT_STATE_LIFE")
    assert destroyed == 0.0
