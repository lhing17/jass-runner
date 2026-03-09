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
