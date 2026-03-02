"""单位组Native函数测试。"""

import pytest
from jass_runner.natives.state import StateContext
from jass_runner.natives.group_natives import CreateGroup, DestroyGroup


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
