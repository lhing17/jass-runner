"""状态管理系统阶段1集成测试。"""


def test_handle_lifecycle_integration():
    """测试handle完整生命周期集成。"""
    from jass_runner.natives.manager import HandleManager

    manager = HandleManager()

    # 创建单位
    unit = manager.create_unit("hfoo", 0, 100.0, 200.0, 270.0)

    # 验证单位创建
    assert unit.unit_type == "hfoo"
    assert unit.player_id == 0
    assert unit.x == 100.0
    assert unit.y == 200.0
    assert unit.facing == 270.0
    assert unit.life == 100.0
    assert unit.is_alive() is True

    # 验证状态查询
    assert manager.get_unit_state(unit.id, "UNIT_STATE_LIFE") == 100.0
    assert manager.get_unit_state(unit.id, "UNIT_STATE_MANA") == 50.0

    # 修改状态
    assert manager.set_unit_state(unit.id, "UNIT_STATE_LIFE", 75.0) is True
    assert manager.get_unit_state(unit.id, "UNIT_STATE_LIFE") == 75.0

    # 销毁单位
    assert manager.destroy_handle(unit.id) is True
    assert unit.is_alive() is False
    assert unit.life == 0

    # 验证销毁后查询
    assert manager.get_unit(unit.id) is None
    assert manager.get_unit_state(unit.id, "UNIT_STATE_LIFE") == 0.0

    # 验证统计（包含16个初始玩家）
    assert manager.get_total_handles() == 17  # 16玩家 + 1单位
    assert manager.get_alive_handles() == 16  # 16玩家存活，单位已销毁
    assert manager.get_handle_type_count("unit") == 1


def test_multiple_units_integration():
    """测试多个单位的集成。"""
    from jass_runner.natives.manager import HandleManager

    manager = HandleManager()

    # 创建多个单位
    units = []
    for i in range(3):
        unit = manager.create_unit(f"unit_type_{i}", i, i * 100.0, i * 100.0, i * 90.0)
        units.append(unit)

    # 验证所有单位
    for i, unit in enumerate(units):
        assert unit.unit_type == f"unit_type_{i}"
        assert unit.player_id == i
        assert unit.x == i * 100.0
        assert unit.y == i * 100.0
        assert unit.facing == i * 90.0

    # 验证统计（包含16个初始玩家）
    assert manager.get_total_handles() == 19  # 16玩家 + 3单位
    assert manager.get_alive_handles() == 19
    assert manager.get_handle_type_count("unit") == 3
    assert manager.get_handle_type_count("player") == 16

    # 销毁部分单位
    assert manager.destroy_handle(units[0].id) is True
    assert manager.destroy_handle(units[1].id) is True

    # 验证统计更新
    assert manager.get_total_handles() == 19  # 总数不变
    assert manager.get_alive_handles() == 17  # 16玩家 + 1存活单位
    assert manager.get_handle_type_count("unit") == 3  # 类型计数不变
