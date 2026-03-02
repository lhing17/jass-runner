"""单位状态Native函数测试。

此模块包含单位状态相关native函数的测试用例。
"""

import pytest
from jass_runner.natives.state import StateContext
from jass_runner.natives.unit_state_natives import GetWidgetLife, SetWidgetLife


class TestGetWidgetLife:
    """测试GetWidgetLife native函数。"""

    def test_get_widget_life_of_unit(self):
        """测试获取单位生命值。"""
        state = StateContext()
        get_life = GetWidgetLife()

        unit = state.handle_manager.create_unit("hfoo", 0, 100.0, 200.0, 0.0)
        # 默认生命值为100
        result = get_life.execute(state, unit)

        assert result == 100.0

    def test_get_widget_life_of_none(self):
        """测试获取None生命值返回0。"""
        state = StateContext()
        get_life = GetWidgetLife()

        result = get_life.execute(state, None)

        assert result == 0.0


class TestSetWidgetLife:
    """测试SetWidgetLife native函数。"""

    def test_set_widget_life(self):
        """测试设置单位生命值。"""
        state = StateContext()
        get_life = GetWidgetLife()
        set_life = SetWidgetLife()

        unit = state.handle_manager.create_unit("hfoo", 0, 100.0, 200.0, 0.0)
        # 设置生命值为50
        set_life.execute(state, unit, 50.0)

        result = get_life.execute(state, unit)
        assert result == 50.0

    def test_set_widget_life_to_zero_kills_unit(self):
        """测试设置生命值为0会杀死单位。"""
        state = StateContext()
        set_life = SetWidgetLife()

        unit = state.handle_manager.create_unit("hfoo", 0, 100.0, 200.0, 0.0)
        # 设置生命值为0
        set_life.execute(state, unit, 0.0)

        assert not unit.is_alive()

    def test_set_widget_life_of_none(self):
        """测试设置None生命值不报错。"""
        state = StateContext()
        set_life = SetWidgetLife()

        # 应该不报错
        set_life.execute(state, None, 50.0)
