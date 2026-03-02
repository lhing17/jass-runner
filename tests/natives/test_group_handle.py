"""单位组Handle测试。"""

import pytest
from jass_runner.natives.handle import Group, Unit
from jass_runner.natives.manager import HandleManager


class TestGroupHandle:
    """测试Group类功能。"""

    def test_create_group(self):
        """测试创建Group对象。"""
        group = Group("group_1")
        assert group.id == "group_1"
        assert group.type_name == "group"
        assert len(group.get_units()) == 0

    def test_add_unit_to_group(self):
        """测试添加单位到组。"""
        group = Group("group_1")
        unit = Unit("unit_1", "hfoo", 0, 100.0, 200.0, 0.0)

        result = group.add_unit(unit)

        assert result is True
        assert len(group.get_units()) == 1
        assert unit.id in group.get_units()

    def test_remove_unit_from_group(self):
        """测试从组移除单位。"""
        group = Group("group_1")
        unit = Unit("unit_1", "hfoo", 0, 100.0, 200.0, 0.0)
        group.add_unit(unit)

        result = group.remove_unit(unit)

        assert result is True
        assert len(group.get_units()) == 0

    def test_clear_group(self):
        """测试清空单位组。"""
        group = Group("group_1")
        unit1 = Unit("unit_1", "hfoo", 0, 100.0, 200.0, 0.0)
        unit2 = Unit("unit_2", "hfoo", 0, 150.0, 250.0, 0.0)
        group.add_unit(unit1)
        group.add_unit(unit2)

        group.clear()

        assert len(group.get_units()) == 0

    def test_first_of_group(self):
        """测试获取组内第一个单位。"""
        group = Group("group_1")
        unit = Unit("unit_1", "hfoo", 0, 100.0, 200.0, 0.0)
        group.add_unit(unit)

        first = group.first()

        assert first == unit.id

    def test_is_unit_in_group(self):
        """测试检查单位是否在组内。"""
        group = Group("group_1")
        unit = Unit("unit_1", "hfoo", 0, 100.0, 200.0, 0.0)
        group.add_unit(unit)

        assert group.contains(unit) is True

        other_unit = Unit("unit_2", "hfoo", 0, 150.0, 250.0, 0.0)
        assert group.contains(other_unit) is False

    def test_add_dead_unit_fails(self):
        """测试添加已销毁的单位到组失败。"""
        group = Group("group_1")
        unit = Unit("unit_1", "hfoo", 0, 100.0, 200.0, 0.0)
        unit.destroy()

        result = group.add_unit(unit)

        assert result is False

    def test_add_duplicate_unit_fails(self):
        """测试重复添加同一单位到组失败。"""
        group = Group("group_1")
        unit = Unit("unit_1", "hfoo", 0, 100.0, 200.0, 0.0)
        group.add_unit(unit)

        result = group.add_unit(unit)

        assert result is False

    def test_remove_nonexistent_unit_fails(self):
        """测试移除不在组中的单位失败。"""
        group = Group("group_1")
        unit = Unit("unit_1", "hfoo", 0, 100.0, 200.0, 0.0)

        result = group.remove_unit(unit)

        assert result is False

    def test_first_of_empty_group_returns_none(self):
        """测试空组的first方法返回None。"""
        group = Group("group_1")

        first = group.first()

        assert first is None

    def test_contains_none_returns_false(self):
        """测试contains方法传入None返回False。"""
        group = Group("group_1")

        result = group.contains(None)

        assert result is False

    def test_group_size(self):
        """测试获取组内单位数量。"""
        group = Group("group_1")
        assert group.size() == 0

        unit1 = Unit("unit_1", "hfoo", 0, 100.0, 200.0, 0.0)
        group.add_unit(unit1)
        assert group.size() == 1

        unit2 = Unit("unit_2", "hfoo", 0, 150.0, 250.0, 0.0)
        group.add_unit(unit2)
        assert group.size() == 2


class TestHandleManagerGroupSupport:
    """测试HandleManager对Group的支持。"""

    def test_create_group_via_manager(self):
        """测试通过HandleManager创建Group。"""
        manager = HandleManager()

        group = manager.create_group()

        assert isinstance(group, Group)
        assert group.type_name == "group"
        assert group.id.startswith("group_")

    def test_get_group_via_manager(self):
        """测试通过HandleManager获取Group。"""
        manager = HandleManager()
        group = manager.create_group()

        retrieved = manager.get_group(group.id)

        assert retrieved == group

    def test_get_group_with_invalid_id_returns_none(self):
        """测试获取不存在的Group返回None。"""
        manager = HandleManager()

        result = manager.get_group("nonexistent_group")

        assert result is None

    def test_get_group_with_wrong_type_returns_none(self):
        """测试用错误类型获取Group返回None。"""
        manager = HandleManager()
        unit = manager.create_unit("hfoo", 0, 100.0, 200.0, 0.0)

        result = manager.get_group(unit.id)

        assert result is None
