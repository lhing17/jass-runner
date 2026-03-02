"""单位位置 native 函数测试。

此模块包含 SetUnitPosition 和 SetUnitPositionLoc native 函数的测试。
"""

import pytest
from jass_runner.natives.handle import Unit
from jass_runner.natives.location import Location


class TestSetUnitPosition:
    """测试 SetUnitPosition native 函数。"""

    def test_set_unit_position(self):
        """测试 SetUnitPosition native 函数。"""
        from jass_runner.natives.unit_position_natives import SetUnitPosition
        from jass_runner.natives.manager import HandleManager

        manager = HandleManager()
        unit = manager.create_unit("hfoo", 0, 100.0, 200.0, 0.0)

        set_unit_position = SetUnitPosition()

        class MockStateContext:
            def __init__(self):
                self.handle_manager = manager

        set_unit_position.execute(MockStateContext(), unit, 300.0, 400.0)

        assert unit.x == 300.0
        assert unit.y == 400.0

    def test_set_unit_position_with_none_unit(self):
        """测试 SetUnitPosition 处理 None 单位。"""
        from jass_runner.natives.unit_position_natives import SetUnitPosition

        set_unit_position = SetUnitPosition()

        class MockStateContext:
            pass

        # 应该不抛出异常
        set_unit_position.execute(MockStateContext(), None, 300.0, 400.0)


class TestSetUnitPositionLoc:
    """测试 SetUnitPositionLoc native 函数。"""

    def test_set_unit_position_loc(self):
        """测试 SetUnitPositionLoc native 函数。"""
        from jass_runner.natives.unit_position_natives import SetUnitPositionLoc
        from jass_runner.natives.manager import HandleManager

        manager = HandleManager()
        unit = manager.create_unit("hfoo", 0, 100.0, 200.0, 0.0)

        set_unit_position_loc = SetUnitPositionLoc()
        loc = Location(500.0, 600.0, 50.0)

        class MockStateContext:
            def __init__(self):
                self.handle_manager = manager

        set_unit_position_loc.execute(MockStateContext(), unit, loc)

        assert unit.x == 500.0
        assert unit.y == 600.0
        assert unit.z == 50.0

    def test_set_unit_position_loc_with_none_unit(self):
        """测试 SetUnitPositionLoc 处理 None 单位。"""
        from jass_runner.natives.unit_position_natives import SetUnitPositionLoc
        from jass_runner.natives.location import Location

        set_unit_position_loc = SetUnitPositionLoc()
        loc = Location(500.0, 600.0)

        class MockStateContext:
            pass

        # 应该不抛出异常
        set_unit_position_loc.execute(MockStateContext(), None, loc)

    def test_set_unit_position_loc_with_none_location(self):
        """测试 SetUnitPositionLoc 处理 None Location。"""
        from jass_runner.natives.unit_position_natives import SetUnitPositionLoc
        from jass_runner.natives.manager import HandleManager

        manager = HandleManager()
        unit = manager.create_unit("hfoo", 0, 100.0, 200.0, 0.0)

        set_unit_position_loc = SetUnitPositionLoc()

        class MockStateContext:
            def __init__(self):
                self.handle_manager = manager

        # 应该不抛出异常
        set_unit_position_loc.execute(MockStateContext(), unit, None)

        # 单位位置不应改变
        assert unit.x == 100.0
        assert unit.y == 200.0


class TestCreateUnitAtLoc:
    """测试 CreateUnitAtLoc native 函数。"""

    def test_create_unit_at_loc(self):
        """测试 CreateUnitAtLoc native 函数。"""
        from jass_runner.natives.unit_position_natives import CreateUnitAtLoc
        from jass_runner.natives.location import Location
        from jass_runner.natives.manager import HandleManager

        manager = HandleManager()

        create_unit_at_loc = CreateUnitAtLoc()
        loc = Location(300.0, 400.0, 25.0)

        class MockStateContext:
            def __init__(self):
                self.handle_manager = manager

        # 创建单位（unit_type 使用 fourcc 整数）
        unit = create_unit_at_loc.execute(MockStateContext(), 0, 1213484355, loc, 90.0)

        assert unit is not None
        assert unit.x == 300.0
        assert unit.y == 400.0
        assert unit.z == 25.0
        assert unit.facing == 90.0

    def test_create_unit_at_loc_with_none_location(self):
        """测试 CreateUnitAtLoc 处理 None Location。"""
        from jass_runner.natives.unit_position_natives import CreateUnitAtLoc
        from jass_runner.natives.manager import HandleManager

        manager = HandleManager()

        create_unit_at_loc = CreateUnitAtLoc()

        class MockStateContext:
            def __init__(self):
                self.handle_manager = manager

        # 应该返回 None
        unit = create_unit_at_loc.execute(MockStateContext(), 0, 1213484355, None, 90.0)
        assert unit is None


class TestGetUnitFacing:
    """测试 GetUnitFacing native 函数。"""

    def test_get_unit_facing(self):
        """测试 GetUnitFacing native 函数。"""
        from jass_runner.natives.unit_position_natives import GetUnitFacing
        from jass_runner.natives.manager import HandleManager

        manager = HandleManager()
        unit = manager.create_unit("hfoo", 0, 100.0, 200.0, 45.0)

        get_unit_facing = GetUnitFacing()

        class MockStateContext:
            def __init__(self):
                self.handle_manager = manager

        result = get_unit_facing.execute(MockStateContext(), unit)
        assert result == 45.0

    def test_get_unit_facing_with_none_unit(self):
        """测试 GetUnitFacing 处理 None 单位。"""
        from jass_runner.natives.unit_position_natives import GetUnitFacing

        get_unit_facing = GetUnitFacing()

        class MockStateContext:
            pass

        # 应该返回 0.0
        result = get_unit_facing.execute(MockStateContext(), None)
        assert result == 0.0


class TestSetUnitFacing:
    """测试 SetUnitFacing native 函数。"""

    def test_set_unit_facing(self):
        """测试 SetUnitFacing native 函数。"""
        from jass_runner.natives.unit_position_natives import SetUnitFacing
        from jass_runner.natives.manager import HandleManager

        manager = HandleManager()
        unit = manager.create_unit("hfoo", 0, 100.0, 200.0, 0.0)

        set_unit_facing = SetUnitFacing()

        class MockStateContext:
            def __init__(self):
                self.handle_manager = manager

        set_unit_facing.execute(MockStateContext(), unit, 180.0)
        assert unit.facing == 180.0

    def test_set_unit_facing_with_none_unit(self):
        """测试 SetUnitFacing 处理 None 单位。"""
        from jass_runner.natives.unit_position_natives import SetUnitFacing

        set_unit_facing = SetUnitFacing()

        class MockStateContext:
            pass

        # 应该不抛出异常
        set_unit_facing.execute(MockStateContext(), None, 180.0)


class TestCreateUnitAtLocByName:
    """测试 CreateUnitAtLocByName native 函数。"""

    def test_create_unit_at_loc_by_name(self):
        """测试 CreateUnitAtLocByName native 函数。"""
        from jass_runner.natives.unit_position_natives import CreateUnitAtLocByName
        from jass_runner.natives.location import Location
        from jass_runner.natives.manager import HandleManager

        manager = HandleManager()

        create_unit_at_loc_by_name = CreateUnitAtLocByName()
        loc = Location(700.0, 800.0, 0.0)

        class MockStateContext:
            def __init__(self):
                self.handle_manager = manager

        # 使用单位名称创建（如 "footman"）
        unit = create_unit_at_loc_by_name.execute(MockStateContext(), 0, "footman", loc, 270.0)

        assert unit is not None
        assert unit.x == 700.0
        assert unit.y == 800.0
        assert unit.facing == 270.0

    def test_create_unit_at_loc_by_name_with_none_location(self):
        """测试 CreateUnitAtLocByName 处理 None Location。"""
        from jass_runner.natives.unit_position_natives import CreateUnitAtLocByName
        from jass_runner.natives.manager import HandleManager

        manager = HandleManager()

        create_unit_at_loc_by_name = CreateUnitAtLocByName()

        class MockStateContext:
            def __init__(self):
                self.handle_manager = manager

        # 应该返回 None
        unit = create_unit_at_loc_by_name.execute(MockStateContext(), 0, "footman", None, 270.0)
        assert unit is None

    def test_create_unit_at_loc_by_name_with_empty_name(self):
        """测试 CreateUnitAtLocByName 处理空名称。"""
        from jass_runner.natives.unit_position_natives import CreateUnitAtLocByName
        from jass_runner.natives.location import Location
        from jass_runner.natives.manager import HandleManager

        manager = HandleManager()

        create_unit_at_loc_by_name = CreateUnitAtLocByName()
        loc = Location(700.0, 800.0, 0.0)

        class MockStateContext:
            def __init__(self):
                self.handle_manager = manager

        # 应该返回 None
        unit = create_unit_at_loc_by_name.execute(MockStateContext(), 0, "", loc, 270.0)
        assert unit is None
