import pytest
from unittest.mock import MagicMock, patch
from jass_runner.natives.version_natives import VersionGet, ConvertVersion, VERSION_FROZEN_THRONE, Version


class TestConvertVersion:
    """测试ConvertVersion native函数。"""

    def test_convert_version_returns_input(self):
        """测试ConvertVersion返回传入的值。"""
        # 准备
        native = ConvertVersion()
        mock_state = MagicMock()

        # 执行
        result = native.execute(mock_state, 0)

        # 验证
        assert result == 0

    def test_convert_version_with_frozen_throne(self):
        """测试ConvertVersion处理冰封王座版本。"""
        # 准备
        native = ConvertVersion()
        mock_state = MagicMock()

        # 执行
        result = native.execute(mock_state, VERSION_FROZEN_THRONE)

        # 验证
        assert result == VERSION_FROZEN_THRONE
        assert result == 1


class TestVersionGet:
    """测试VersionGet native函数。"""

    def test_version_get_returns_version_handle(self):
        """测试VersionGet返回Version handle对象。"""
        # 准备
        native = VersionGet()
        mock_state = MagicMock()
        mock_state.handle_manager.generate_id.return_value = "version_001"

        # 执行
        result = native.execute(mock_state)

        # 验证
        assert isinstance(result, Version)
        assert result.version_value == VERSION_FROZEN_THRONE
        assert result.type_name == "version"
