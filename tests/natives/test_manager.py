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
