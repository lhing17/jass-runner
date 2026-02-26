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
