"""单位范围检测Native函数测试。"""

import pytest
import math
from jass_runner.natives.unit_range_natives import IsUnitInRangeXY, IsUnitInRangeLoc, IsUnitInRange
from jass_runner.natives.handle import Unit
from jass_runner.natives.location import Location


class TestIsUnitInRangeXY:
    """测试IsUnitInRangeXY函数。"""

    def test_unit_in_range_returns_true(self):
        """测试单位在范围内返回True。"""
        native = IsUnitInRangeXY()
        unit = Unit("unit_001", "Hpal", 0, 0.0, 0.0, 0.0)

        result = native.execute(unit, 100.0, 0.0, 150.0)

        assert result is True

    def test_unit_out_of_range_returns_false(self):
        """测试单位在范围外返回False。"""
        native = IsUnitInRangeXY()
        unit = Unit("unit_001", "Hpal", 0, 0.0, 0.0, 0.0)

        result = native.execute(unit, 200.0, 0.0, 150.0)

        assert result is False

    def test_unit_at_exact_distance_returns_true(self):
        """测试单位恰好在边界距离返回True。"""
        native = IsUnitInRangeXY()
        unit = Unit("unit_001", "Hpal", 0, 100.0, 0.0, 0.0)

        result = native.execute(unit, 0.0, 0.0, 100.0)

        assert result is True

    def test_diagonal_distance(self):
        """测试对角线距离计算。"""
        native = IsUnitInRangeXY()
        unit = Unit("unit_001", "Hpal", 0, 30.0, 40.0, 0.0)  # 距离50

        result = native.execute(unit, 0.0, 0.0, 50.0)

        assert result is True

        result = native.execute(unit, 0.0, 0.0, 49.9)

        assert result is False

    def test_null_unit_returns_false(self):
        """测试null单位返回False。"""
        native = IsUnitInRangeXY()

        result = native.execute(None, 0.0, 0.0, 100.0)

        assert result is False

    def test_negative_distance_treated_as_zero(self):
        """测试负距离视为0。"""
        native = IsUnitInRangeXY()
        unit = Unit("unit_001", "Hpal", 0, 0.0, 0.0, 0.0)

        result = native.execute(unit, 0.0, 0.0, -10.0)

        # 距离为0，只有恰好在同一点才返回True
        assert result is True


class TestIsUnitInRangeLoc:
    """测试IsUnitInRangeLoc函数。"""

    def test_unit_in_range_of_location(self):
        """测试单位在位置范围内返回True。"""
        native = IsUnitInRangeLoc()
        unit = Unit("unit_001", "Hpal", 0, 0.0, 0.0, 0.0)
        loc = Location(100.0, 0.0)

        result = native.execute(unit, loc, 150.0)

        assert result is True

    def test_unit_out_of_range_of_location(self):
        """测试单位在位置范围外返回False。"""
        native = IsUnitInRangeLoc()
        unit = Unit("unit_001", "Hpal", 0, 0.0, 0.0, 0.0)
        loc = Location(200.0, 0.0)

        result = native.execute(unit, loc, 150.0)

        assert result is False

    def test_null_location_returns_false(self):
        """测试null位置返回False。"""
        native = IsUnitInRangeLoc()
        unit = Unit("unit_001", "Hpal", 0, 0.0, 0.0, 0.0)

        result = native.execute(unit, None, 100.0)

        assert result is False


class TestIsUnitInRange:
    """测试IsUnitInRange函数。"""

    def test_unit_in_range_of_other_unit(self):
        """测试单位在另一个单位范围内返回True。"""
        native = IsUnitInRange()
        unit1 = Unit("unit_001", "Hpal", 0, 0.0, 0.0, 0.0)
        unit2 = Unit("unit_002", "Hpal", 0, 100.0, 0.0, 0.0)

        result = native.execute(unit1, unit2, 150.0)

        assert result is True

    def test_unit_out_of_range_of_other_unit(self):
        """测试单位在另一个单位范围外返回False。"""
        native = IsUnitInRange()
        unit1 = Unit("unit_001", "Hpal", 0, 0.0, 0.0, 0.0)
        unit2 = Unit("unit_002", "Hpal", 0, 200.0, 0.0, 0.0)

        result = native.execute(unit1, unit2, 150.0)

        assert result is False

    def test_null_other_unit_returns_false(self):
        """测试null其他单位返回False。"""
        native = IsUnitInRange()
        unit1 = Unit("unit_001", "Hpal", 0, 0.0, 0.0, 0.0)

        result = native.execute(unit1, None, 100.0)

        assert result is False
