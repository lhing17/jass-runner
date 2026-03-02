"""单位属性 native 函数测试。

此模块包含单位属性访问和修改的 native 函数测试。
"""

import pytest
from jass_runner.natives.unit_property_natives import SetUnitState
from jass_runner.natives.manager import HandleManager
from jass_runner.natives.handle import Unit


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
