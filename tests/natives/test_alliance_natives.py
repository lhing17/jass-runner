"""联盟相关 native 函数测试。"""

import pytest
from unittest.mock import MagicMock
from src.jass_runner.natives.alliance_natives import ConvertAllianceType
from src.jass_runner.natives.alliance import ALLIANCE_PASSIVE, ALLIANCE_SHARED_VISION


class TestConvertAllianceType:
    """测试 ConvertAllianceType native 函数。"""

    def test_convert_alliance_type_returns_input(self):
        """测试 ConvertAllianceType 返回传入的整数。"""
        native = ConvertAllianceType()
        state_context = MagicMock()

        result = native.execute(state_context, 0)
        assert result == 0

        result = native.execute(state_context, 5)
        assert result == 5

    def test_convert_alliance_type_with_constants(self):
        """测试使用联盟常量。"""
        native = ConvertAllianceType()
        state_context = MagicMock()

        assert native.execute(state_context, ALLIANCE_PASSIVE) == ALLIANCE_PASSIVE
        assert native.execute(state_context, ALLIANCE_SHARED_VISION) == ALLIANCE_SHARED_VISION
