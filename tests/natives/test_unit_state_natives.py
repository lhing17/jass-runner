"""单位状态Native函数测试。

此模块包含单位状态相关native函数的测试用例。
"""

import pytest
from jass_runner.natives.state import StateContext
from jass_runner.natives.unit_state_natives import GetWidgetLife, SetWidgetLife, UnitDamageTarget, GetUnitLevel


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


class TestUnitDamageTarget:
    """测试UnitDamageTarget native函数。"""

    def test_damage_target_reduces_life(self):
        """测试对目标造成伤害减少生命值。"""
        state = StateContext()
        damage_target = UnitDamageTarget()
        get_life = GetWidgetLife()

        attacker = state.handle_manager.create_unit("hfoo", 0, 100.0, 200.0, 0.0)
        target = state.handle_manager.create_unit("hfoo", 1, 150.0, 200.0, 0.0)

        # 造成25点伤害
        damage_target.execute(state, attacker, target, 25.0, True, False, 0, 0, 0)

        result = get_life.execute(state, target)
        assert result == 75.0  # 100 - 25 = 75

    def test_damage_target_can_kill(self):
        """测试伤害可以杀死目标。"""
        state = StateContext()
        damage_target = UnitDamageTarget()

        attacker = state.handle_manager.create_unit("hfoo", 0, 100.0, 200.0, 0.0)
        target = state.handle_manager.create_unit("hfoo", 1, 150.0, 200.0, 0.0)

        # 造成100点伤害（致命）
        damage_target.execute(state, attacker, target, 100.0, True, False, 0, 0, 0)

        assert not target.is_alive()

    def test_damage_target_with_none_params(self):
        """测试None参数不报错。"""
        state = StateContext()
        damage_target = UnitDamageTarget()

        # 应该不报错
        damage_target.execute(state, None, None, 25.0, True, False, 0, 0, 0)


class TestGetUnitLevel:
    """测试GetUnitLevel native函数。"""

    def test_get_unit_level_default(self):
        """测试获取单位默认等级。"""
        state = StateContext()
        get_level = GetUnitLevel()

        unit = state.handle_manager.create_unit("hfoo", 0, 100.0, 200.0, 0.0)
        # 默认等级为1
        result = get_level.execute(state, unit)

        assert result == 1

    def test_get_unit_level_custom(self):
        """测试获取自定义等级。"""
        state = StateContext()
        get_level = GetUnitLevel()

        unit = state.handle_manager.create_unit("hfoo", 0, 100.0, 200.0, 0.0)
        unit.level = 5

        result = get_level.execute(state, unit)
        assert result == 5

    def test_get_unit_level_of_none(self):
        """测试获取None等级返回0。"""
        state = StateContext()
        get_level = GetUnitLevel()

        result = get_level.execute(state, None)

        assert result == 0
