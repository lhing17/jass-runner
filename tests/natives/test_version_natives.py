import pytest
from unittest.mock import MagicMock
from jass_runner.natives.version_natives import VersionGet, VERSION_FROZEN_THRONE


class TestVersionGet:
    """测试VersionGet native函数。"""

    def test_version_get_returns_frozen_throne(self):
        """测试VersionGet返回冰封王座版本。"""
        # 准备
        native = VersionGet()
        mock_state = MagicMock()

        # 执行
        result = native.execute(mock_state)

        # 验证
        assert result == VERSION_FROZEN_THRONE
        assert result == 1
