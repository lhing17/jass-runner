"""HandleManager枚举功能测试。"""

import pytest
from jass_runner.natives.manager import HandleManager


class TestHandleManagerEnum:
    """测试HandleManager单位枚举功能。"""

    def test_enum_units_of_player(self):
        """测试按玩家枚举单位。"""
        manager = HandleManager()
        unit1 = manager.create_unit("hfoo", 0, 100.0, 200.0, 0.0)
        unit2 = manager.create_unit("hfoo", 0, 150.0, 250.0, 0.0)
        unit3 = manager.create_unit("hfoo", 1, 300.0, 400.0, 0.0)  # 不同玩家

        result = manager.enum_units_of_player(0)

        assert len(result) == 2
        assert unit1.id in result
        assert unit2.id in result
        assert unit3.id not in result

    def test_enum_units_in_range(self):
        """测试在范围内枚举单位。"""
        manager = HandleManager()
        unit1 = manager.create_unit("hfoo", 0, 100.0, 200.0, 0.0)  # 距离0
        unit2 = manager.create_unit("hfoo", 0, 150.0, 200.0, 0.0)  # 距离50
        unit3 = manager.create_unit("hfoo", 0, 300.0, 200.0, 0.0)  # 距离200，超出范围

        result = manager.enum_units_in_range(100.0, 200.0, 100.0)  # 中心(100,200)，半径100

        assert len(result) == 2
        assert unit1.id in result
        assert unit2.id in result
        assert unit3.id not in result

    def test_enum_units_in_range_no_units(self):
        """测试在范围内没有单位。"""
        manager = HandleManager()
        manager.create_unit("hfoo", 0, 1000.0, 2000.0, 0.0)  # 远离中心

        result = manager.enum_units_in_range(0.0, 0.0, 100.0)

        assert len(result) == 0

    def test_enum_units_of_type(self):
        """测试按类型枚举单位。"""
        manager = HandleManager()
        unit1 = manager.create_unit("hfoo", 0, 100.0, 200.0, 0.0)  # 步兵
        unit2 = manager.create_unit("hfoo", 0, 150.0, 250.0, 0.0)  # 步兵
        unit3 = manager.create_unit("hkni", 0, 300.0, 400.0, 0.0)  # 骑士

        result = manager.enum_units_of_type("hfoo")

        assert len(result) == 2
        assert unit1.id in result
        assert unit2.id in result
        assert unit3.id not in result
