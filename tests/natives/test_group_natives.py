"""单位组Native函数测试。"""

import pytest
from jass_runner.natives.state import StateContext
from jass_runner.natives.group_natives import CreateGroup, DestroyGroup, GroupAddUnit, GroupRemoveUnit, GroupClear, FirstOfGroup, IsUnitInGroup


class TestCreateGroup:
    """测试CreateGroup native函数。"""

    def test_create_group_returns_group(self):
        """测试CreateGroup返回group handle。"""
        state = StateContext()
        create_group = CreateGroup()

        result = create_group.execute(state)

        assert result is not None
        assert result.type_name == "group"
        # 验证组已注册到HandleManager
        group_from_manager = state.handle_manager.get_group(result.id)
        assert group_from_manager is not None
        assert group_from_manager.id == result.id


class TestDestroyGroup:
    """测试DestroyGroup native函数。"""

    def test_destroy_group_removes_group(self):
        """测试DestroyGroup销毁单位组。"""
        state = StateContext()
        create_group = CreateGroup()
        destroy_group = DestroyGroup()

        # 先创建组
        group = create_group.execute(state)
        group_id = group.id

        # 销毁组
        result = destroy_group.execute(state, group)

        assert result is True
        # 验证组已被销毁
        group_from_manager = state.handle_manager.get_group(group_id)
        assert group_from_manager is None

    def test_destroy_nonexistent_group_returns_false(self):
        """测试销毁不存在的组返回False。"""
        state = StateContext()
        destroy_group = DestroyGroup()

        # 创建一个组然后手动销毁
        from jass_runner.natives.handle import Group
        group = Group("group_test")
        group.destroy()

        result = destroy_group.execute(state, group)

        assert result is False


class TestGroupAddUnit:
    """测试GroupAddUnit native函数。"""

    def test_add_unit_to_group(self):
        """测试添加单位到组。"""
        state = StateContext()
        from jass_runner.natives.group_natives import CreateGroup, GroupAddUnit

        create_group = CreateGroup()
        add_unit = GroupAddUnit()

        group = create_group.execute(state)
        unit = state.handle_manager.create_unit("hfoo", 0, 100.0, 200.0, 0.0)

        result = add_unit.execute(state, group, unit)

        assert result is True
        assert group.contains(unit) is True

    def test_add_same_unit_twice_returns_false(self):
        """测试重复添加同一单位返回False。"""
        state = StateContext()
        from jass_runner.natives.group_natives import CreateGroup, GroupAddUnit

        create_group = CreateGroup()
        add_unit = GroupAddUnit()

        group = create_group.execute(state)
        unit = state.handle_manager.create_unit("hfoo", 0, 100.0, 200.0, 0.0)

        add_unit.execute(state, group, unit)
        result = add_unit.execute(state, group, unit)

        assert result is False


class TestGroupRemoveUnit:
    """测试GroupRemoveUnit native函数。"""

    def test_remove_unit_from_group(self):
        """测试从组移除单位。"""
        state = StateContext()
        from jass_runner.natives.group_natives import CreateGroup, GroupAddUnit, GroupRemoveUnit

        create_group = CreateGroup()
        add_unit = GroupAddUnit()
        remove_unit = GroupRemoveUnit()

        group = create_group.execute(state)
        unit = state.handle_manager.create_unit("hfoo", 0, 100.0, 200.0, 0.0)
        add_unit.execute(state, group, unit)

        result = remove_unit.execute(state, group, unit)

        assert result is True
        assert group.contains(unit) is False


class TestGroupClear:
    """测试GroupClear native函数。"""

    def test_clear_group_removes_all_units(self):
        """测试清空组移除所有单位。"""
        state = StateContext()
        from jass_runner.natives.group_natives import CreateGroup, GroupAddUnit, GroupClear

        create_group = CreateGroup()
        add_unit = GroupAddUnit()
        clear_group = GroupClear()

        group = create_group.execute(state)
        unit1 = state.handle_manager.create_unit("hfoo", 0, 100.0, 200.0, 0.0)
        unit2 = state.handle_manager.create_unit("hfoo", 0, 150.0, 250.0, 0.0)
        add_unit.execute(state, group, unit1)
        add_unit.execute(state, group, unit2)

        result = clear_group.execute(state, group)

        assert result is True
        assert group.size() == 0


class TestFirstOfGroup:
    """测试FirstOfGroup native函数。"""

    def test_first_of_group_returns_unit(self):
        """测试FirstOfGroup返回组内第一个单位。"""
        state = StateContext()
        from jass_runner.natives.group_natives import CreateGroup, GroupAddUnit, FirstOfGroup

        create_group = CreateGroup()
        add_unit = GroupAddUnit()
        first_of_group = FirstOfGroup()

        group = create_group.execute(state)
        unit = state.handle_manager.create_unit("hfoo", 0, 100.0, 200.0, 0.0)
        add_unit.execute(state, group, unit)

        result = first_of_group.execute(state, group)

        assert result == unit

    def test_first_of_empty_group_returns_none(self):
        """测试空组返回None。"""
        state = StateContext()
        from jass_runner.natives.group_natives import CreateGroup, FirstOfGroup

        create_group = CreateGroup()
        first_of_group = FirstOfGroup()

        group = create_group.execute(state)

        result = first_of_group.execute(state, group)

        assert result is None


class TestIsUnitInGroup:
    """测试IsUnitInGroup native函数。"""

    def test_unit_in_group_returns_true(self):
        """测试单位在组内返回True。"""
        state = StateContext()
        from jass_runner.natives.group_natives import CreateGroup, GroupAddUnit, IsUnitInGroup

        create_group = CreateGroup()
        add_unit = GroupAddUnit()
        is_unit_in_group = IsUnitInGroup()

        group = create_group.execute(state)
        unit = state.handle_manager.create_unit("hfoo", 0, 100.0, 200.0, 0.0)
        add_unit.execute(state, group, unit)

        result = is_unit_in_group.execute(state, unit, group)

        assert result is True

    def test_unit_not_in_group_returns_false(self):
        """测试单位不在组内返回False。"""
        state = StateContext()
        from jass_runner.natives.group_natives import CreateGroup, IsUnitInGroup

        create_group = CreateGroup()
        is_unit_in_group = IsUnitInGroup()

        group = create_group.execute(state)
        unit = state.handle_manager.create_unit("hfoo", 0, 100.0, 200.0, 0.0)
        # 不添加到组

        result = is_unit_in_group.execute(state, unit, group)

        assert result is False
