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
