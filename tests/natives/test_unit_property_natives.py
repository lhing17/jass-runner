"""单位属性 native 函数测试。

此模块包含单位属性访问和修改的 native 函数测试。
"""

import pytest
from jass_runner.natives.unit_property_natives import SetUnitState, GetUnitX, GetUnitY, GetUnitLoc, GetUnitTypeId, GetUnitName
from jass_runner.natives.manager import HandleManager
from jass_runner.natives.handle import Unit
from jass_runner.natives.location import Location


class TestSetUnitState:
    """测试 SetUnitState native 函数。"""

    def test_set_unit_state_native(self):
        """测试 SetUnitState native 函数。"""
        # 创建 HandleManager 和 unit
        manager = HandleManager()
        unit = manager.create_unit("hfoo", 0, 100.0, 200.0, 0.0)

        # 创建 native 函数
        set_unit_state = SetUnitState()

        # 创建 mock state_context
        class MockStateContext:
            def __init__(self):
                self.handle_manager = manager

        state_context = MockStateContext()

        # 设置生命值（UNIT_STATE_LIFE = 0）
        set_unit_state.execute(state_context, unit, 0, 75.0)

        # 验证
        assert unit.life == 75.0

    def test_set_unit_state_mana(self):
        """测试设置魔法值。"""
        manager = HandleManager()
        unit = manager.create_unit("hfoo", 0, 100.0, 200.0, 0.0)

        set_unit_state = SetUnitState()

        class MockStateContext:
            def __init__(self):
                self.handle_manager = manager

        state_context = MockStateContext()

        # 设置魔法值（UNIT_STATE_MANA = 2）
        set_unit_state.execute(state_context, unit, 2, 30.0)

        assert unit.mana == 30.0

    def test_set_unit_state_none_unit(self):
        """测试设置 None 单位的状态。"""
        set_unit_state = SetUnitState()

        class MockStateContext:
            pass

        state_context = MockStateContext()

        # 不应抛出异常
        set_unit_state.execute(state_context, None, 0, 75.0)

    def test_set_unit_state_invalid_state_type(self):
        """测试设置无效状态类型。"""
        manager = HandleManager()
        unit = manager.create_unit("hfoo", 0, 100.0, 200.0, 0.0)

        set_unit_state = SetUnitState()

        class MockStateContext:
            def __init__(self):
                self.handle_manager = manager

        state_context = MockStateContext()

        # 设置无效状态类型（999）
        set_unit_state.execute(state_context, unit, 999, 75.0)

        # 单位状态不应改变
        assert unit.life == 100.0


class TestGetUnitX:
    """测试 GetUnitX native 函数。"""

    def test_get_unit_x(self):
        """测试 GetUnitX native 函数。"""
        manager = HandleManager()
        unit = manager.create_unit("hfoo", 0, 150.0, 250.0, 0.0)

        get_unit_x = GetUnitX()

        class MockStateContext:
            def __init__(self):
                self.handle_manager = manager

        result = get_unit_x.execute(MockStateContext(), unit)
        assert result == 150.0

    def test_get_unit_x_none_unit(self):
        """测试获取 None 单位的 X 坐标。"""
        get_unit_x = GetUnitX()

        class MockStateContext:
            pass

        result = get_unit_x.execute(MockStateContext(), None)
        assert result == 0.0


class TestGetUnitY:
    """测试 GetUnitY native 函数。"""

    def test_get_unit_y(self):
        """测试 GetUnitY native 函数。"""
        manager = HandleManager()
        unit = manager.create_unit("hfoo", 0, 150.0, 250.0, 0.0)

        get_unit_y = GetUnitY()

        class MockStateContext:
            def __init__(self):
                self.handle_manager = manager

        result = get_unit_y.execute(MockStateContext(), unit)
        assert result == 250.0

    def test_get_unit_y_none_unit(self):
        """测试获取 None 单位的 Y 坐标。"""
        get_unit_y = GetUnitY()

        class MockStateContext:
            pass

        result = get_unit_y.execute(MockStateContext(), None)
        assert result == 0.0


class TestGetUnitLoc:
    """测试 GetUnitLoc native 函数。"""

    def test_get_unit_loc(self):
        """测试 GetUnitLoc native 函数。"""
        manager = HandleManager()
        unit = manager.create_unit("hfoo", 0, 150.0, 250.0, 0.0)
        unit.z = 30.0  # 设置 z 坐标

        get_unit_loc = GetUnitLoc()

        class MockStateContext:
            def __init__(self):
                self.handle_manager = manager

        result = get_unit_loc.execute(MockStateContext(), unit)
        assert isinstance(result, Location)
        assert result.x == 150.0
        assert result.y == 250.0
        assert result.z == 30.0

    def test_get_unit_loc_none_unit(self):
        """测试获取 None 单位的位置。"""
        get_unit_loc = GetUnitLoc()

        class MockStateContext:
            pass

        result = get_unit_loc.execute(MockStateContext(), None)
        assert isinstance(result, Location)
        assert result.x == 0.0
        assert result.y == 0.0
        assert result.z == 0.0


class TestGetUnitTypeId:
    """测试 GetUnitTypeId native 函数。"""

    def test_get_unit_type_id(self):
        """测试 GetUnitTypeId native 函数。"""
        from jass_runner.utils import fourcc_to_int

        manager = HandleManager()
        unit = manager.create_unit("hfoo", 0, 100.0, 200.0, 0.0)

        get_unit_type_id = GetUnitTypeId()

        class MockStateContext:
            def __init__(self):
                self.handle_manager = manager

        result = get_unit_type_id.execute(MockStateContext(), unit)

        # "hfoo" 转换为整数
        expected = fourcc_to_int("hfoo")
        assert result == expected

    def test_get_unit_type_id_none_unit(self):
        """测试获取 None 单位的类型 ID。"""
        get_unit_type_id = GetUnitTypeId()

        class MockStateContext:
            pass

        result = get_unit_type_id.execute(MockStateContext(), None)
        assert result == 0


class TestGetUnitName:
    """测试 GetUnitName native 函数。"""

    def test_get_unit_name(self):
        """测试 GetUnitName native 函数。"""
        manager = HandleManager()
        unit = manager.create_unit("hfoo", 0, 100.0, 200.0, 0.0)

        get_unit_name = GetUnitName()

        class MockStateContext:
            def __init__(self):
                self.handle_manager = manager

        result = get_unit_name.execute(MockStateContext(), unit)
        assert result == "hfoo"  # 默认使用 unit_type 作为名称

    def test_get_unit_name_none_unit(self):
        """测试获取 None 单位的名称。"""
        get_unit_name = GetUnitName()

        class MockStateContext:
            pass

        result = get_unit_name.execute(MockStateContext(), None)
        assert result == ""
