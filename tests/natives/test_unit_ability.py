"""单位技能系统测试。"""

import pytest
from jass_runner.natives.handle import Unit


class TestUnitAbility:
    """测试Unit类技能功能。"""

    def test_add_ability_to_unit(self):
        """测试给单位添加技能。"""
        unit = Unit("unit_1", "hfoo", 0, 100.0, 200.0, 0.0)
        ability_id = 1097699445  # 'AHhb' - 圣光术

        result = unit.add_ability(ability_id)

        assert result is True
        assert unit.has_ability(ability_id) is True
        assert unit.get_ability_level(ability_id) == 1

    def test_add_duplicate_ability_fails(self):
        """测试重复添加技能失败。"""
        unit = Unit("unit_1", "hfoo", 0, 100.0, 200.0, 0.0)
        ability_id = 1097699445

        unit.add_ability(ability_id)
        result = unit.add_ability(ability_id)

        assert result is False

    def test_remove_ability_from_unit(self):
        """测试从单位移除技能。"""
        unit = Unit("unit_1", "hfoo", 0, 100.0, 200.0, 0.0)
        ability_id = 1097699445
        unit.add_ability(ability_id)

        result = unit.remove_ability(ability_id)

        assert result is True
        assert unit.has_ability(ability_id) is False

    def test_remove_nonexistent_ability_fails(self):
        """测试移除不存在的技能失败。"""
        unit = Unit("unit_1", "hfoo", 0, 100.0, 200.0, 0.0)
        ability_id = 1097699445

        result = unit.remove_ability(ability_id)

        assert result is False

    def test_set_ability_level(self):
        """测试设置技能等级。"""
        unit = Unit("unit_1", "hfoo", 0, 100.0, 200.0, 0.0)
        ability_id = 1097699445
        unit.add_ability(ability_id)

        result = unit.set_ability_level(ability_id, 3)

        assert result is True
        assert unit.get_ability_level(ability_id) == 3

    def test_increment_ability_level(self):
        """测试增加技能等级。"""
        unit = Unit("unit_1", "hfoo", 0, 100.0, 200.0, 0.0)
        ability_id = 1097699445
        unit.add_ability(ability_id)

        result = unit.inc_ability_level(ability_id)

        assert result is True
        assert unit.get_ability_level(ability_id) == 2

    def test_decrement_ability_level(self):
        """测试降低技能等级。"""
        unit = Unit("unit_1", "hfoo", 0, 100.0, 200.0, 0.0)
        ability_id = 1097699445
        unit.add_ability(ability_id)
        unit.set_ability_level(ability_id, 3)

        result = unit.dec_ability_level(ability_id)

        assert result is True
        assert unit.get_ability_level(ability_id) == 2

    def test_get_ability_level_nonexistent(self):
        """测试获取不存在技能的等级返回0。"""
        unit = Unit("unit_1", "hfoo", 0, 100.0, 200.0, 0.0)
        ability_id = 1097699445

        level = unit.get_ability_level(ability_id)

        assert level == 0

    def test_set_ability_level_nonexistent_fails(self):
        """测试为不存在的技能设置等级失败。"""
        unit = Unit("unit_1", "hfoo", 0, 100.0, 200.0, 0.0)
        ability_id = 1097699445

        result = unit.set_ability_level(ability_id, 3)

        assert result is False

    def test_set_invalid_ability_level_fails(self):
        """测试设置无效技能等级失败。"""
        unit = Unit("unit_1", "hfoo", 0, 100.0, 200.0, 0.0)
        ability_id = 1097699445
        unit.add_ability(ability_id)

        result = unit.set_ability_level(ability_id, 0)

        assert result is False

    def test_increment_nonexistent_ability_fails(self):
        """测试增加不存在技能等级失败。"""
        unit = Unit("unit_1", "hfoo", 0, 100.0, 200.0, 0.0)
        ability_id = 1097699445

        result = unit.inc_ability_level(ability_id)

        assert result is False

    def test_decrement_nonexistent_ability_fails(self):
        """测试降低不存在技能等级失败。"""
        unit = Unit("unit_1", "hfoo", 0, 100.0, 200.0, 0.0)
        ability_id = 1097699445

        result = unit.dec_ability_level(ability_id)

        assert result is False

    def test_decrement_ability_level_to_zero_fails(self):
        """测试降低技能等级到1以下失败。"""
        unit = Unit("unit_1", "hfoo", 0, 100.0, 200.0, 0.0)
        ability_id = 1097699445
        unit.add_ability(ability_id)  # 等级为1

        result = unit.dec_ability_level(ability_id)

        assert result is False
        assert unit.get_ability_level(ability_id) == 1

    def test_make_ability_permanent(self):
        """测试设置技能为永久技能。"""
        unit = Unit("unit_1", "hfoo", 0, 100.0, 200.0, 0.0)
        ability_id = 1097699445
        unit.add_ability(ability_id)

        result = unit.make_ability_permanent(ability_id, True)

        assert result is True
        assert unit.is_ability_permanent(ability_id) is True

    def test_make_nonexistent_ability_permanent_fails(self):
        """测试为不存在技能设置永久标记失败。"""
        unit = Unit("unit_1", "hfoo", 0, 100.0, 200.0, 0.0)
        ability_id = 1097699445

        result = unit.make_ability_permanent(ability_id, True)

        assert result is False

    def test_remove_ability_clears_permanent_flag(self):
        """测试移除技能时清除永久标记。"""
        unit = Unit("unit_1", "hfoo", 0, 100.0, 200.0, 0.0)
        ability_id = 1097699445
        unit.add_ability(ability_id)
        unit.make_ability_permanent(ability_id, True)

        unit.remove_ability(ability_id)

        assert unit.is_ability_permanent(ability_id) is False

    def test_cancel_ability_permanent(self):
        """测试取消技能的永久标记。"""
        unit = Unit("unit_1", "hfoo", 0, 100.0, 200.0, 0.0)
        ability_id = 1097699445
        unit.add_ability(ability_id)
        unit.make_ability_permanent(ability_id, True)

        result = unit.make_ability_permanent(ability_id, False)

        assert result is True
        assert unit.is_ability_permanent(ability_id) is False
