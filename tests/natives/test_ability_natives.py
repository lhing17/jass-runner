"""技能Native函数测试。
"""

import pytest
from jass_runner.natives.state import StateContext
from jass_runner.natives.ability_natives import UnitAddAbility, UnitRemoveAbility


class TestUnitAddAbility:
    """测试UnitAddAbility native函数。"""

    def test_add_ability_to_unit(self):
        """测试给单位添加技能。"""
        state = StateContext()
        add_ability = UnitAddAbility()
        unit = state.handle_manager.create_unit("hfoo", 0, 100.0, 200.0, 0.0)
        ability_id = 1097699445  # 'AHhb'

        result = add_ability.execute(state, unit, ability_id)

        assert result is True
        assert unit.has_ability(ability_id) is True

    def test_add_ability_to_none_unit_returns_false(self):
        """测试给None单位添加技能返回False。"""
        state = StateContext()
        add_ability = UnitAddAbility()

        result = add_ability.execute(state, None, 1097699445)

        assert result is False


class TestUnitRemoveAbility:
    """测试UnitRemoveAbility native函数。"""

    def test_remove_ability_from_unit(self):
        """测试从单位移除技能。"""
        state = StateContext()
        add_ability = UnitAddAbility()
        remove_ability = UnitRemoveAbility()
        unit = state.handle_manager.create_unit("hfoo", 0, 100.0, 200.0, 0.0)
        ability_id = 1097699445

        add_ability.execute(state, unit, ability_id)
        result = remove_ability.execute(state, unit, ability_id)

        assert result is True
        assert unit.has_ability(ability_id) is False

    def test_remove_nonexistent_ability_returns_false(self):
        """测试移除不存在的技能返回False。"""
        state = StateContext()
        remove_ability = UnitRemoveAbility()
        unit = state.handle_manager.create_unit("hfoo", 0, 100.0, 200.0, 0.0)

        result = remove_ability.execute(state, unit, 1097699445)

        assert result is False
