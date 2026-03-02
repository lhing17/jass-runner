"""单位组枚举功能测试。"""

import pytest
from jass_runner.natives.handle import Group, Unit


class TestGroupEnumSupport:
    """测试Group类枚举支持功能。"""

    def test_group_get_size_empty(self):
        """测试获取空组大小。"""
        group = Group("group_1")
        assert group.get_size() == 0

    def test_group_get_size_with_units(self):
        """测试获取有单位的组大小。"""
        group = Group("group_1")
        unit1 = Unit("unit_1", "hfoo", 0, 100.0, 200.0, 0.0)
        unit2 = Unit("unit_2", "hfoo", 0, 150.0, 250.0, 0.0)
        group.add_unit(unit1)
        group.add_unit(unit2)

        assert group.get_size() == 2

    def test_group_unit_at_valid_index(self):
        """测试获取有效索引的单位。"""
        group = Group("group_1")
        unit = Unit("unit_1", "hfoo", 0, 100.0, 200.0, 0.0)
        group.add_unit(unit)

        result = group.unit_at(0)

        assert result == unit.id

    def test_group_unit_at_invalid_index(self):
        """测试获取无效索引返回None。"""
        group = Group("group_1")

        result = group.unit_at(0)

        assert result is None

    def test_group_unit_at_negative_index(self):
        """测试获取负索引返回None。"""
        group = Group("group_1")
        unit = Unit("unit_1", "hfoo", 0, 100.0, 200.0, 0.0)
        group.add_unit(unit)

        result = group.unit_at(-1)

        assert result is None
