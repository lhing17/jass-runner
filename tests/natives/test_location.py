"""Location 类的测试。

此模块包含 Location 位置类的单元测试。
"""

import pytest


class TestLocation:
    """测试 Location 类的功能。"""

    def test_location_creation(self):
        """测试 Location 对象创建。"""
        from jass_runner.natives.location import Location

        loc = Location(100.0, 200.0)
        assert loc.x == 100.0
        assert loc.y == 200.0
        assert loc.z == 0.0  # 默认 z 为 0

    def test_location_creation_with_z(self):
        """测试带 z 坐标的 Location 创建。"""
        from jass_runner.natives.location import Location

        loc = Location(100.0, 200.0, 50.0)
        assert loc.x == 100.0
        assert loc.y == 200.0
        assert loc.z == 50.0
