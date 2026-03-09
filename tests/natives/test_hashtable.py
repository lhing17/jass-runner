"""Hashtable 类测试"""

import pytest
from jass_runner.natives.hashtable import Hashtable


class TestHashtableCreation:
    """测试 Hashtable 创建"""

    def test_hashtable_creation(self):
        """测试 Hashtable 创建和基本属性"""
        ht = Hashtable("hashtable_1")

        assert ht.id == "hashtable_1"
        assert ht.type_name == "hashtable"
        assert ht.is_alive()

    def test_hashtable_default_values(self):
        """测试 DEFAULT_VALUES 常量"""
        assert Hashtable.DEFAULT_VALUES["integer"] == 0
        assert Hashtable.DEFAULT_VALUES["real"] == 0.0
        assert Hashtable.DEFAULT_VALUES["boolean"] == False
        assert Hashtable.DEFAULT_VALUES["string"] is None
        assert Hashtable.DEFAULT_VALUES["unit"] is None


class TestHashtableBasicTypes:
    """测试基础类型 Save/Load"""

    def test_save_and_load_integer(self):
        """测试整数存储和加载"""
        ht = Hashtable("ht_1")

        ht.save_integer(0, 0, 42)
        result = ht.load_integer(0, 0)

        assert result == 42

    def test_load_integer_default(self):
        """测试加载未设置的整数返回默认值"""
        ht = Hashtable("ht_1")

        result = ht.load_integer(0, 0)

        assert result == 0

    def test_save_and_load_real(self):
        """测试实数存储和加载"""
        ht = Hashtable("ht_1")

        ht.save_real(0, 0, 3.14)
        result = ht.load_real(0, 0)

        assert result == 3.14

    def test_save_and_load_boolean(self):
        """测试布尔值存储和加载"""
        ht = Hashtable("ht_1")

        ht.save_boolean(0, 0, True)
        result = ht.load_boolean(0, 0)

        assert result is True

    def test_save_and_load_string(self):
        """测试字符串存储和加载"""
        ht = Hashtable("ht_1")

        ht.save_string(0, 0, "hello")
        result = ht.load_string(0, 0)

        assert result == "hello"

    def test_multiple_types_same_key(self):
        """测试同一键下存储不同类型"""
        ht = Hashtable("ht_1")

        ht.save_integer(0, 0, 42)
        ht.save_real(0, 0, 3.14)
        ht.save_string(0, 0, "test")

        assert ht.load_integer(0, 0) == 42
        assert ht.load_real(0, 0) == 3.14
        assert ht.load_string(0, 0) == "test"


from unittest.mock import Mock


class TestHashtableHandleTypes:
    """测试 Handle 类型 Save/Load"""

    def test_save_and_load_unit_handle(self):
        """测试单位 handle 存储和加载"""
        ht = Hashtable("ht_1")
        mock_unit = Mock()
        mock_unit.id = "unit_123"

        ht.save_unit_handle(0, 0, mock_unit)

        # 验证存储的是 handle_id
        assert ht._data[0][0]["unit"] == "unit_123"

    def test_load_unit_handle(self):
        """测试加载单位 handle"""
        ht = Hashtable("ht_1")
        mock_manager = Mock()
        mock_unit = Mock()
        mock_manager.get_unit.return_value = mock_unit

        # 直接设置内部数据
        ht._data[0] = {0: {"unit": "unit_123"}}

        result = ht.load_unit_handle(0, 0, mock_manager)

        assert result == mock_unit
        mock_manager.get_unit.assert_called_once_with("unit_123")

    def test_load_unit_handle_not_found(self):
        """测试加载不存在的单位返回 None"""
        ht = Hashtable("ht_1")
        mock_manager = Mock()
        mock_manager.get_unit.return_value = None

        ht._data[0] = {0: {"unit": "unit_123"}}

        result = ht.load_unit_handle(0, 0, mock_manager)

        assert result is None

    def test_load_unit_handle_no_data(self):
        """测试加载未设置过的单位返回 None"""
        ht = Hashtable("ht_1")
        mock_manager = Mock()

        result = ht.load_unit_handle(0, 0, mock_manager)

        assert result is None
        mock_manager.get_unit.assert_not_called()

    def test_save_and_load_player_handle(self):
        """测试玩家 handle 存储和加载"""
        ht = Hashtable("ht_1")
        mock_player = Mock()
        mock_player.id = "player_0"

        ht.save_player_handle(0, 0, mock_player)

        assert ht._data[0][0]["player"] == "player_0"

    def test_save_and_load_item_handle(self):
        """测试物品 handle 存储和加载"""
        ht = Hashtable("ht_1")
        mock_item = Mock()
        mock_item.id = "item_456"

        ht.save_item_handle(0, 0, mock_item)

        assert ht._data[0][0]["item"] == "item_456"


class TestHashtableExistenceAndRemoval:
    """测试存在性检查和删除方法"""

    def test_have_saved_integer_true(self):
        """测试检查存在的整数"""
        ht = Hashtable("ht_1")
        ht.save_integer(0, 0, 42)

        assert ht.have_saved_integer(0, 0) is True

    def test_have_saved_integer_false(self):
        """测试检查不存在的整数"""
        ht = Hashtable("ht_1")

        assert ht.have_saved_integer(0, 0) is False

    def test_have_saved_handle(self):
        """测试检查任意 handle 类型"""
        ht = Hashtable("ht_1")
        mock_unit = Mock()
        mock_unit.id = "unit_123"

        ht.save_unit_handle(0, 0, mock_unit)

        assert ht.have_saved_handle(0, 0) is True
        assert ht.have_saved_integer(0, 0) is False  # 整数不存在

    def test_remove_saved_integer(self):
        """测试删除整数"""
        ht = Hashtable("ht_1")
        ht.save_integer(0, 0, 42)

        ht.remove_saved_integer(0, 0)

        assert ht.have_saved_integer(0, 0) is False
        assert ht.load_integer(0, 0) == 0  # 返回默认值

    def test_remove_saved_handle(self):
        """测试删除所有 handle 类型"""
        ht = Hashtable("ht_1")
        mock_unit = Mock()
        mock_unit.id = "unit_123"
        mock_item = Mock()
        mock_item.id = "item_456"

        ht.save_unit_handle(0, 0, mock_unit)
        ht.save_item_handle(0, 0, mock_item)
        ht.save_integer(0, 0, 42)

        ht.remove_saved_handle(0, 0)

        assert ht.have_saved_handle(0, 0) is False
        assert ht.have_saved_integer(0, 0) is True  # 整数仍然存在


class TestHashtableFlush:
    """测试清空方法"""

    def test_flush_child(self):
        """测试清空指定 parentKey 下所有数据"""
        ht = Hashtable("ht_1")
        ht.save_integer(0, 0, 42)
        ht.save_integer(0, 1, 100)
        ht.save_integer(1, 0, 200)

        ht.flush_child(0)

        assert ht.load_integer(0, 0) == 0
        assert ht.load_integer(0, 1) == 0
        assert ht.load_integer(1, 0) == 200  # parentKey=1 的数据保留

    def test_flush_all(self):
        """测试清空整个 hashtable"""
        ht = Hashtable("ht_1")
        ht.save_integer(0, 0, 42)
        ht.save_real(1, 1, 3.14)

        ht.flush_all()

        assert ht.load_integer(0, 0) == 0
        assert ht.load_real(1, 1) == 0.0
        assert ht._data == {}
